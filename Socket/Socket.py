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
	
from twisted.internet.protocol import Protocol,ServerFactory
from twisted.internet import task#,reactor
import os
import socket
import sys
import rijndael
	
class Factory(ServerFactory):
	def __init__(self, serverobj):
		with serverobj.lock_print:
			print "[login]", "listening", serverobj.serveraddress, serverobj.loginserverport
		self.serverobj = serverobj
	def buildProtocol(self, addr):
		print "[login]", "new client accepted"
		return Socket(self.serverobj)
		
class Socket(Protocol):
	def __init__(self, serverobj):
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		#self.thread_recv = {}
		self.packethandle = {}
		self.waitmapserverrequest = False
		self.serverobj.clientlistcount += 1
		self.clientindex = int(self.serverobj.clientlistcount)
		self.serverobj.clientlist[self.clientindex] = PC()
		self.serverobj.clientlist[self.clientindex].name = None
		self.serverobj.clientlist[self.clientindex].client = self
		self.serverobj.packethandle[self.clientindex] = PacketHandle()
		self.serverobj.packethandle[self.clientindex].init(self.serverobj)
		self.serverobj.packethandle[self.clientindex].setpclist(self.pclist)
		self.pc = self.serverobj.clientlist[self.clientindex]
		self.buffer = ""
		self.ecoinit = False
		self.ecorecvkey = False
		self.encode = self.cryptio.encode
		self.decode = self.cryptio.decode
		
	def dataReceived(self, data):
		self.buffer += data.encode("hex")
		#print self.ecoinit,self.ecorecvkey,self.buffer
		while True:
			if not self.buffer:
				break
			if self.ecoinit and not self.ecorecvkey:
				length = int(self.buffer[:8],16) * 2 + 8
			else:
				length = int(self.buffer[:8],16) * 2 + 16
			if length <= len(self.buffer):
				recv = self.buffer[:length]
				self.buffer = self.buffer[length:]
			else:
				print "[login]","error / packet fragmentation",self.buffer
				break
			#recv = self.data.encode("hex")
			#print recv
			#recv_length = int(recv[:8],16) * 2 + 16
			#if len(recv) > recv_length:
			#	print "[login] error on recv length check",recv[recv_length:]
			if not self.ecoinit:
				if recv == "0000000000000010":
					self.ecoinit = True
					sendkeyhead		= "000000000000000131"
					primehead		= "00000100"
					prime			= "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
					serverkeyhead		= "00000100"
					serverkey			= "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
					sendkeypacketdata = sendkeyhead + primehead + prime + serverkeyhead + serverkey
					sendkeypacketdata = sendkeypacketdata.decode("hex")
					self.transport.write(sendkeypacketdata)
				else:
					self.transport.loseConnection()
			elif not self.ecorecvkey:
				if recv == "0000000130":
					self.ecorecvkey = True
				else:
					self.transport.loseConnection()
			else:
				data,datalength = self.decode(recv)
				if data != None:
					returntype,returndata = self.serverobj.packethandle[self.clientindex].packet_handle(data, datalength, self.pc)
					if returntype == "00a8":
						self.waitmapserverrequest = True
						#args = (data,datalength)
						#thread.start_new_thread(self.s00a8,args)
						self.count_s00a8 = 0
						self.timer_s00a8 = task.LoopingCall(self.s00a8, data, datalength)
						self.timer_s00a8.start(1, now=False)
					elif returntype == "0032":
						self.waitmapserverrequest = False
					elif returntype == "changepc":
						self.pc = returndata
						self.serverobj.clientlist[self.clientindex] = returndata
					elif returntype == "isonline":
						print "[login] end on recv_thread"
						self.exitpc(returndata)#
						self.transport.loseConnection()
		else:
			print "[login]","error / no data received"
	
	def connectionMade(self):
		self.transport.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		print "[login]","client connected"#,self
	
	def connectionLost(self, reason):
		self.transport.loseConnection()
		#print self.serverobj.clientlist
		self.exitpc(self.pc)
		del self.serverobj.clientlist[self.clientindex]
		del self.serverobj.packethandle[self.clientindex]
		print "[login]","client disconnected"
	
	def s00a8(self,data,datalength):
		self.count_s00a8 += 1
		if not self.waitmapserverrequest:
			self.timer_s00a8.stop()
		elif self.count_s00a8 >= 5:
			self.timer_s00a8.stop()
		else:
			try:
				self.serverobj.packethandle[self.clientindex].packet_handle(data, datalength, self.pc)
			except Exception,e:
				print "[ map ]","error on s00a8	",e
				self.timer_s00a8.stop()
	
	def exitpc(self, pc):
		#only set on logout
		pc.client = None
		pc.online_login = False
		#reset
		pc.sendmapserver = False
		#save pc data
		if pc.name != None:
			pc.saveallconfig(pc, "UserDB/"+str(pc.account)+".ini")
	
from Handle.packethandle import PacketHandle
from Object.pcobj import PC



