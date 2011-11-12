#!/usr/bin/python
# -*- coding: utf-8 -*-
#License BSD
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from Socket.DataAccessControl import DataAccessControl
from mobobj import Mob
import sys
import os
import copy
import time
import traceback

class Event(DataAccessControl):
	def __init__(self):
		self.add("id", 0)
		self.add("pclist", {})
		self.add("moblist", {})
		self.add("lock_pclist", None)
		self.add("lock_moblist", None)
		self.add("itemobj", None)
		self.add("itemdic", {})
		self.add("mapdic", {})
		self.add("shopdic", {})
		self.add("npcdic", {})
		self.add("mobdic", {})
		self.add("pack", None)
		self.add("send", None)
		self.add("sendmap", None)
		self.add("sendmapwithoutself", None)
		self.add("sendserver", None)
		self.add("netio", None)
		self.add("createpacket", None)
		self.add("serverobj", None)
		self.add("eventhandle", None)

def say(pc, text, npc_name="", motion_id=131, npcid=None):
	"""npc say"""
	if not npcid:
		npcid = pc.e.id
	text = str(text)
	#NPCメッセージのヘッダー
	datatype,datacontent = pc.e.createpacket.create03f8()
	pc.e.send(datatype,datacontent,pc.mapclient,None)
	#NPCメッセージ
	text = text.replace("$r","$R")
	split = text.split("$R")
	for text in split:
		datatype, datacontent = pc.e.createpacket.create03f7(pc,text,npc_name,\
													motion_id,npcid)
		pc.e.send(datatype,datacontent,pc.mapclient,None)
	#NPCメッセージのフッター
	datatype, datacontent = pc.e.createpacket.create03f9()
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def warp(pc, mapid, x, y):
	"""warp"""
	mapid = str(mapid)
	mapinfo = pc.e.mapdic.get(int(mapid))
	if mapinfo == None:
		message = "map id "+mapid+" not found"
		print "[event]", message
		systemmessage(pc, message)
		return
	elif int(x) > 255:
		systemmessage(pc, "warp error / x > 255")
		return
	elif int(y) > 255:
		systemmessage(pc, "warp error / y > 255")
		return
	pc.x = int(x)
	pc.y = int(y)
	pc.dir = 0
	pc.rawdir = 0
	if mapinfo != None:
		centerx = mapinfo.centerx
		centery = mapinfo.centery
	else:
		centerx,centery = 128,128
	#print centerx,centery
	rawxcache = int(x) - float(centerx)
	rawycache = float(centery) - int(y)
	if str(centerx)[-2:] == ".5":
		rawxcache = rawxcache + 0.5
	if str(centery)[-2:] == ".5":
		rawycache = rawycache - 0.5
	rawx = int(rawxcache) * 100
	rawy = int(rawycache) * 100
	# raw x (word) = int ( x - 中心座標ｘ ) x 100
	# if 中心座標ｘ [-2:]  = ".5" , raw x + 0.5
	# if  raw x < 0 , raw x = raw x + 65536
	# raw y (word) = int ( 中心座標ｙ - y  ) x 100
	# if 中心座標y  [-2:] = ".5" , raw y - 0.5
	# if  raw y < 0 , raw y = raw y + 65536
	if str(rawxcache)[:1] == "-":
		rawx += 65536
	if str(rawycache)[:1] == "-":
		rawy += 65536
	rawx,rawy = str(rawx), str(rawy)
	rawx,rawy = rawx.replace(".0",""),rawy.replace(".0","")
	warpraw(pc, mapid, rawx, rawy, x, y)

