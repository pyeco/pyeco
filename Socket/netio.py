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
import os
import socket
import sys
import rijndael
from cryptio import CryptIO
import traceback

class NetIO(DataAccessControl):
	def init(self, cryptio):
		self.add("cryptio", cryptio)
		self.add("encode", self.cryptio.encode)
		self.add("decode", self.cryptio.decode)
	
	def calc_data_head(self, datatype, datacontent):
		try:
			datahead = (len(datatype)+len(datacontent))/2.0
			datahead = hex(int(datahead))
			if len(datahead) < 3:
				print "error on clac_data_head: data too short"
				return"0000"
			if len(datahead) > 6:
				print "error on clac_data_head: data too long"
				return"0000"
			datahead = datahead[2:]
			datahead = datahead.zfill(4)
			#while len(datahead) < 4:
			#	datahead = "0"+datahead
		except Exception:
			print "[netio]","error on calc_data_head /", traceback.format_exc()
			datahead = "0000"
		return datahead
	
	def packstr(self, string):
		try:
			string = str(string)
			if string == "":
				return "0100"
			string = string.encode("hex")+"00"
			stringhead = self.pack(len(string)/2, 2)
			result = stringhead+string
		except Exception:
			print "[netio]","error on packstr /", traceback.format_exc()
			result = "0100"
		return result
	
	def pack(self, data, length):
		try:
			if data == True:
				data = "01"
			if data == False or data == None:
				data = "00"
			if len(str(data)) > 1:
				if str(data)[:1] == "-":
					data = 256 - int(str(data)[1:])
					data = hex(data)[2:]
					data = "f"*(length-len(data)) + data
					#print "[debug]", data
					return data
			if data != None:
				data = int(data)
				data = hex(data)
				data = str(data)
			else:
				print "[netio]","some data equal None"
				data = ""
			if len(data) < 3:
				print "[netio]","error on datatohex: data too short"
				data = ""
				data = data.zfill(length) # data = "0"*(length-len(data)) + data
			else:
				data = data[2:] # 0x01 -> 01
				if len(data) > length:
					print "error on datatohex: data too long", data,len(data), length
					data = data[:length]
				else:
					data = data.zfill(length) # data = "0"*(length-len(data)) + data
		except Exception:
			print "[netio]","error on pack /", traceback.format_exc()
			data = "00"
		return data
	
	def send(self, datatype, datacontent, client, datalength=None, fast=False):
		try:
			datahead = self.calc_data_head(datatype, datacontent)
			data = datahead + datatype + datacontent
			#print "[netio]", "send", data
			rawdata = self.encode(data, datalength)
			if fast:
				client.transport.socket.sendall(rawdata)
			else:
				client.transport.write(rawdata)
		except Exception:
			print "[netio]","error on send /", traceback.format_exc()
	
	def sendmap(self, datatype, datacontent, pclist, pc, datalength=None, fast=False):
		try:
			for p in pclist.values():
				if p.online and p.mapclient != None:
					if p.map == pc.map:
						self.send(datatype, datacontent, p.mapclient, None, fast)
		except Exception:
			print "[netio]","error on sendmap /", traceback.format_exc()
	
	def sendmapwithoutself(self, datatype, datacontent, pclist, pc, datalength=None, fast=False):
		try:
			for p in pclist.values():
				if p.online and p.mapclient != None:
					if p.charid != pc.charid and p.map == pc.map:
						self.send(datatype, datacontent, p.mapclient, None, fast)
		except Exception:
			print "[netio]","error on sendmapwithoutself /", traceback.format_exc()
	
	def sendserver(self, datatype, datacontent, pclist, pc, datalength=None, fast=False):
		try:
			for p in pclist.values():
				if p.online:
					self.send(datatype, datacontent, p.mapclient, None, fast)
		except Exception:
			print "[netio]","error on sendserver /", traceback.format_exc()


