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
import sys
import os
import time
import thread
from Object.eventobj import *
import traceback

class EventHandle(DataAccessControl):
	def __init__(self):
		self.add("scriptdic", {})
		self.add("removelist", [])
	
	def loadscript(self, scriptpath):
		scriptfilelist = []
		self.scriptdic = {}
		for a,b,c in os.walk(scriptpath):
			#a:path c:filenamelist
			for x in c:
				if x[:4] == "tmp_":
					os.remove(a+"/"+x)
					continue
				path = os.path.join(a, x)
				if x[-3:] == ".py" and path not in scriptfilelist:
					scriptfilelist.append(path)
		for scriptfile in scriptfilelist:
			try:
				f = open(scriptfile, "rb")
				code = f.read().replace("\r\n", "\n").replace("\r", "\n")
				execobj = compile(code+"\n", "", "exec")
				f.close()
				namespace_tmp = {}
				scriptclass_tmp = None
				exec execobj in namespace_tmp
				scriptclass_tmp = namespace_tmp["Script"]()
				for eventid in map(int, scriptclass_tmp.get_id()):
					if self.scriptdic.get(eventid):
						print "[ all ]", "event id existed [%s, %s]" % (eventid, scriptfile)
						continue
					self.scriptdic[eventid] = scriptclass_tmp
					#self.scriptdic[eventid] = namespace_tmp["Script"]()
					#self.scriptdic[eventid].get_id() #init
			except:
				print "[ all ]", "script load error [%s]\n" % (scriptfile, ), traceback.format_exc()
				continue
	
	"""def loadscript_old(self, scriptpath):
		l = {}
		for a,b,c in os.walk(scriptpath):
			for x in c:
				if x[:4] == "tmp_":
					os.remove(a+"/"+x)
					continue
				if x[-3:] == ".py" and l.get(x[:-3]) == None:
					l[x[:-3]] = a
				#elif x[-4:] == ".pyc" and l.get(x[:-4]) == None:
				#		l[x[:-4]] = a
		d = list()
		self.scriptdic = {}
		self.removelist = list()
		index = 0
		for x in l:
			filename = x+".py"
			loaderror = False
			#print x,l[x]
			try:
				d.index(l[x])
			except:
				d.append(l[x])
				sys.path.append(l[x])
			try:
				del sys.modules[str(x)]
			except:
				pass
			try:
				exec("import "+x)
				#exec(x+" = eval(\"__import__\")(x)")
			except SyntaxError:
				index =index+1
				open(l[x]+"/tmp_"+str(index)+".py", "wb").write(open(l[x]+"/"+str(x)+".py", "rb").read())
				removelistpy = l[x]+"/tmp_"+str(index)+".py"
				removelistpyc = l[x]+"/tmp_"+str(index)+".pyc"
				self.removelist.append(removelistpy)
				self.removelist.append(removelistpyc)
				x = "tmp_"+str(index)
				try:
					del sys.modules[str(x)]
				except:
					pass
				try:
					exec("import "+x)
				except:
					print "\n[ all ]","script reload error [", filename, "]", traceback.format_exc(),
					loaderror = True
			if loaderror:
				continue
			try:
				exec("s = "+x+".Script()")
			except AttributeError,e:
				print "[ all ]", "\nscript load error, try rename script [", filename, "]" ,
				continue
			for i in s.get_id():
				exec("self.event_"+i+"=s")
				if self.scriptdic.get(int(i)) != None:
					print "\n[ all ]", "the same event id existed [", filename, "]",
				else:
					exec("self.scriptdic[int(i)] = self.event_"+i)
		if self.removelist:
			for x in self.removelist:
				try:
					if os.path.isfile(x):
						os.remove(x)
				except:
					print "[ all ]","\nfile remove failed [",x,"]","""
	
	def run_thread(self,pc):
		#イベント開始の通知
		datatype,datacontent = pc.e.createpacket.create05dc()
		pc.e.send(datatype, datacontent, pc.mapclient, None)
		#EventID通知。 Event送信に対する応答
		datatype,datacontent = pc.e.createpacket.create05e8(pc.e.id)
		pc.e.send(datatype, datacontent, pc.mapclient, None)
		#pc.e.id = str(pc.e.id).zfill(8)
		eventid = int(pc.e.id)
		eventobj = self.scriptdic.get(eventid)
		if eventobj != None:
			try:
				#exec("self.event_"+pc.e.id+".main(pc)")
				eventobj.main(pc)
			except:
				print"[ map ]", "script error", traceback.format_exc()
		else:
			print "[ map ]", "event", pc.e.id, "not found"
			say(pc, "未実装$RID %s"%(pc.e.id, ), "", 0)
		#イベント終了の通知
		datatype,datacontent = pc.e.createpacket.create05dd()
		pc.e.send(datatype, datacontent, pc.mapclient, None)
	
	def run(self,pc):
		args = (pc,)
		thread.start_new_thread(self.run_thread, args)