def warpraw(pc, mapid, rawx, rawy, x=None, y=None):
	"""warp raw"""
	mapid = int(mapid)
	rawx = int(rawx)
	rawy = int(rawy)
	mapinfo = pc.e.mapdic.get(mapid)
	if mapinfo == None:
		message = "map id %s not found" % (mapid, )
		print "[event]", message
		systemmessage(pc, message)
		return
	elif rawx > 65535:
		systemmessage(pc, "warpraw error / rawx > 65535")
		return
	elif rawy > 65535:
		systemmessage(pc, "warpraw error / rawy > 65535")
		return
	if x == None or y == None:
		if mapinfo != None:
			centerx = mapinfo.centerx
			centery = mapinfo.centery
		else:
			centerx,centery = 128,128
		x, y = rawx, rawy
		if x >= 32768:
			x = x - 65536
		if y >= 32768:
			y = y - 65536
		x = int(float(centerx)+(x/100.0))
		y = int(float(centery)-(y/100.0))
		pc.x, pc.y = x, y
	pc.rawx, pc.rawy = rawx, rawy
	#print pc.rawx, pc.rawy
	if int(pc.map) == mapid:
		#print pc.rawx,pc.rawy
		#キャラ移動アナウンス
		datatype,datacontent = pc.e.createpacket.create11f9(pc, 14)
		#print datatype,datacontent
		pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)
	else:
		#PC消去
		datatype,datacontent = pc.e.createpacket.create1211(pc)
		pc.e.sendmapwithoutself(datatype, datacontent, pc.e.pclist, pc, None)
		#
		pc.map = int(mapid)
		#マップ変更通知
		datatype,datacontent = pc.e.createpacket.create11fd(pc, mapid, x, y)
		pc.e.send(datatype, datacontent, pc.mapclient, None)
		#モンスター関連（MonsterID通知？）
		datatype,datacontent = pc.e.createpacket.create122a()
		pc.e.send(datatype, datacontent, pc.mapclient, None)

def giveitem(pc, itemid, count=1, fromwarehouse=False, towarehouse=None):
	"""give item"""
	try:
		if int(count) > 65535:
			print "[event]", "giveitem count too big",count
			return
	except ValueError:
		print "[event]", "giveitem count not a number",count
		return None,None
	itemid = int(itemid)
	if towarehouse == None:
		itemlist = pc.sort.item
		pcitemdic = pc.item
		equiplist = pc.equiplist()
	else:
		towarehouse = int(towarehouse)
		itemlist = pc.sort.warehouse
		pcitemdic = pc.warehouse
		equiplist = []
	count = int(count)
	printcount = str(count)
	item = pc.e.itemobj.createitem(pc.e.itemdic, itemid)
	stockidlist = []
	newcount = 0
	if item.stock == 1:
		for x in itemlist:
			x = int(x)
			if x == 0:
				continue
			if x in equiplist:
				continue
			iinfo = pcitemdic.get(x)
			if iinfo == None:
				print "can not get pc item info / giveitem", x, pc.account
				continue
			if iinfo.id == itemid and iinfo.count != 999:
				if towarehouse == None:
					stockidlist.append(x)
	for stockid in stockidlist:
		if count == 0:
			break
		count = pcitemdic[stockid].count+count
		if count > 999:
			count = count - 999
			newcount = 999
		else:
			newcount = count
			count = 0
		pcitemdic[stockid].count = newcount
		if towarehouse == None:
			#アイテム個数変化
			datatype,datacontent = pc.e.createpacket.create09cf(stockid, newcount)
			pc.e.send(datatype, datacontent, pc.mapclient, None)
	while True:
		if count == 0:
			break
		if count > 999:
			count = count - 999
			newcount = 999
		else:
			newcount = count
			count = 0
		item.count = newcount
		existitemid = []
		existitemid.extend(map(int, pc.item.keys()))
		existitemid.extend(map(int, pc.warehouse.keys()))
		if towarehouse:
			newid = 10000
		else:
			newid = 1
		while newid in existitemid:
			newid += 1
		itemlist.append(newid)
		pcitemdic[newid] = copy.copy(item)
		if towarehouse == None:
			#アイテム取得
			datatype,datacontent = pc.e.createpacket.create09d4(pc, item, newid, 02)
			pc.e.send(datatype, datacontent, pc.mapclient, None)
		else:
			pcitemdic[newid].warehouse = towarehouse
			#倉庫インベントリーデータ
			datatype,datacontent = pc.e.createpacket.create09f9(pc,item,newid,30)
			pc.e.send(datatype, datacontent, pc.mapclient, None)
	sysenc = sys.getfilesystemencoding()
	print "[event]", "giveitem", printcount,
	print str(item.name).decode("utf-8").encode(sysenc), towarehouse
	if towarehouse == None:
		systemmessage(pc, "%sを%s個入手しました"%(item.name, printcount))
	else:
		systemmessage(pc, "%sを%s個預かりました"%(item.name, printcount))
	returnitem = copy.copy(item)
	return returnitem

