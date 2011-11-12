#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- tab-width: 5 -*-
#Reference ecore
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
#
uselogfile = 0
enableattackhandle = 0
#
print "-----------------------------------------"
print "|\tpyeco 0.51.3 / 2011-11-13\t|"
print "-----------------------------------------"
print "[ all ]", "loading library ...",
import os
import sys
import time
import thread
from twisted.internet import reactor
from twisted.python import threadable
from Object.itemobj import Item
from Object.mapobj import Map
from Object.shopobj import Shop
from Object.npcobj import Npc
from Object.skillobj import Skill
from Object.serverobj import Server
from Object.pcobj import PC
from Object.mobobj import Mob
from Handle.eventhandle import EventHandle
from Handle.mobhandle import MobHandle
from Handle.attackhandle import AttackHandle
from Handle.commandhandle import Command
from Handle.createpacket import CreatePacket
from Handle.consts import const
from Handle.skillhandle import SkillHandle
from Socket.cryptio import CryptIO
from Socket.netio import NetIO
from Socket.Socket import Factory
from Socket.Socket_map import Factory_Map
from Socket.webserver import WebServer
print "over"

def thread_savepcdata(pclist, lock_print, lock_pclist):
	"""save online player data every 60 sec"""
	with lock_print: #lock_print.acquire()	...	lock_print.release()
		print "[ all ]", "start thread_savepcdata"
	while True:
		try:
			with lock_pclist:
				for p in pclist.itervalues():
					if not p.online:
						continue
					p.saveallconfig("UserDB/%s.ini"%p.account)
			time.sleep(60)
		except KeyboardInterrupt:
			print "[ all ]", "thread_savepcdata end"
			break
		except:
			print "[timer]", "timer_savepcdata error", sys.exc_info()

def create_global_serverobj():
	global global_serverobj
	global_serverobj = Server()
	print "[ all ]", "loading server config ...",
	global_serverobj.loadallconfig("server.ini")
	print "over"

def create_global_itemdic():
	global global_itemobj
	global global_itemdic
	global_itemobj = Item()
	print "[ all ]", "loading item database ...",
	itemcsv = "/Database/item.csv"
	global_itemdic = global_itemobj.getitemdic(os.getcwd()+itemcsv)
	print "over", "	", len(global_itemdic), "	item load"

def create_global_mapdic():
	global global_mapobj
	global global_mapdic
	global_mapobj = Map()
	print "[ all ]", "loading map database ...",
	global_mapdic = global_mapobj.getmapdic(os.getcwd()+"/Database/map.csv")
	print "over", "	", len(global_mapdic), "	map load"

def create_global_shopdic():
	global global_shopobj
	global global_shopdic
	global_shopobj = Shop()
	print "[ all ]", "loading shop database ...",
	global_shopdic = global_shopobj.getshopdic(os.getcwd()+"/Database/shop.csv")
	print "over", "	", len(global_shopdic), "	shop load"

def create_global_npcdic():
	global global_npcobj
	global global_npcdic
	global_npcobj = Npc()
	print "[ all ]","loading npc database ...",
	global_npcdic = global_npcobj.getnpcdic(os.getcwd()+"/Database/npc.csv")
	print "over", "	", len(global_npcdic), "	npc load"

def create_global_skilldic():
	global global_skillobj
	global global_skilldic
	global_skillobj = Skill()
	print "[ all ]","loading skill database ...",
	global_skilldic = global_skillobj.getskilldic(os.getcwd()+"/Database/skill.csv")
	print "over	", len(global_skilldic), "	skill load"

def create_global_mobdic():
	global global_mobobj
	global global_mobdic
	global_mobobj = Mob()
	print "[ all ]","loading mob database ...",
	global_mobdic = global_mobobj.getmobdic(os.getcwd()+"/Database/mob.csv")
	print "over", "	", len(global_mobdic), "	mob load"

def create_global_eventhandle():
	global global_eventhandle
	global_eventhandle = EventHandle()
	print "[ all ]","loading script ...",
	global_eventhandle.loadscript(os.getcwd()+"/Script")
	print "over", "	", len(global_eventhandle.scriptdic), "	event load"

def create_global_skillhandle():
	global global_skillhandle
	global_skillhandle = SkillHandle()

def create_global_attackhandle():
	global global_attackhandle
	global_attackhandle = AttackHandle()

def create_global_lock():
	from threading import RLock
	global global_lock_print
	global global_lock_pclist
	global global_lock_moblist
	global_lock_print = RLock()
	global_lock_pclist = RLock()
	global_lock_moblist = RLock()

def create_global_cryptio():
	global global_cryptio
	global_cryptio = CryptIO()

def create_global_netio():
	global global_netio
	global_netio = NetIO()
	global_netio.init(global_cryptio)

def create_global_createpacket():
	global global_createpacket
	global_createpacket = CreatePacket()

def create_global_commandio():
	global global_commandio
	global_commandio = Command()

