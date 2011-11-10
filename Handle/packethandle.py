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
import hashlib
import Socket.rijndael
from Object.itemobj import Item
try:
	import traceback
except ImportError, e:
	print "import error", e
	exceptinfo = sys.exc_info
else:
	exceptinfo = traceback.format_exc
	
class PacketHandle:
	def __init__(self):
		self.dolist = list(set(map(self.rm, dir(self))))
		#dir self to list function ->
		#remove not start from "do_" ->
		#remove duplicate ->
		#transform type "set" to "list"
		self.dolist.remove("")
		#print self.dolist

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
				print "[login]", "packet", s, "packet type didn't define"
		except:
			print "[login]", "error in do /", exceptinfo()
	
	def init(self, serverobj):
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		self.encode = self.cryptio.encode
		self.decode = self.cryptio.decode
		self.pack = self.netio.pack
		self.send = self.netio.send
		self.passtype = list()
		self.passtype.append("000a")#ping
	
	def setpclist(self, pclist):
		self.pclist = pclist
	
	def packet_handle(self, data, datalength, pc):
		try:
			recvhead = data[0:4]
			recvtype = data[4:8]
			recvcontent = data[8:]
			tmp_datalength = int(recvhead, 16) * 2 - 4 # 4 --- recvtype
			tmp_dataadd = recvcontent[tmp_datalength:]
			tmp_datacheck = tmp_dataadd.replace("0","")
			recvcontent = recvcontent[:tmp_datalength]
			if tmp_datacheck != "":
				self.packet_handle(tmp_dataadd, None, pc)
			if recvtype not in self.passtype:
				#print datalength
				print "[login]", recvhead, recvtype, recvcontent
		#datahead = (len(datatype)+len(datacontent)) / 2
		#or datahead = len(data) / 2 - 2
			self.returntype, self.returndata = None, None
			self.do(recvtype, pc, data, datalength, recvhead, recvtype, recvcontent)
		except:
			print "[login]", "error in packet_handle /", exceptinfo()
			self.returntype = None
			self.returndata = None
		return self.returntype, self.returndata
	
	def do_0001(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		clientver = recvcontent[4:16]
		print "[login]", "client version", clientver
		datatype,datacontent = self.createpacket.create0002(clientver)
		self.send(datatype,datacontent,pc.client,None)
		datatype,datacontent = self.createpacket.create001e()
		self.send(datatype,datacontent,pc.client,None)
	
	def do_000a(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		datatype, datacontent = self.createpacket.create000b(recvcontent)
		#print "[login]", "reply ping from client", print datatype, datacontent
		self.send(datatype, datacontent, pc.client, datalength)
	
	def do_001f(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		print "[login]", "receive account and password form client"
		chars = recvcontent.decode("hex")
		account = chars[1:chars.index("\x00")]
		passwordhash = chars[chars.index("\x00")+1:]
		passwordhash = passwordhash[1:passwordhash.rindex("\x00\x06")]
		#print passwordhash.encode("hex")
		print "[login]", account, passwordhash
		if self.pclist.get(account) != None:
			#self.pclist[account].password is a hash from md5
			front_word = str(int("30303030",16))
			back_word = str(int("30303030",16))
			buf = front_word+self.pclist[account].password+back_word
			finallyhash = hashlib.sha1(buf).hexdigest()
			if passwordhash == finallyhash:
				if self.pclist[account].online or self.pclist[account].online_login:
					#既にログインしています
					datatype,datacontent = self.createpacket.create0020("isonline")
					self.send(datatype,datacontent,pc.client,None)
					if self.pclist[account].mapclient != None:
						self.pclist[account].mapclient.transport.loseConnection()
					self.pclist[account].client.transport.loseConnection()
					self.returntype = "isonline"
					self.returndata = self.pclist[account]
				else:
					#認証成功
					datatype,datacontent = self.createpacket.create0020("loginsucess")
					self.send(datatype,datacontent,pc.client,None)
					client = pc.client
					pc = self.pclist[account]
					pc.client = client
					pc.online_login = True
					#reset
					pc.sendmapserver = False
					pc.logout = False
					pc.visible = False
					pc.loginevent = False
					pc.selectresult = None
					pc.motion = 111
					pc.effect = None
					pc.tradestate = 0
					pc.tradelist = None
					pc.tradereturnlist = None
					pc.isnpctrade = False
					pc.warehouse_open = None
					pc.battlestatus = 0
					pc.attacking = False
					pc.attacking_target = None
					pc.attacking_delay = 0
					#reset
					self.returntype = "changepc"
					self.returndata = pc
					#4キャラクターの基本属性
					datatype,datacontent = self.createpacket.create0028(pc)
					self.send(datatype,datacontent,pc.client,None)
					#4キャラクターの装備
					datatype,datacontent = self.createpacket.create0029(pc)
					self.send(datatype,datacontent,pc.client,None)
			else:
				#認証失敗(パスワードが合わない)
				datatype,datacontent = self.createpacket.create0020("loginfaild")
				self.send(datatype,datacontent,pc.client,None)
		else:
			#認証失敗(アカウントが見つからない)
			datatype,datacontent = self.createpacket.create0020("loginfaild")
			self.send(datatype,datacontent,pc.client,None)
	
	def do_00a0(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		print "[login]", "character create"
	
	#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>開始通知と接続先情報
	def do_00a7(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		print "[login]", "character start"
		#print pc.map
		datatype,datacontent = self.createpacket.create00a8(pc, pc.map)
		self.send(datatype,datacontent,pc.client,None)
		self.returntype = "00a8"
	
	def do_0032(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		if not pc.sendmapserver:
			pc.sendmapserver = True
			print "[login]", "mapserver request"
			serveraddress = str(self.serverobj.serveraddress)
			mapserverport = int(self.serverobj.mapserverport)
			datatype,datacontent = self.createpacket.create0033(serveraddress,\
														mapserverport)
			#datatype,datacontent = self.createpacket.create0033("127.0.0.1","13001")
			self.send(datatype,datacontent,pc.client,None)
			self.returntype = "0032"
	
	def do_002a(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		print "[login]", "friend list request, character num:",recvcontent[0:4]
		datatype,datacontent = self.createpacket.create00dd()
		self.send(datatype,datacontent,pc.client,None)
	
	def do_00e6(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		#フレンドリストのマップ更新(自分用) 
		#マップ変更後にゲームサーバーにマップID通知する
		print "[login]", "map change:",recvcontent[0:8]
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<開始通知と接続先情報
	
	def do_00c9(self, pc, data, datalength, recvhead, recvtype, recvcontent):
		"""ウィスパー送信"""
		if not pc.online:
			return
		target_length = int(recvcontent[0:2],16) * 2
		#sample 023100023100 -> 02 * 2 -> 4
		target = recvcontent[2:target_length].decode("hex")
		#sample 023100023100[2:4] -> 31
		recvcontent = recvcontent[target_length+2:]
		#sample 023100023100[6:] = 023100
		text_length = int(recvcontent[0:2],16) * 2
		#sample 023100 -> 02 * 2 -> 4
		text = recvcontent[2:text_length].decode("hex")
		#sample 023100[2:4] -> 31
		sysenc = sys.getfilesystemencoding()
		targetsysenc = target.decode("utf-8").encode(sysenc) 
		textsysenc = text.decode("utf-8").encode(sysenc) 
		#print "[login]", "[wis chat]", targetsysenc, textsysenc
		for p in pc.e.pclist.itervalues():
			if not p.online:
				continue
			if p.name == target:
				datatype, datacontent = self.createpacket.create00ce(pc.name, text)
				self.send(datatype, datacontent, p.client,None)
				print "[login]", "[wis send]", datatype, datacontent
				break
		else: # if no break
			datatype, datacontent = self.createpacket.create00ca(target)
			self.send(datatype, datacontent, pc.client, None)
			print "[login]", "[wis miss]", datatype, datacontent
