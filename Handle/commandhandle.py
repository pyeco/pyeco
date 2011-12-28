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
from Object import eventobj
import sys
import os
import traceback

def splitcommand(openchattext):
	inputtext = str(openchattext).split(" ")
	while True:
		try:
			inputtext.remove("")
		except:
			break
	return inputtext
	
def simplehandle(pc, openchattext, commandstr, commandhint=None, errormessage=None, args=1, extra=False):
	# if errormessage, args must be number
	# if commandhint, args > 1; else, args = 1 (like "!help")
	arg = None
	if pc.e.serverobj.gmlevel.get(commandstr) == None:
		eventobj.systemmessage(pc,"gmlevel[%s] not defined"%(commandstr, ))
	elif int(pc.gmlevel) < int(pc.e.serverobj.gmlevel[commandstr]):
		eventobj.systemmessage(pc, "access denied")
	elif not commandhint:
		arg = True
	else:
		command = splitcommand(openchattext)
		try:
			if args < 1:
				args = 1
			if len(command) <= args:
				print "[ map ]", commandhint
				eventobj.systemmessage(pc, commandhint)
				raise Exception
			if args == 1 and not extra:
				if errormessage:
					arg = str(int(command[1]))
				else:
					arg = str(command[1])
			else:
				arg = command
				if errormessage:
					for x in range(0, len(arg)):
						if x == 0:
							continue
						arg[x] = str(int(arg[x]))
		except ValueError:
			arg = None
			print "[ map ]", errormessage, command[1:]
			eventobj.systemmessage(pc, str(errormessage)+" "+str(command[1:]))
		except Exception:
			arg = None
	return arg