def create_pclist():
	global pclist
	pclist = {}
	print "[ all ]","loading pclist ...",
	for a, b, c in os.walk(os.getcwd() + "/UserDB"):
		for x in c:
			if len(str(x)) > 4 and x[-4:] == ".ini":
				pclist[x[:-4]] = None
	for name in pclist:
		pclist[name] = PC(global_itemobj, global_itemdic)
		pclist[name].loadallconfig("UserDB/%s.ini"%name)
		pclist[name].account = name
	print "over", "	", len(pclist), "	pc load"

def create_moblist():
	global moblist
	moblist = {}

def init_attackhandle():
	global_attackhandle.init(global_serverobj)

def init_skillhandle():
	global_skillhandle.init(global_serverobj)

def init_createpacket():
	global_createpacket.init(global_serverobj)

def init_loginserver():
	global factory
	loginserverport = int(global_serverobj.loginserverport)
	factory = Factory(global_serverobj)
	reactor.listenTCP(loginserverport, factory)

def init_mapserver():
	global factory_map
	mapserverport = int(global_serverobj.mapserverport)
	factory_map = Factory_Map(global_serverobj)
	reactor.listenTCP(mapserverport, factory_map)

def init_webserver():
	global webserver
	webserver = WebServer()
	webserver.create_listen_thread(global_serverobj)

def exec_thread():
	global global_mobhandle
	thread.start_new_thread(thread_savepcdata, (pclist, \
					global_lock_print, global_lock_pclist))
	global_mobhandle = MobHandle(global_serverobj)
	thread.start_new_thread(global_mobhandle.thread_mobhandle, ())
	if enableattackhandle:
		thread.start_new_thread(global_attackhandle.thread_attackhandle, ())
	time.sleep(0.1)

def setlibdic_serverobj():
	libdic = {"lock_print"	:	global_lock_print,
			"lock_pclist"	:	global_lock_pclist,
			"lock_moblist"	:	global_lock_moblist,
			"itemobj"		:	global_itemobj,
			"itemdic"		:	global_itemdic,
			"mapdic"		:	global_mapdic,
			"eventhandle"	:	global_eventhandle,
			"shopdic"		:	global_shopdic,
			"npcdic"		:	global_npcdic,
			"serverobj"	:	global_serverobj, #self
			"pclist"		:	pclist,
			"moblist"		:	moblist,
			"skilldic"	:	global_skilldic,
			"mobdic"		:	global_mobdic,
			"cryptio"		:	global_cryptio,
			"netio"		:	global_netio,
			"createpacket"	:	global_createpacket,
			"commandio"	:	global_commandio,
			"const"		:	const,
			"skillhandle"	:	global_skillhandle,
			"attackhandle"	:	global_attackhandle,
			}
	global_serverobj.setlibdic(libdic)
	global_serverobj.enableattackhandle = enableattackhandle

def exit_pyeco():
	for x in pclist:
		#print pclist[x].online
		if pclist[x].online:
			pclist[x].saveallconfig("UserDB/%s.ini"%pclist[x].account)
	try:
		null = open("/dev/null", "r")
	except:
		#print "current system is windows"
		from ctypes import windll
		kernel32 = windll.LoadLibrary("kernel32.dll")
		process = kernel32.OpenProcess(1, False,os.getpid())
		if process:
			kernel32.TerminateProcess(process, 0)
		else:
			print "[ all ]","error on process terminate"
	else:
		#print "current system is linux"
		import signal
		os.kill(os.getpid(), signal.SIGKILL)

class Log:
	def __init__(self):
		self.logtime = True
	def write(self, s):
		stdout.write(s)
		stdout.flush()
		if not uselogfile:
			return
		if self.logtime:
			logfile.write(time.strftime("[%y-%m-%d %H:%M:%S]", time.localtime())+" "+s)
		else:
			logfile.write(s)
		self.logtime = False
		if s[-1] != "\n":
			return
		logfile.flush()
		self.logtime = True
	def flush(self):
		stdout.flush()
		if uselogfile:
			logfile.flush()

if __name__ == "__main__":
	os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
	#thread.stack_size(256*1024)
	threadable.init() #twisted.python.threadable
	stdout = sys.stdout
	if uselogfile:
		logfile = file("pyeco.log", "a")
		logfile.write("-"*30+" pyeco start "+"-"*30+"\n")
	sys.stdout = Log()
	create_global_serverobj() # a class
	create_global_itemdic() # key: int item id
	create_global_mapdic() # key: int map id
	create_global_shopdic() # key: int shop id
	create_global_npcdic() # key: int npc id
	create_global_skilldic() # key: int skill id
	create_global_mobdic() # key: int mob id
	create_global_eventhandle() # load script
	create_global_cryptio()
	create_global_netio() # need global_netio
	create_global_createpacket()
	create_global_commandio()
	create_global_skillhandle()
	create_global_attackhandle()
	create_global_lock() #thread lock
	create_pclist() # key: str account name
	create_moblist() # key: int mob server id
	setlibdic_serverobj() # set itemdic, mapdic, etc... in serverobj
	init_createpacket() # createpacket.init
	init_skillhandle() # skillhandle.init
	init_attackhandle() # attackhandle.init
	exec_thread() # exec thread
	init_loginserver() # reactor.listenTCP
	init_mapserver() # reactor.listenTCP
	init_webserver() # reactor.listenTCP
	reactor.run() # blocking
	exit_pyeco() # save online player data and kill self pid