def takeitem(pc, itemid, count=1):
	"""take item"""
	itemlist = pc.sort.item
	pcitemdic = pc.item
	equiplist = pc.equiplist()
	itemid = int(itemid)
	count = int(count)
	printcount = str(count)
	#print itemlist, pcitemdic
	for x in itemlist:
		x = int(x)
		if x == 0:
			continue
		if x in equiplist:
			continue
		iinfo = pcitemdic.get(x)
		if iinfo == None:
			print "can not get pc item info / takeitem", x, pc.account
			continue
		if iinfo.id == itemid:
			if iinfo.count <= count:
				printcount = str(iinfo.count)
				returnitem = copy.copy(iinfo)
				itemlist.remove(x)
				del pcitemdic[x]
				#インベントリからアイテム消去
				datatype,datacontent = pc.e.createpacket.create09ce(x)
				pc.e.send(datatype, datacontent, pc.mapclient, None)
				print "[event]", "take item", itemid,count
			else:
				stockid = x
				#print int(pcitemdic[x].count), int(count)
				newcount = int(iinfo.count) - int(count)
				returnitem = copy.copy(iinfo)
				returnitem.count = int(count)
				pcitemdic[x].count = newcount
				#アイテム個数変化
				datatype,datacontent = pc.e.createpacket.create09cf(stockid, newcount)
				pc.e.send(datatype, datacontent, pc.mapclient, None)
				print "[event]", "take item", itemid, count
			systemmessage(pc, "%sを%s個失いました"%(returnitem.name, printcount))
			return returnitem
	print "[event]", "takeitem id not found", itemid
	return None

def takeitembyiid(pc, iid, count=1, fromwarehouse=False):
	"""take item by iid"""
	if not fromwarehouse:
		itemlist = pc.sort.item
		pcitemdic = pc.item
		equiplist = pc.equiplist()
	else:
		itemlist = pc.sort.warehouse
		pcitemdic = pc.warehouse
		equiplist = []
	iid = int(iid)
	count = int(count)
	printcount = str(count)
	for x in itemlist:
		x = int(x)
		if x == 0:
			continue
		if x in equiplist:
			continue
		if x == iid:
			iinfo = pcitemdic.get(x)
			if iinfo == None:
				print "can not get pc item info / takeitembyiid", x, pc.account
				continue
			if iinfo.count <= count:
				printcount = iinfo.count
				returnitem = copy.copy(iinfo)
				itemlist.remove(x)
				del pcitemdic[x]
				if not fromwarehouse:
					#インベントリからアイテム消去
					datatype,datacontent = pc.e.createpacket.create09ce(x)
					pc.e.send(datatype, datacontent, pc.mapclient, None)
				print "[event]", "take item by iid", iid, count, fromwarehouse
			else:
				stockid = x
				#print int(pcitemdic[x].count),int(count)
				newcount = int(iinfo.count) - int(count)
				returnitem = copy.copy(iinfo)
				returnitem.count = int(count)
				pcitemdic[x].count = newcount
				if not fromwarehouse:
					#アイテム個数変化 
					datatype,datacontent = pc.e.createpacket.create09cf(stockid, newcount)
					pc.e.send(datatype, datacontent, pc.mapclient, None)
				print "[event]", "take(minus) item by iid", iid, count, fromwarehouse
			if not fromwarehouse:
				systemmessage(pc, "%sを%s個失いました"%(returnitem.name, printcount))
			else:
				systemmessage(pc, "%sを%s個取り出しました"%(returnitem.name, printcount))
			return returnitem
	print "[event]", "takeitem iid not found", iid
	return None

def countitem(pc, itemid):
	"""count item"""
	itemid = int(itemid)
	itemlist = pc.sort.item
	equiplist = pc.equiplist()
	returncount = 0
	for x in itemlist:
		x = int(x)
		if x == 0:
			continue
		if x in equiplist:
			continue
		if pc.item[x].id == itemid:
			returncount += int(pc.item[x].count)
	return returncount

