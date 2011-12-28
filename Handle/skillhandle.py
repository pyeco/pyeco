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
import sys
import os
import time
import thread
from Object import eventobj
import traceback

class SkillHandle:
	def __init__(self):
		self.dolist = list(set(map(self.rm, dir(self))))
		#dir self to list function ->
		#remove not start from "do_" ->
		#remove duplicate ->
		#transform type "set" to "list"
		self.dolist.remove("")
		#print self.dolist
		self.sysenc = sys.getfilesystemencoding()
	
	def init(self, serverobj):
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		self.except_count = 0
		self.send = self.netio.send
		self.sendmap = self.netio.sendmap
		self.sendmapwithoutself = self.netio.sendmapwithoutself
		self.sendserver = self.netio.sendserver
		#self.oldtime = time.time()
	
	def rm(self, s):
		if s[:3] == "do_":
			return s[3:]
		else:
			return ""
	
	def do(self, s, *args):
		s = str(s)
		try:
			if s in self.dolist:
				eval("self.do_"+s)(*args)
				return True
			else:
				return False
		except:
			print "[skill]", "error in do /", traceback.format_exc()
	
	def run(self, *args):
		try:
			s = str(int(args[0]))
			print "[skill]", "run %s" % (s, )
			thread.start_new_thread(self.do, args)
		except:
			print "[skill]", "error in run /", traceback.format_exc()
		
	def do_10100(self, pc, skillid, targetsid, targetx, targety, skilllv):
		"""受け取れ
		対象者のH.E.ARTレベルを、1つ上昇させる"""
		cast = 500
		#スキル使用通知
		#print "targetsid", targetsid
		datatype,datacontent = self.createpacket.create1389(pc, skillid, \
											targetsid, targetx, targety, \
											skilllv, 0, cast)
											# 0 = エラーなし
		self.send(datatype, datacontent, pc.mapclient, None, True) #nodelay
		time.sleep(cast/1000.0)
		#スキル使用結果通知（対象：単体）
		datatype, datacontent = self.createpacket.create1392(pc, (targetsid,), \
										 skillid, skilllv)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		#戦闘状態変更通知
		datatype,datacontent = self.createpacket.create0fa6(pc, 0)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		datatype,datacontent = self.createpacket.create0fa6(pc, 1)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		eventobj.systemmessage(pc, "スキル[受け取れ]は完全に実装されていません")
	
	def do_3054(self, pc, skillid, targetsid, targetx, targety, skilllv):
		"""ヒーリング
		対象のHPを回復する"""
		cast = 500
		#スキル使用通知
		#print "targetsid", targetsid
		datatype,datacontent = self.createpacket.create1389(pc, skillid, \
											targetsid, targetx, targety, \
											skilllv, 0, cast)
		self.send(datatype, datacontent, pc.mapclient, None, True) #nodelay
		time.sleep(cast/1000.0)
		#スキル使用結果通知（対象：単体）
		datatype, datacontent = self.createpacket.create1392(pc, (targetsid,), \
										 skillid, skilllv, (-100,))
										 #マイナス = 回復
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		#戦闘状態変更通知
		datatype,datacontent = self.createpacket.create0fa6(pc, 0)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		datatype,datacontent = self.createpacket.create0fa6(pc, 1)
		self.sendmap(datatype, datacontent, self.pclist, pc, None)
		eventobj.systemmessage(pc, "スキル[ヒーリング]は完全に実装されていません")