class Command:
	def __init__(self):
		self.dolist = list(set(map(self.rm, dir(self))))
		#dir self to list function ->
		#remove not start from "do_" ->
		#remove duplicate ->
		#transform type "set" to "list"
		self.dolist.remove("")
		#print self.dolist
		self.sysenc = sys.getfilesystemencoding()
	
	def rm(self, s):
		if s[:3] == "do_":
			return s[3:]
		else:
			return ""
	
	def do(self, s, *args):
		try:
			if s in self.dolist:
				eval("self.do_"+s)(*args)
				return True
			else:
				return False
		except:
			print "[ cmd ]", "error in do /", traceback.format_exc()
			return False
	
	def run(self, pc, openchattext):
		try:
			openchattext = str(openchattext)
			commandtype = splitcommand(openchattext)[0]
			if commandtype[0] == "!":
				commandtype = "0"+commandtype[1:] #replace ! to 0
			if commandtype[0] == "/":
				commandtype = "1"+commandtype[1:] #replace / to 1
			iscommand = self.do(commandtype, pc, openchattext)
		except:
			print "[ cmd ]", "error in run /", traceback.format_exc()
			iscommand = False
		return iscommand
	
	def do_0help(self, pc, openchattext):
		eventobj.systemmessage(pc, "---------------------------------------")
		eventobj.systemmessage(pc, "!help")
		eventobj.systemmessage(pc, "　!commandlist")
		eventobj.systemmessage(pc, "!user")
		eventobj.systemmessage(pc, "　/user")
		eventobj.systemmessage(pc, "/dustbox")
		eventobj.systemmessage(pc, "!reloadscript")
		eventobj.systemmessage(pc, "!printitem")
		eventobj.systemmessage(pc, "!shop shop_id")
		eventobj.systemmessage(pc, "!wh warehouse_id")
		eventobj.systemmessage(pc, "!servermessage servermessage")
		eventobj.systemmessage(pc, "　!sm servermessage")
		eventobj.systemmessage(pc, "!item item_id <count>")
		eventobj.systemmessage(pc, "　!giveitem item_id <count>")
		eventobj.systemmessage(pc, "!gold num")
		eventobj.systemmessage(pc, "　!updategold num")
		eventobj.systemmessage(pc, "!takeitem item_id <count>")
		eventobj.systemmessage(pc, "!countitem item_id")
		eventobj.systemmessage(pc, "!event event_id")
		eventobj.systemmessage(pc, "!warp map_id ( x y )")
		eventobj.systemmessage(pc, "!warpraw map_id ( x y )")
		eventobj.systemmessage(pc, "!hair hair_id")
		eventobj.systemmessage(pc, "!haircolor haircolor_id")
		eventobj.systemmessage(pc, "　!hc haircolor_id")
		eventobj.systemmessage(pc, "!face face_id")
		eventobj.systemmessage(pc, "!wig wig_id")
		eventobj.systemmessage(pc, "!ex ex_id")
		eventobj.systemmessage(pc, "!wing wing_id")
		eventobj.systemmessage(pc, "!wingcolor wingcolor_id")
		eventobj.systemmessage(pc, "　!wc wingcolor_id")
		eventobj.systemmessage(pc, "!motion motion_id")
		eventobj.systemmessage(pc, "!effect effect_id")
		eventobj.systemmessage(pc, "!speed num")
		eventobj.systemmessage(pc, "!sell")
		eventobj.systemmessage(pc, "!mob mobid")
		eventobj.systemmessage(pc, "!killallmob")
		eventobj.systemmessage(pc, "---------------------------------------")
	
	def do_0commandlist(self, pc, openchattext):
		self.do_0help(pc, openchattext)
	
	def do_0item(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "giveitem", "!item item_id <count>", "giveitem id or count not a number",args=1,extra=True)
		if arg:
			inputid = arg[1]
			if len(arg) >= 3:
				inputcount = arg[2]
			else:
				inputcount = 1
			eventobj.giveitem(pc, int(inputid), int(inputcount))
	
	def do_0giveitem(self, pc, openchattext):
		self.do_0item(pc, openchattext)
	
	def do_0takeitem(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "takeitem", "!takeitem item_id <count>", "takeitem id or count not a number",args=1,extra=True)
		if arg:
			inputid = arg[1]
			if len(arg) >= 3:
				inputcount = arg[2]
			else:
				inputcount = 1
			eventobj.takeitem(pc, int(inputid), int(inputcount))
	
	def do_0warpraw(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "warpraw", "!warpraw map_id x y", "warpraw mapid or x or y not a number", args=1, extra=True)
		if arg:
			if len(arg) == 3:
				eventobj.systemmessage(pc, "!warpraw map_id ( rawx rawy )")
			else:
				mapid = arg[1]
				if len(arg) >= 4:
					rawx = arg[2]
					rawy = arg[3]
					print "[ map ]", "warpraw command", mapid, rawx, rawy
					eventobj.warpraw(pc, mapid, rawx, rawy)
				else:
					mapinfo = pc.e.mapdic.get(int(mapid))
					if mapinfo != None:
						x = int(mapinfo.centerx)
						y = int(mapinfo.centery)
					else:
						x, y = 128, 128
					print "[ map ]", "warpraw -> warp command", mapid, x, y
					eventobj.warp(pc, int(mapid), int(x), int(y))
	
	def do_0warp(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "warp", "!warp map_id ( x y )", "warp mapid or x or y not a number", args=1, extra=True)
		if arg:
			if len(arg) == 3:
				eventobj.systemmessage(pc, "!warp map_id ( x y )")
			else:
				mapid = arg[1]
				if len(arg) >= 4:
					x = arg[2]
					y = arg[3]
				else:
					mapinfo = pc.e.mapdic.get(int(mapid))
					if mapinfo != None:
						x = int(mapinfo.centerx)
						y = int(mapinfo.centery)
					else:
						x, y = 128, 128
				print "[ map ]", "warp command", mapid, x, y
				eventobj.warp(pc, int(mapid), int(x), int(y))
	
	def do_0user(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "user")
		if arg:
			print "[ map ]", "get online player list"
			count = 0
			for p in pc.e.pclist.itervalues():
				if p.online:
					count += 1
					mapinfo = pc.e.mapdic.get(int(p.map))
					if mapinfo != None:
						mapname = mapinfo.name
					else:
						mapname = str(p.map)
					pcname = str(p.name)
					message = pcname+" "+"["+mapname+"]"
					eventobj.systemmessage(pc, message)
			message = "online player"+" "+str(count)
			eventobj.systemmessage(pc, message)
	
	def do_1user(self, pc, openchattext):
		self.do_0user(pc, openchattext)
	
	def do_0reloadscript(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "reloadscript")
		if arg:
			print "[ map ]", "reloading script ...",
			eventobj.servermessage(pc, "reloading script", True) #fast = True
			pc.e.eventhandle.loadscript(os.getcwd() + "/Script")
			print "over"
			eventobj.servermessage(pc, "over")
	
	def do_1dustbox(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "dustbox")
		if arg:
			print "[ map ]", "call npc trade",
			pc.e.id = 12000170
			pc.e.eventhandle.run(pc)
	
	def do_0printitem(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "printitem")
		if arg:
			itemlist = pc.sort.item
			equiplist = pc.equiplist()
			for x in itemlist:
				x = int(x)
				if x == 0:
					continue
				if x in equiplist:
					continue
				msg = "printitem %s %s" % (pc.item[x].id, \
					str(pc.item[x].name).decode("utf-8").encode(self.sysenc))
				msgforeco = "printitem "+str(pc.item[x].id)+" "+str(pc.item[x].name)
				print "[ map ]", msg
				eventobj.systemmessage(pc, msgforeco)
	
	def do_0where(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "whereraw")
		if arg:
			mapinfo = pc.e.mapdic.get(int(pc.map))
			if mapinfo != None:
				mapname = mapinfo.name
			else:
				mapname = str(pc.map)
			eventobj.systemmessage(pc, "%s [%s] (%s, %s) r(%s, %s)"%(mapname, \
									pc.map, pc.x, pc.y, pc.rawx, pc.rawy))
	
	def do_0sell(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "sell")
		if arg:
			eventobj.npcsell(pc)
	
	def do_0servermessage(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "servermessage", "!sm servermessage")
		if arg:
			eventobj.servermessage(pc, arg)
	
	def do_0sm(self, pc, openchattext):
		self.do_0servermessage(pc, openchattext)
	
	def do_0shop(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "shop", "!shop shop_id", "shop id not a number")
		if arg:
			eventobj.npcshop(pc, int(arg))
	
	def do_0warehouse(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "warehouse", "!wh warehouse_id", "warehouse id not a number")
		if arg:
			eventobj.warehouse(pc, int(arg))
	
	def do_0wh(self, pc, openchattext):
		self.do_0warehouse(pc, openchattext)
	
	def do_0countitem(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "countitem", "!countitem item_id", "countitem id not a number")
		if arg:
			itemcount = eventobj.countitem(pc, int(arg))
			msg = "count item %s %s"%(arg, itemcount)
			print "[ map ]", msg
			eventobj.systemmessage(pc, msg)
	
	def do_0updategold(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "updategold", "!gold num", "gold input not a number")
		if arg:
			if int(arg) >= 0 and int(arg) <= 1000000000:
				eventobj.updategold(pc, int(arg))
			#持ゴールド上限 99999999 #銀行への預かり上限 1000000000
	
	def do_0gold(self, pc, openchattext):
		self.do_0updategold(pc, openchattext)
	
	def do_0event(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "event", "!event event_id", "event id not a number")
		if arg:
			pc.e.id = int(arg)
			print "[ map ]", "event start from command",pc.e.id
			pc.e.eventhandle.run(pc)
	
	def do_0hair(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "hair", "!hair hair_id", "hair id not a number")
		if arg:
			pc.hair = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0haircolor(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "hc", "!hc haircolor_id", "haircolor id not a number")
		if arg:
			pc.haircolor = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0hc(self, pc, openchattext):
		self.do_0haircolor(pc, openchattext)
	
	def do_0face(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "face", "!face face_id", "face id not a number")
		if arg:
			pc.face = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0wig(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "wig", "!wig wig_id", "wig id not a number")
		if arg:
			pc.wig = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0ex(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "ex", "!ex ex_id", "ex id not a number")
		if arg:
			pc.ex = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0wing(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "wing", "!wing wing_id", "wing id not a number")
		if arg:
			pc.wing = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0wingcolor(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "wc", "!wc wingcolor_id", "wingcolor id not a number")
		if arg:
			pc.wingcolor = int(arg)
			#eventobj.updatepc(pc)
	
	def do_0wc(self, pc, openchattext):
		self.do_0wingcolor(pc, openchattext)
	
	def do_0motion(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "motion", "!motion motion_id", "motion id not a number")
		if arg:
			eventobj.motion(pc, int(arg), True)
	
	def do_0effect(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "effect", "!effect motion_id", "effect id not a number")
		if arg:
			eventobj.effect(pc, int(arg))
	
	def do_0speed(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "speed", "!speed num", "speed input not a number")
		if arg:
			eventobj.speed(pc, int(arg))
	
	def do_0mob(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "mob", "!mob mobid", "mob id not a number")
		if arg:
			eventobj.mob(pc, int(arg))
	
	def do_0killallmob(self, pc, openchattext):
		arg = simplehandle(pc, openchattext, "killallmob")
		if arg:
			eventobj.killallmob(pc)
	
	def do_0dropitem(self, pc, openchattext):
		pass
	
	def do_0skill(self, pc, openchattext):
		pass
	
	def do_0clearskill(self, pc, openchattext):
		pass