def select(pc, optionlist, title=""):
	"""select window"""
	while True:
		try:
			optionlist.remove("")
		except:
			break
	if len(optionlist) > 65:
		say(pc, "option count can not large than 65", "error")
		print "[event]", "error [ option count can not large than 65 ]"
		return 0
	pc.selectresult = None
	datatype,datacontent = pc.e.createpacket.create0604(optionlist, title)
	pc.e.send(datatype, datacontent, pc.mapclient, None)
	while not pc.selectresult:
		if not pc.online:
			pc.selectresult = None
			return None
		time.sleep(0.1)
	selectresult = int(pc.selectresult)
	pc.selectresult = None
	return selectresult

def motion(pc, motionid, isloop=0):
	"""motion"""
	isloop = int(isloop)
	motionid = int(motionid)
	if isloop != 0:
		pc.motion = motionid
		isloop = 1
	datatype,datacontent = pc.e.createpacket.create121c(pc, motionid, isloop)
	pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)

def systemmessage(pc, message, fast=False):
	"""system message"""
	datatype,datacontent = pc.e.createpacket.create03e9(message, -1)
	pc.e.send(datatype, datacontent, pc.mapclient, None, fast)

def servermessage(pc, message, fast=False):
	"""server message"""
	datatype,datacontent = pc.e.createpacket.create03e9(message, 0)
	pc.e.sendserver(datatype, datacontent, pc.e.pclist, pc, None, fast)

def getgold(pc):
	"""get gold num"""
	return pc.gold

def givegold(pc, goldgive):
	"""give gold"""
	pc.gold = int(pc.gold) + int(goldgive)
	returntype = True
	if int(pc.gold) > 99999999:
		pc.gold = 99999999
		returntype = False
	datatype,datacontent = pc.e.createpacket.create09ec(pc)
	pc.e.send(datatype, datacontent, pc.mapclient, None)
	return returntype

def takegold(pc, goldtake):
	"""take gold"""
	if int(pc.gold) < int(goldtake):
		#pc.gold = 0
		return False
	else:
		pc.gold = int(pc.gold) - int(goldtake)
	datatype,datacontent = pc.e.createpacket.create09ec(pc)
	pc.e.send(datatype, datacontent, pc.mapclient, None)
	return True

def updategold(pc, gold=None):
	"""update gold view"""
	if gold == None:
		pc.gold = int(pc.gold)
	else:
		pc.gold = int(gold)
	datatype,datacontent = pc.e.createpacket.create09ec(pc)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def createitem(pc, itemid):
	"""create item
	return Object.itemobj.Item"""
	itemid = int(itemid)
	item = pc.e.itemobj.createitem(pc.e.itemdic, itemid)
	return item

def npcshop(pc, shopid):
	"""npc shop"""
	shopid = int(shopid)
	itemidlist = pc.e.shopdic.get(shopid)
	if itemidlist == None:
		print "[event]", "shopid not found", shopid
		return
	datatype,datacontent = pc.e.createpacket.create0613(pc, itemidlist)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def updateitemwindow(pc):
	"""update item window"""
	itemlist = pc.sort.item
	equiplist = pc.equiplist()
	for x in itemlist:
		x = int(x)
		if x == 0:
			continue
		if x in equiplist:
			continue
		stockid = x
		newcount = pc.item[stockid].count
		#アイテム個数変化
		datatype,datacontent = pc.e.createpacket.create09cf(stockid, newcount)
		pc.e.send(datatype, datacontent, pc.mapclient, None)

def npctrade(pc):
	"""npc trade / for trash or quest"""
	pc.isnpctrade = True
	pc.tradereturnlist = list()
	npcinfo = pc.e.npcdic.get(int(pc.e.id))
	if npcinfo == None:
		npcname = ""
	else:
		npcname = npcinfo.name
	isnpc = 1
	datatype,datacontent = pc.e.createpacket.create0a0f(pc, isnpc, npcname)
	pc.e.send(datatype, datacontent, pc.mapclient, None)
	while pc.isnpctrade:
		if not pc.online:
			pc.isnpctrade = False
			return ()
		time.sleep(0.1)
	if not pc.online:
		pc.isnpctrade = False
		return ()
	updateitemwindow(pc)
	return pc.tradereturnlist

