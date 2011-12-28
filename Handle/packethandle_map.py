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
import os
import socket
import sys
import copy
import time
import thread
import threading
import hashlib
import Socket.rijndael
from Object import eventobj
from Object.itemobj import Item
from Handle.eventhandle import EventHandle
from Handle.attackhandle import AttackHandle
import traceback
PACKET_NOT_PRINT = ["0032", #ping
				"0fa5", #battle status change
				"11f8", #move
				"0f9f", #attack
				]

class PacketHandle_Map():
	def __init__(self):
		self.dolist = list(set(map(self.rm, dir(self))))
		#dir self to list function ->
		#remove not start from "do_" ->
		#remove duplicate ->
		#transform type "set" to "list"
		self.dolist.remove("")
		#print self.dolist
		self.sysenc = sys.getfilesystemencoding()
		self.returntype = None
		self.returndata = None

	def rm(self, s):
		if s[:3] == "do_":
			return s[3:]
		else:
			return ""

	def do(self, s, *args):
		try:
			if s in self.dolist:
				eval("self.do_"+s)(*args)
			else:
				print "[ map ]", "recv", s, "packet type didn't define"
		except:
			print "[ map ]", "error in do /", traceback.format_exc()
	
	def init(self, serverobj):
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		self.encode = self.cryptio.encode
		self.decode = self.cryptio.decode
		self.pack = self.netio.pack
		self.send = self.netio.send
		self.sendmap = self.netio.sendmap
		self.sendmapwithoutself = self.netio.sendmapwithoutself
		self.sendserver = self.netio.sendserver
		self.event = eventobj.Event()
		self.event.id = 00000000
		self.event.pclist = self.pclist
		self.event.moblist = self.moblist
		self.event.petlist = self.petlist
		self.event.lock_pclist = self.lock_pclist
		self.event.lock_moblist = self.lock_moblist
		self.event.lock_petlist = self.lock_petlist
		self.event.itemobj = self.itemobj
		self.event.itemdic = self.itemdic
		self.event.mapdic = self.mapdic
		self.event.shopdic = self.shopdic
		self.event.npcdic = self.npcdic
		self.event.mobdic = self.mobdic
		self.event.petdic = self.petdic
		self.event.pack = self.pack
		self.event.send = self.send
		self.event.sendmap = self.sendmap
		self.event.sendmapwithoutself = self.sendmapwithoutself
		self.event.sendserver = self.sendserver
		self.event.netio = self.netio
		self.event.createpacket = self.createpacket
		self.event.serverobj = self.serverobj
		self.event.eventhandle = self.eventhandle

	def packet_handle(self, data, datalength, pc):
		try:
			returntype,returndata = None,None
			recvhead = data[0:4]
			recvtype = data[4:8]
			recvcontent = data[8:]
			tmp_datalength = int(recvhead,16) * 2 - 4 # 4 --- recvtype
			tmp_dataadd = recvcontent[tmp_datalength:]
			tmp_datacheck = tmp_dataadd.replace("0","")
			recvcontent = recvcontent[:tmp_datalength]
			if tmp_datacheck != "":
				self.packet_handle(tmp_dataadd,None,pc)
			if recvtype not in PACKET_NOT_PRINT:
				#print datalength
				print "[ map ]", recvhead, recvtype, recvcontent
		#datahead = (len(datatype)+len(datacontent)) / 2
		#or datahead = len(data) / 2 - 2
			self.returntype, self.returndata = None, None
			self.do(recvtype, pc, data, datalength, recvhead, recvtype, recvcontent)
		except:
			print "[ map ]", "error in packet_handle /", traceback.format_exc()
			self.returntype = None
			self.returndata = None
		return self.returntype, self.returndata
	
	def do_0032(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""接続確認(マップサーバとのみ)#20秒一回"""
		datatype, datacontent = self.createpacket.create0033(None, None, reply=True)
		self.send(datatype, datacontent, pc.mapclient, None)
	
	#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>接続
	def do_000a(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""接続・接続確認"""
		print "[ map ]", "connection initialization"
		datatype, datacontent = self.createpacket.create000b(recvcontent)
		self.send(datatype, datacontent, pc.mapclient, None)
		datatype,datacontent = self.createpacket.create000f()
		self.send(datatype, datacontent, pc.mapclient, None)
	
	def do_0010(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""マップサーバーに認証情報の送信"""
		print "[ map ]", "certification account and password form client"
		chars = recvcontent.decode("hex")
		account = chars[1:chars.index("\x00")]
		passwordhash = chars[chars.index("\x00")+1:]
		passwordhash = passwordhash[1:passwordhash.rindex("\x00\x06")]
		#print passwordhash.encode("hex")
		print "[login]", account, passwordhash
		if self.pclist.get(account) == None:
			self.returntype = "accountnotfound"
			self.returndata = None
			pc.mapclient.transport.loseConnection()
			if pc.client != None:
				pc.client.transport.loseConnection()
		else:
			#self.pclist[account].password is a hash from md5
			front_word = str(int("30303030",16))
			back_word = str(int("30303030",16))
			buf = front_word+self.pclist[account].password+back_word
			finallyhash = hashlib.sha1(buf).hexdigest()
			if passwordhash == finallyhash:
				mapclient = pc.mapclient
				pc = self.pclist[account]
				pc.mapclient = mapclient
				#set
				pc.online = True
				#reset
				pc.logout = False
				#
				self.returntype = "changepc"
				self.returndata = pc
				datatype,datacontent = self.createpacket.create0011()
				self.send(datatype,datacontent,pc.mapclient,None)
			else:
				self.returntype = "accountnotfound"
				#returntype should be passworderror
				returndata = None
				pc.mapclient.transport.loseConnection()
				if pc.client != None:
					pc.client.transport.loseConnection()
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<接続
	
	#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>キャラおよびワールドの情報通知
	def do_01fd(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""選択したキャラ番号通知"""
		print "[ map ]", "character detail request ...",
		#キャラ速度通知・変更#マップ読み込み中は10
		datatype,datacontent = self.createpacket.create1239(pc, 10)
		self.send(datatype,datacontent,pc.mapclient,None)#----------------------------
		#キャラのモード変更
		datatype,datacontent = self.createpacket.create1239(pc, 2)
		self.send(datatype,datacontent,pc.mapclient,None)#----------------------------
		#右クリ設定
		datatype,datacontent = self.createpacket.create1a5f()
		self.send(datatype,datacontent,pc.mapclient,None)#----------------------------
		#インベントリ情報
		#itemlist = sorted(pc.item,key=int)
		itemlist = pc.sort.item
		for x in itemlist:
			if int(x) == 0:
				continue
			x = int(x)
			item = pc.item.get(x)
			part = 02
			if item.type != "NONE":
				if x != 0 and x == pc.equip.head:
					if item.type == "HELM":
						part = 6
					elif item.type == "ACCESORY_HEAD":
						part = 7
					else:
						continue
				elif x != 0 and x == pc.equip.face:
					if item.type == "FULLFACE":
						part = 6 #8 before ver315
					elif item.type == "ACCESORY_FACE":
						part = 8 #9 before ver315
					else:
						continue
				elif x != 0 and x == pc.equip.chestacce:
					part = 10
				elif x != 0 and x == pc.equip.tops:
					part = 11
					#if item.type == "ONEPIECE":
					#	part_copy = 12
				elif x != 0 and x == pc.equip.bottoms:
					part = 12
				elif x != 0 and x == pc.equip.backpack:
					part = 13
				elif x != 0 and x == pc.equip.right:
					part = 14
				elif x != 0 and x == pc.equip.left:
					part = 15
				elif x != 0 and x == pc.equip.shoes:
					part = 16
				elif x != 0 and x == pc.equip.socks:
					part = 17
				elif x != 0 and x == pc.equip.pet:
					part = 18
			datatype,datacontent = self.createpacket.create0203(pc,item,x,part)
			self.send(datatype,datacontent,pc.mapclient,None)
		#自分のキャラクター情報
		datatype,datacontent = self.createpacket.create01ff(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#システムメッセージ
		#構えが「叩き」に変更されました
		datatype,datacontent = self.createpacket.create03f2(4)
		self.send(datatype,datacontent,pc.mapclient,None)
		#ゴールド入手 
		datatype,datacontent = self.createpacket.create09ec(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#最大HP/MP/SP
		datatype,datacontent = self.createpacket.create0221(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#現在のHP/MP/SP/EP
		datatype,datacontent = self.createpacket.create021c(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#ステータス・補正・ボーナスポイント
		datatype,datacontent = self.createpacket.create0212(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#詳細ステータス
		datatype,datacontent = self.createpacket.create0217(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#現在CAPA/PAYL
		datatype,datacontent = self.createpacket.create0230(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#最大CAPA/PAYL
		datatype,datacontent = self.createpacket.create0231(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#職業
		datatype,datacontent = self.createpacket.create0244(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#スキル一覧0
		datatype,datacontent = self.createpacket.create0226(pc, 0)
		print datatype,datacontent
		self.send(datatype,datacontent,pc.mapclient,None)
		#スキル一覧1
		datatype,datacontent = self.createpacket.create0226(pc, 1)
		self.send(datatype,datacontent,pc.mapclient,None)
		#リザーブスキル
		datatype,datacontent = self.createpacket.create022e(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#Lv JobLv ボーナスポイント スキルポイント
		datatype,datacontent = self.createpacket.create023a(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#EXP/JOBEXP
		datatype,datacontent = self.createpacket.create0235(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#キャラの見た目を変更
		datatype,datacontent = self.createpacket.create09e9(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		
		#0.43 add
		#キャラのモード変更
		datatype, datacontent = self.createpacket.create0fa7(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		#もてなしタイニーアイコン
		datatype, datacontent = self.createpacket.create1f72()
		self.send(datatype, datacontent, pc.mapclient, None)
		#キャラの状態
		datatype, datacontent = self.createpacket.create157c(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		#HEARTスキル
		datatype, datacontent = self.createpacket.create022d()
		self.send(datatype, datacontent, pc.mapclient, None)
		#属性値
		datatype, datacontent = self.createpacket.create0223()
		self.send(datatype, datacontent, pc.mapclient, None)
		#モンスターID通知
		datatype, datacontent = self.createpacket.create122a()
		self.send(datatype, datacontent, pc.mapclient, None)
		#スタンプ帳詳細
		datatype, datacontent = self.createpacket.create1bbc()
		self.send(datatype, datacontent, pc.mapclient, None)
		#不明
		datatype, datacontent = self.createpacket.create025d()
		self.send(datatype, datacontent, pc.mapclient, None)
		#不明
		datatype, datacontent = self.createpacket.create0695()
		self.send(datatype, datacontent, pc.mapclient, None)
		#wrp ranking関係
		datatype, datacontent = self.createpacket.create0236()
		self.send(datatype, datacontent, pc.mapclient, None)
		
		#マップ情報完了通知
		#MAPログイン時に基本情報を全て受信した後に受信される
		datatype,datacontent = self.createpacket.create1b67()
		self.send(datatype,datacontent,pc.mapclient,None)
		print "[ map ]", "send character detail over",

	def do_00b8(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""detected cheat tool"""
		print "[ map ]", "client detect cheat tool"
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<キャラおよびワールドの情報通知
	
	def do_11fe(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""MAPワープ完了通知"""
		print "[ map ]", "client map loading over"
		pc.visible = True#見える状態になった
		pc.motion = "111"#モーションリセット
		#ログインイベント
		if self.serverobj.loginevent and not pc.loginevent:
			pc.loginevent = True
			pc.e = copy.copy(self.event)
			pc.e.id = self.serverobj.loginevent
			pc.e.eventhandle.run(pc)
		#キャラ速度通知・変更
		datatype, datacontent = self.createpacket.create1239(pc,pc.status.speed)
		self.send(datatype, datacontent, pc.mapclient, None)
		#クエスト回数・時間
		datatype,  datacontent = self.createpacket.create196e(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		#ステータス試算結果
		datatype,datacontent = self.createpacket.create0259(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		#マップ情報完了通知
		datatype,datacontent = self.createpacket.create1b67()
		self.send(datatype,datacontent,pc.mapclient,None)
		
		#0.43 add
		#キャラの状態
		datatype, datacontent = self.createpacket.create157c(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		#スキル一覧0
		datatype,datacontent = self.createpacket.create0226(pc, 0)
		self.send(datatype,datacontent,pc.mapclient,None)
		#スキル一覧1
		datatype,datacontent = self.createpacket.create0226(pc, 1)
		self.send(datatype,datacontent,pc.mapclient,None)
		#リザーブスキル
		datatype,datacontent = self.createpacket.create022e(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#HEARTスキル
		datatype, datacontent = self.createpacket.create022d()
		self.send(datatype, datacontent, pc.mapclient, None)
		#キャラの見た目を変更
		datatype, datacontent = self.createpacket.create09e9(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		#現在のHP/MP/SP/EP
		datatype, datacontent = self.createpacket.create021c(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
		
		#他キャラ情報
		with self.lock_pclist:
			for p in self.pclist.itervalues():
				if not (p.online and p.mapclient):
					continue
				if not (p.charid != pc.charid and p.map == pc.map):
					continue
				#print "send 120c"
				#他キャラ情報→自キャラ
				datatype, datacontent = self.createpacket.create120c(p)
				self.send(datatype, datacontent, pc.mapclient, None)
				if p.pet:
					datatype, datacontent = pc.e.createpacket.create122f(p, p.pet)
					self.send(datatype, datacontent, pc.mapclient, None)
				#自キャラ情報→他キャラ
				datatype, datacontent = self.createpacket.create120c(pc)
				self.send(datatype, datacontent, p.mapclient, None)
		#モンスター情報
		with self.lock_moblist:
			for m in self.moblist.itervalues(): # in self.moblist.keys()
				if m.hp <= 0:
					continue
				if not (m.map == pc.map):
					continue
				#モンスターID通知
				datatype, datacontent = self.createpacket.create122a(pc, (m.sid,), m.npc)
				self.send(datatype, datacontent, pc.mapclient, None)
				#モンスター情報
				datatype, datacontent = self.createpacket.create1220(pc, m)
				self.send(datatype, datacontent, pc.mapclient, None)
		#pet info
		eventobj.unsetpet(pc)
		eventobj.setpet(pc)
	
	def do_020d(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""キャラクタ情報要求"""
		requestid = int(recvcontent[0:8],16)
		print "[ map ]", "request other character detail", requestid
		if requestid >= 20000: #pet
			with self.lock_petlist:
				pet = self.petlist.get(requestid)
				if pet:
					print "[ map ]", "send pet sid %s info (020e)"%pet.sid
					datatype, datacontent = self.createpacket.create020e(pet)
					self.send(datatype, datacontent, pc.mapclient, None)
					return # self.lock_petlist.__exit__
		with self.lock_pclist:
			for p in self.pclist.itervalues(): #player
				if not p.online or p.charid != requestid:
					continue
				#キャラ情報
				#print "send 020e"
				datatype, datacontent = self.createpacket.create020e(p)
				self.send(datatype, datacontent, pc.mapclient, None)
				#datatype,datacontent = self.createpacket.create121c(p, p.motion, "1")
				#self.send(datatype,datacontent,pc.mapclient,None)
				#get kanban
				datatype, datacontent = self.createpacket.create041b(p)
				self.send(datatype, datacontent, pc.mapclient, None)
				break
	
	def do_0fa5(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""戦闘状態変更通知"""
		#print "[ map ]", "battlestatus change",recvcontent[0:2]
		pc.battlestatus = recvcontent[0:2]
		#戦闘状態変更通知
		datatype, datacontent = self.createpacket.create0fa6(pc, pc.battlestatus)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
	
	def do_05e6(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""イベント実行"""
		pc.reset_attack_info()
		pc.e = copy.copy(self.event)
		pc.e.id = int(recvcontent[0:8],16)
		print "[ map ]", "event", pc.e.id ,"start"
		self.eventhandle.run(pc)
	
	def do_09c4(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""アイテム使用"""
		iid = int(recvcontent[0:8],16)
		target = int(recvcontent[8:16],16)
		#x = int(recvcontent[16:18],16)
		#y = int(recvcontent[18:20],16)
		item = pc.item.get(iid)
		if not item:
			return
		if not item.eventid or item.eventid == 0:
			return
		def startevent(rpc, eventid):
			rpc.reset_attack_info()
			rpc.e = copy.copy(self.event)
			rpc.e.id = eventid
			print "[ map ]", "item event", rpc.e.id, "start"
			self.eventhandle.run(rpc)
		if pc.sid == target:
			startevent(pc, item.eventid)
			return
		for p in self.pclist.itervalues():
			if not p.online:
				continue
			if int(p.sid) != target:
				continue
			startevent(p, item.eventid)
			break
	
	def do_03e8(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""オープンチャット送信"""
		data_length = int(recvcontent[0:2],16) * 2
		
		openchattext = recvcontent[2:data_length].decode("hex")
		openchattextsysenc = openchattext.decode("utf-8").encode(self.sysenc)
		pc.e = copy.copy(self.event)
		if self.commandio.run(pc, openchattext):
			return
		print "[ map ]", "[open chat]",openchattextsysenc
		#オープンチャット・システムメッセージ
		datatype, datacontent = self.createpacket.create03e9(openchattext,pc.charid)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
	
	def do_121b(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""モーションセット＆ログアウト"""
		pc.reset_attack_info()
		motionid = int(recvcontent[:4],16)
		isloop = int(recvcontent[4:6],16)
		print "[ map ]", "set motion =", motionid, "loop =", isloop
		#モーション通知
		pc.e = copy.copy(self.event)
		eventobj.motion(pc, motionid, isloop)
		if motionid == 135 and isloop == 1:
			##ログアウト開始
			print "[ map ]", "client logout waiting"
			datatype,datacontent = self.createpacket.create0020("logoutstart")
			self.send(datatype, datacontent, pc.mapclient, None)
			pc.logout = True
	
	def do_001e(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""ログアウト(PASS鍵リセット・マップサーバーとのみ通信)"""
		if recvcontent.upper() != "FF":
			print "[ map ]", "client logout"
		#hide pet
		eventobj.unsetpet(pc, True)
		#hide pc
		datatype, datacontent = self.createpacket.create1211(pc)
		self.sendmapwithoutself(datatype, datacontent, self.pclist, pc, None)
	
	def do_001f(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""ログアウト開始&ログアウト失敗"""
		if recvcontent[:2] == "00":
			print "[ map ]", "client logout start"
		else:
			print "[ map ]", "client logout failed"
	
	def do_09e2(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""インベントリ移動"""
		iid = int(recvcontent[0:8],16)
		part = int(recvcontent[8:10],16)
		count = int(recvcontent[10:14],16)
		if pc.item.get(iid) == None:
			print "[ map ]", "error on item move", iid
		else:
			print "[ map ]", "item move", iid
			#アイテム保管場所変更
			datatype,datacontent = self.createpacket.create09e3(iid,part)
			self.send(datatype, datacontent, pc.mapclient,None)
			if iid in pc.equiplist():
				#装備を外す時の処理
				pc.unsetequip(iid)
				pc.sort.item.remove(iid)
				pc.sort.item.append(iid)
				print "[ map ]", "unset pc equip", pc.item[iid].id
				#アイテム装備
				datatype,datacontent = self.createpacket.create09e8(-1, -1, 1, 1)
				self.send(datatype, datacontent, pc.mapclient, None)
				#キャラの見た目を変更
				datatype,datacontent = self.createpacket.create09e9(pc)
				self.sendmap(datatype, datacontent, self.pclist, pc, None)
	
	def do_09e7(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""アイテム装備"""
		#pc.reset_attack_info()
		iid = int(recvcontent[0:8],16)
		if not pc.item.get(iid):
			print "[ map ]", "error on item setup", iid
			return
		old, new = pc.setequip(iid, self.itemobj, self.itemdic)
		print "[ map ]", "item setup", pc.item[iid].id, old, new
		if not new:
			#装備しようとする装備タイプが不明の場合
			#アイテム装備
			datatype, datacontent = self.createpacket.create09e8(iid, -1, -2, 1)
			self.send(datatype, datacontent, pc.mapclient, None)
			return
		for x in old:
			if int(x) != 0 and x != "":
				#装備先に居る装備を外す時の処理
				pc.sort.item.remove(x)
				pc.sort.item.append(x)
				#アイテム保管場所変更
				datatype, datacontent = self.createpacket.create09e3(x, 02)
				self.send(datatype, datacontent, pc.mapclient, None)
		#アイテム装備
		datatype,datacontent = self.createpacket.create09e8(iid, new, 0, 1)
		self.send(datatype, datacontent, pc.mapclient, None)
		#キャラの見た目を変更
		datatype,datacontent = self.createpacket.create09e9(pc)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		if new == 18: # set pet
			eventobj.setpet(pc)
	
	def do_11f8(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""自キャラの移動"""
		if pc.logout:
			print "[ map ]", "client cancel logout"
			datatype,datacontent = self.createpacket.create0020("logoutcancel")
			self.send(datatype,datacontent,pc.mapclient,None)
			pc.logout = False
		cachex = int(recvcontent[:4],16)
		cachey = int(recvcontent[4:8],16)
		cachedir = int(recvcontent[8:12],16)
		if pc.rawx != cachex or pc.rawy != cachey:
			pc.motion = 111#モーションリセット
			pc.reset_attack_info()
		pc.rawx = cachex
		pc.rawy =  cachey
		pc.rawdir = cachedir
		cachedir = cachedir / 45
		if cachex >= 32768:
			cachex = cachex - 65536
		if cachey >= 32768:
			cachey = cachey - 65536
		#pc.map = str(pc.map)
		mapinfo = self.mapdic.get(int(pc.map))
		if mapinfo != None:
			centerx = mapinfo.centerx
			centery = mapinfo.centery
		else:
			centerx,centery = 128,128
		cachex = int(float(centerx)+(cachex/100.0))
		cachey = int(float(centery)-(cachey/100.0))
		#print "[ map ]","move",cachex,cachey
		pc.x = cachex
		pc.y = cachey
		pc.dir = cachedir
		#キャラ移動アナウンス
		datatype,datacontent = self.createpacket.create11f9(pc)
		self.sendmapwithoutself(datatype, datacontent, self.pclist, pc, None)
		if pc.pet: #pet move
			eventobj.mobmove(pc.pet, pc.x, pc.y, self.pclist, self.mapdic,
						self.netio, self.createpacket)
	
	def do_0605(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""NPCメッセージ(選択肢)の返信"""
		datatype,datacontent = self.createpacket.create0606()
		self.send(datatype, datacontent, pc.mapclient, None)
		selectresult = int(recvcontent[:2],16)
		pc.selectresult = selectresult
		print "[ map ]", "selectresult =", selectresult
	
	def do_13ba(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""座る/立つの通知"""
		pc.reset_attack_info()
		pc.e = copy.copy(self.event)
		if pc.motion != 135:
			eventobj.motion(pc, 135, 1)
		else:
			eventobj.motion(pc, 111, 1)
		print "[ map ]","sitdown/getup"
	
	def do_0617(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""購入・売却のキャンセル"""
		print "[ map ]","cancel npcshop"
	
	def do_0614(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""NPCショップのアイテム購入"""
		print "[ map ]","pay in npcshop"
		#TODO 書き直しな・・・
		itemcount = int(recvcontent[:2],16)
		recvcontent = recvcontent[2:]
		itemlist = list()
		for x in range(0,itemcount):
			itemlist.append(int(recvcontent[:8],16))
			recvcontent = recvcontent[8:]
		countcount = int(recvcontent[:2],16)
		recvcontent = recvcontent[2:]
		countlist = list()
		for x in range(0,countcount):
			countlist.append(int(recvcontent[:8],16))
			recvcontent = recvcontent[8:]
		pc.e = copy.copy(self.event)
		totalgoldtake = 0
		totalbuylist = list()
		for x in range(0, len(itemlist)):
			buyid = itemlist[x]
			buycount = countlist[x]
			item = eventobj.createitem(pc, buyid)
			if int(item.price) < 1:
				price = 1
			else:
				price = item.price
			goldtake = int(price) * int(buycount)
			totalgoldtake = totalgoldtake+goldtake
			totalbuylist.append((buyid, buycount))
		if eventobj.takegold(pc, totalgoldtake):
			for x in totalbuylist:
				eventobj.giveitem(pc,x[0],x[1])
	
	def do_0a16(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""トレードキャンセル"""
		print "[ map ]","trade / cancel"
		datatype,datacontent = self.createpacket.create0a19(pc)
		self.send(datatype,datacontent,pc.mapclient,None)
		#if pc.tradestate == 1:
		#	pc.tradestate = -1
		#elif pc.tradestate == -1:
		#	pc.tradestate = 0
		#else:
			#トレード終了通知
			#datatype,datacontent = self.createpacket.create0a1c(pc)
			#self.send(datatype, datacontent, pc.mapclient, None)
		pc.isnpctrade = False
		pc.tradelist = []
		pc.tradestate = 0
		#トレード終了通知
		datatype,datacontent = self.createpacket.create0a1c(pc)
		self.send(datatype, datacontent, pc.mapclient, None)

	def do_0a14(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""トレードのOK状態"""
		print "[ map ]","trade / send ok"
		pc.tradestate = -1

	def do_0a15(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""トレードのTradeを押した際に送信"""
		print "[ map ]","trade / send trade"
		pc.tradestate = 1
		tradereturnlist = list()
		if pc.isnpctrade:
			if pc.tradelist:
				pc.e = copy.copy(self.event)
				for x in pc.tradelist:
					tradereturnlist.append(eventobj.takeitembyiid(pc,x[0],x[1]))
		pc.tradereturnlist = tradereturnlist
		pc.isnpctrade = False
		pc.tradelist = []
		pc.tradestate = 0
		#トレード終了通知
		datatype,datacontent = self.createpacket.create0a1c(pc)
		self.send(datatype, datacontent, pc.mapclient, None)

	def do_0a1b(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""トレードウィンドウに置いたアイテム・金の情報を送信？ """
		print "[ map ]","trade / send item list"
		itemcount = int(recvcontent[:2],16)
		recvcontent = recvcontent[2:]
		iidlist = list()
		for x in range(0,itemcount):
			iidlist.append(int(recvcontent[:8],16))
			recvcontent = recvcontent[8:]
		countcount = int(recvcontent[:2],16)
		recvcontent = recvcontent[2:]
		countlist = list()
		for x in range(0,countcount):
			countlist.append(int(recvcontent[:4],16))
			recvcontent = recvcontent[4:]
		iidlist = map(int, iidlist)
		countlist = map(int, countlist)
		tradelist = zip(iidlist, countlist)
		#tradelist = list()
		#for x in range(0,len(iidlist)):
		#	tradeiid = int(iidlist[x])
		#	tradecount = int(countlist[x])
		#	tradelist.append((tradeiid,tradecount))
		pc.tradelist = tradelist

	def do_0616(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""ショップで売却"""
		print "[ map ]","sell to npcshop"
		itemcount = int(recvcontent[:2],16)
		recvcontent = recvcontent[2:]
		iidlist = list()
		for x in range(0,itemcount):
			iidlist.append(int(recvcontent[:8],16))
			recvcontent = recvcontent[8:]
		countcount = int(recvcontent[:2],16)
		recvcontent = recvcontent[2:]
		countlist = list()
		for x in range(0,countcount):
			countlist.append(int(recvcontent[:8],16))
			recvcontent = recvcontent[8:]
		#print iidlist,countlist
		iidlist = map(int, iidlist)
		countlist = map(int, countlist)
		selllist = zip(iidlist, countlist)
		#selllist = list()
		#for x in range(0,len(iidlist)):
		#	sellid = int(iidlist[x])
		#	sellcount = int(countlist[x])
		#	selllist.append((sellid,sellcount))
		income = 0
		pc.e = copy.copy(self.event)
		for i, c in selllist:
			item = eventobj.takeitembyiid(pc, i, c)
			if item:
				income = income + int(int(item.price) * int(item.count) / 10)
		income = int(income)
		eventobj.givegold(pc, income)

	def do_09f7(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""倉庫を閉じる"""
		pc.warehouse_open = None
		print "[ map ]","close warehouse"

	def do_09fb(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""倉庫から取り出す"""
		iid = int(recvcontent[:8],16)
		count = int(recvcontent[8:12],16)
		print "[ map ]","take item from warehouse", iid, count
		if pc.warehouse_open == None:
			#倉庫から取り出した時の結果#倉庫を開けていません
			datatype, datacontent = self.createpacket.create09fc(-1)
			self.send(datatype, datacontent, pc.mapclient, None)
			raise ValueError, "pc.warehouse_open == None"
		if not pc.warehouse.get(iid):
			#倉庫から取り出した時の結果#指定されたアイテムは存在しません
			datatype,datacontent = self.createpacket.create09fc(-2)
			self.send(datatype, datacontent, pc.mapclient, None)
			raise ValueError, "not pc.warehouse.get(iid)"
		if int(pc.warehouse[iid].count) < int(count):
			#倉庫から取り出した時の結果#指定された数量が不正です
			datatype, datacontent = self.createpacket.create09fc(-3)
			self.send(datatype, datacontent, pc.mapclient, None)
			raise ValueError, "int(pc.warehouse[iid].count) < int(count)"
		pc.e = copy.copy(self.event)
		item = eventobj.takeitembyiid(pc, iid, count, fromwarehouse=True)
		if item:
			eventobj.giveitem(pc, item.id, item.count, fromwarehouse=True)
			#倉庫から取り出した時の結果#成功
			datatype, datacontent = self.createpacket.create09fc(0)
			self.send(datatype, datacontent, pc.mapclient, None)

	def do_09fd(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""倉庫に預ける"""
		iid = int(recvcontent[:8],16)
		count = int(recvcontent[8:12],16)
		print "[ map ]","store item to warehouse", iid, count
		if pc.warehouse_open == None:
			#倉庫に預けた時の結果#倉庫を開けていません
			datatype,datacontent = self.createpacket.create09fe(-1)
			self.send(datatype, datacontent, pc.mapclient, None)
			raise ValueError, "pc.warehouse_open == None"
		if not pc.item.get(iid):
			#倉庫に預けた時の結果#指定されたアイテムは存在しません
			datatype,datacontent = self.createpacket.create09fe(-2)
			self.send(datatype, datacontent, pc.mapclient, None)
			raise ValueError, "not pc.item.get(iid)"
		if int(pc.item[iid].count) < int(count):
			#倉庫に預けた時の結果#指定された数量が不正です
			datatype,datacontent = self.createpacket.create09fe(-3)
			self.send(datatype, datacontent, pc.mapclient, None)
			raise ValueError, "int(pc.item[iid].count) < int(count)"
		pc.e = copy.copy(self.event)
		item = eventobj.takeitembyiid(pc, iid, count)
		if item:
			eventobj.giveitem(pc, item.id, item.count, towarehouse=pc.warehouse_open)
			#倉庫に預けた時の結果#成功
			datatype, datacontent = self.createpacket.create09fe(0)
			self.send(datatype, datacontent, pc.mapclient, None)
	
	def do_0258(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		print "[ map ]","status detail request"
		#ステータス試算結果
		datatype,datacontent = self.createpacket.create0259(pc)
		self.send(datatype, datacontent, pc.mapclient, None)
	
	def do_0f9f(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""攻撃"""
		targetsid = int(recvcontent[:8],16) #攻撃対象のserver id
		if not self.serverobj.enableattackhandle:
			self.attackhandle.attackmob(pc, targetsid)
			return
		if pc.attacking_target == targetsid:
			return
		print "[ map ]", "start attacking mob id", targetsid
		with self.lock_pclist:
			pc.attacking = True
			pc.attacking_target = targetsid
			pc.attacking_delay = pc.status.adelay
	
	def do_0f96(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""攻撃中止？"""
		pc.reset_attack_info()
		#print "[ map ]", "stop attacking"
	
	def do_1387(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""スキル使用"""
		skillid = int(recvcontent[:4], 16)
		targetsid = int(recvcontent[4:12], 16)
		targetx = int(recvcontent[12:14], 16)
		targety = int(recvcontent[14:16], 16)
		skilllv = int(recvcontent[16:18], 16)
		print "[ map ]", "use skill", skillid, "lv", skilllv,
		print "to sid", targetsid, targetx, targety
		if str(int(skillid)) in self.skillhandle.dolist:
			self.skillhandle.run(skillid, pc, skillid, targetsid, \
									targetx, targety, skilllv)
			return
		skill = self.skilldic.get(skillid)
		if skill:
			skillname = str(name.name)
		else:
			skillname = "Unknow"
		#スキル使用通知
		datatype, datacontent = self.createpacket.create1389(pc, skillid, \
											-1, targetx, targety, \
											skilllv, 13, -1)
											#スキルを使用できません
		self.send(datatype, datacontent, pc.mapclient, None)
		#スキル使用通知（スキルを使用できません）
		datatype, datacontent = self.createpacket.create138a(pc, 13)
		self.send(datatype, datacontent, pc.mapclient, None)
		eventobj.systemmessage(pc, "スキル["+skillname+"]は未実装です")

	def do_041a(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""set kanban"""
		pc.kanban = recvcontent[2:-2].decode("hex") #0431313100 -> 313131 -> 111
		datatype, datacontent = self.createpacket.create041b(pc)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
	
	#def do_1d4c(self, pc, data, datalength, recvhead, recvtype, recvcontent):
	#	"""greeting"""
	#	targetsid = int(recvcontent, 16)