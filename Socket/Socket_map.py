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
from DataAccessControl import DataAccessControl
from twisted.internet.protocol import Protocol, ServerFactory
from Handle.packethandle_map import PacketHandle_Map
from Object.pcobj import PC
import os
import socket
import sys
import rijndael
DIRECT_WRITE_NAME = ["connected",
				"transport",
				]

class Factory_Map(ServerFactory):
	def __init__(self, serverobj):
		with serverobj.lock_print:
			print "[ map ]", "listening", serverobj.serveraddress, serverobj.mapserverport
		self.serverobj = serverobj
	def buildProtocol(self, addr):
		print "[ map ]", "new client accepted"
		return Socket_Map(self.serverobj)

class Socket_Map(Protocol, DataAccessControl):
	def __init__(self, serverobj):
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		self.add("packethandle_map", {})
		self.serverobj.clientlistcount_map += 1
		self.add("clientindex", int(self.serverobj.clientlistcount_map))
		self.serverobj.clientlist_map[self.clientindex] = PC(self.itemobj, self.itemdic)
		self.serverobj.clientlist_map[self.clientindex].name = ""
		self.serverobj.clientlist_map[self.clientindex].mapclient = self
		self.serverobj.packethandle_map[self.clientindex] = PacketHandle_Map()
		self.serverobj.packethandle_map[self.clientindex].init(self.serverobj)
		self.add("pc", self.serverobj.clientlist_map[self.clientindex])
		self.add("buffer", "")
		self.add("ecoinit", False)
		self.add("ecorecvkey", False)
		self.add("encode", self.cryptio.encode)
		self.add("decode", self.cryptio.decode)
	
	def __setattr__(self, name, value):
		if name in DIRECT_WRITE_NAME:
			self.__dict__[name] = value
		else:
			DataAccessControl.__setattr__(self, name, value)
	
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
				print "[ map ]","error / packet fragmentation",self.buffer
				break
			#recv = self.data.encode("hex")
			#print recv
			#recv_length = int(recv[:8],16) * 2 + 16
			#if len(recv) > recv_length:
			#	print "[ map ] error on recv length check",recv[recv_length:]
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
					returntype,returndata = self.serverobj.packethandle_map[self.clientindex].packet_handle(data, datalength, self.pc)
					if returntype == "changepc":
						self.pc = returndata
						self.serverobj.clientlist_map[self.clientindex] = returndata
					elif returntype == "accountnotfound":
						self.transport.loseConnection()
		else:
			print "[ map ]","error / no data received"
	
	def connectionMade(self):
		self.transport.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		print "[ map ]","client connected"#,self
	
	def connectionLost(self, reason):
		self.transport.loseConnection()
		#print self.serverobj.clientlist_map
		self.serverobj.packethandle_map[self.clientindex].packet_handle("0003001eff", None, self.pc)
		self.exitpc(self.pc)
		del self.serverobj.clientlist_map[self.clientindex]
		del self.serverobj.packethandle_map[self.clientindex]
		print "[ map ]","client disconnected"
	
	def exitpc(self, pc):
		#only set on logout
		pc.mapclient = None
		pc.online = False
		#reset
		pc.sendmapserver = False
		pc.logout = False
		pc.visible = False
		pc.loginevent = False
		pc.selectresult = None
		pc.motion = 111
		pc.effect = None
		pc.tradestate = 0
		pc.tradelist = []
		pc.tradereturnlist = []
		pc.isnpctrade = False
		pc.warehouse_open = None
		pc.battlestatus = 0
		pc.attacking = False
		pc.attacking_target = None
		pc.attacking_delay = 0
		pc.pet = None
		pc.kanban = ""