def npcmotion(pc, motionid, npcid=None):
	"""npc motion"""
	if not npcid:
		npcid = pc.e.id
	datatype,datacontent = pc.e.createpacket.create121c(pc, motionid, 0, npcid)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def wait(pc, time_ms):
	"""let client wait"""
	datatype,datacontent = pc.e.createpacket.create05eb(time_ms)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def npcsell(pc):
	"""npc sell window"""
	datatype,datacontent = pc.e.createpacket.create0615(pc)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def updatepc(pc):
	"""update pc information"""
	datatype, datacontent = pc.e.createpacket.create020e(pc)
	pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)

def warehouse(pc, warehouse_id):
	"""warehouse window"""
	warehouse_id = int(warehouse_id)
	num_max = 300
	num_here = 0
	num_all = 0
	for x in pc.sort.warehouse:
		num_all = num_all + 1
		if pc.warehouse[x].warehouse == warehouse_id:
			num_here = num_here + 1
	datatype,datacontent = pc.e.createpacket.create09f6(pc, warehouse_id, num_here, num_all, num_max)
	pc.e.send(datatype, datacontent, pc.mapclient, None)
	for x in pc.sort.warehouse:
		x = int(x)
		part = pc.warehouse[x].warehouse
		if part == warehouse_id:
			part = 30
		datatype,datacontent = pc.e.createpacket.create09f9(pc, pc.warehouse[x], x, part)
		pc.e.send(datatype, datacontent, pc.mapclient, None)
	pc.warehouse_open = warehouse_id
	datatype,datacontent = pc.e.createpacket.create09fa()
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def playbgm(pc, sound_id, loop=1, volume=100):
	"""play bgm / bgm_xxx.wma"""
	datatype,datacontent = pc.e.createpacket.create05f0(sound_id, loop, volume)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def playse(pc, sound_id, loop=0, volume=100, balance=50):
	"""play se / se_xxx.wav"""
	datatype,datacontent = pc.e.createpacket.create05f5(sound_id, loop, volume, balance)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def playjin(pc, sound_id, loop=0, volume=100, balance=50):
	"""play jin / jin_xxx.wav"""
	datatype,datacontent = pc.e.createpacket.create05fa(sound_id, loop, volume, balance)
	pc.e.send(datatype, datacontent, pc.mapclient, None)

def effect(pc, effect_id=0):
	"""effect show"""
	datatype,datacontent = pc.e.createpacket.create060e(pc, effect_id)
	pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)

def speed(pc, speed=410):
	"""move speed change"""
	pc.status.speed = int(speed)
	datatype,datacontent = pc.e.createpacket.create1239(pc, pc.status.speed)
	pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)

def mobmove(mob, x, y, pclist, mapdic, netio, createpacket):
	"""for mob move"""
	mapinfo = mapdic.get(int(mob.map))
	if mapinfo == None:
		print "[event]", "movemob error / map id", mob.map, "not found / movemob"
		return
	elif int(x) > 255:
		print "[event]", "movemob error / x > 255"
		return
	elif int(y) > 255:
		print "[event]", "movemob error / y > 255"
		return
	mob.x = int(x)
	mob.y = int(y)
	mob.dir = 0
	mob.rawdir = 0
	if mapinfo != None:
		centerx = mapinfo.centerx
		centery = mapinfo.centery
	else:
		centerx, centery = 128,128
	#print centerx,centery
	rawxcache = int(x) - float(centerx)
	rawycache = float(centery) - int(y)
	if str(centerx)[-2:] == ".5":
		rawxcache += 0.5
	if str(centery)[-2:] == ".5":
		rawycache -= 0.5
	rawx = int(rawxcache) * 100
	rawy = int(rawycache) * 100
	# raw x (word) = int ( x - 中心座標ｘ ) x 100
	# if 中心座標ｘ [-2:]  = ".5" , raw x + 0.5
	# if  raw x < 0 , raw x = raw x + 65536
	# raw y (word) = int ( 中心座標ｙ - y  ) x 100
	# if 中心座標y  [-2:] = ".5" , raw y - 0.5
	# if  raw y < 0 , raw y = raw y + 65536
	if str(rawxcache)[:1] == "-":
		rawx += 65536
	if str(rawycache)[:1] == "-":
		rawy += 65536
	rawx,rawy = int(rawx),int(rawy)
	mobmoveraw(mob, rawx, rawy, pclist, mapdic, netio,\
				createpacket, x, y)

def mobmoveraw(mob, rawx, rawy, pclist, mapdic, \
				netio, createpacket, x=None, y=None):
	"""mob move raw / call from mob move"""
	mapid = int(mob.map)
	rawx = int(rawx)
	rawy = int(rawy)
	mapinfo = mapdic.get(int(mob.map))
	if mapinfo == None:
		print "[event]", "movemobraw error / map id", mapid, "not found"
	elif rawx > 65535:
		print "[event]", "movemobraw error / rawx > 65535", rawx, x
		return
	elif rawy > 65535:
		print "[event]", "movemobraw error / rawy > 65535", rawy, y
		return
	if x == None or y == None:
		if mapinfo != None:
			centerx = mapinfo.centerx
			centery = mapinfo.centery
		else:
			centerx,centery = 128,128
		x, y = int(rawx), int(rawy)
		if x >= 32768:
			x = x - 65536
		if y >= 32768:
			y = y - 65536
		x = int(float(centerx)+(x/100.0))
		y = int(float(centery)-(y/100.0))
		mob.x, mob.y = x, y
	mob.rawx, mob.rawy = rawx, rawy
	#モブ移動アナウンス
	datatype,datacontent = createpacket.create11f9(mob, 6) #6 歩き
	#print datatype,datacontent
	netio.sendmap(datatype, datacontent, pclist, mob, None)
	#will use mob.map

def mob(pc, mobid):
	"""make mob and announce"""
	mobid = int(mobid)
	print "[event]", "make mob id", mobid
	mobfromdic = pc.e.mobdic.get(mobid)
	if not mobfromdic:
		message = "mob id "+str(mobid)+" not found"
		print "[event]", message
		systemmessage(pc, message)
		return
	newmob = copy.copy(mobfromdic)
	newmob.id = mobid
	newmob.sid = 10000
	newmob.centerx = pc.x
	newmob.centery = pc.y
	newmob.x = pc.x
	newmob.y = pc.y
	newmob.dir = pc.dir
	newmob.map = pc.map
	newmob.damagedic = {} # None -> {}
	with pc.e.lock_pclist and pc.e.lock_moblist:
		existid = []
		for p in pc.e.pclist.itervalues():
			try:
				existid.append(int(p.sid))
			except:
				print "[event]", "create mob error at append pc sid", traceback.format_exc()
		existid.extend(pc.e.moblist.keys()) #maybe need map(int, keys)
		while newmob.sid in existid:
			newmob.sid += 1
		newmob.charid = newmob.sid # fake pc
		pc.e.moblist[newmob.sid] = newmob
		#モンスターID通知
		datatype,datacontent = pc.e.createpacket.create122a(pc, (newmob.sid,))
		pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)
		#モンスター情報
		datatype,datacontent = pc.e.createpacket.create1220(pc, newmob)
		pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)
		#モンスターの状態
		datatype,datacontent = pc.e.createpacket.create157c(newmob)
		pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)

def killallmob(pc):
	"""kill all mob on pc.map"""
	with pc.e.lock_moblist:
		removelist = []
		for sid, mob in pc.e.moblist.items():
			if int(mob.map) == int(pc.map):
				removelist.append(sid)
		for sid in removelist:
			try:
				del pc.e.moblist[sid]
				#モンスター消去
				datatype,datacontent = pc.e.createpacket.create1225(sid)
				pc.e.sendmap(datatype, datacontent, pc.e.pclist, pc, None)
			except:
				print "[event]", "killallmob error", traceback.format_exc()
	systemmessage(pc, "kill %s mob"%(len(removelist), ))
	print "[event]", "kill", len(removelist), "mob"