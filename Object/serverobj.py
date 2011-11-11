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
import ConfigParser
import os
import io

class Server:
	def __init__(self):
		self.loginserverport = None
		self.mapserverport = None
		self.webserverport = None
		self.serveraddress = None
		self.defaultgmlevel = None
		self.gmlevel = {}
		self.clientlistcount = 0
		self.clientlist = {}
		self.packethandle = {}
		self.clientlistcount_map = 0
		self.clientlist_map = {}
		self.packethandle_map = {}
	
	def setlibdic(self, libdic, selfx=None):
		if not selfx:
			selfx = self
		selfx.libdic = libdic
		#selfx.__dict__.update(self.libdic) #danger
		for attr, value in selfx.libdic.items():
			if attr in selfx.__dict__.keys():
				print "[ lib ]", "error / attribute repeated /", attr
				continue
			selfx.__dict__[attr] = value
	
	def csv(self,var):
		var = var.split(",")
		while True:
			try:
				var.remove("")
			except:
				break
		return var
	
	def saveallconfig(self, server, ConfigFileName):
		#server.cfg.set("main","newcharid",server.newcharid)
		server.cfg.set("main","loginserverport", str(server.loginserverport))
		server.cfg.set("main","mapserverport", str(server.mapserverport))
		server.cfg.set("main","webserverport", str(server.webserverport))
		server.cfg.set("main","serveraddress", str(server.serveraddress))
		server.cfg.set("player","defaultgmlevel", str(server.defaultgmlevel))
		server.cfg.set("player","loginevent", str(server.loginevent))
		for cmd, gmlevel in server.gmlevel.iteritems():
			server.cfg.set("gmlevel", cmd, str(gmlevel))
		server.writehandle = open("./"+ConfigFileName, "w")
		server.cfg.write(server.writehandle)
		server.writehandle.close()
	
	def loadallconfig(self, server, ConfigFileName):
		server.readhandle = open("./"+ConfigFileName, "r")
		content = server.readhandle.read()
		server.readhandle.close()
		contentcopy = content
		contenthead_typea = content[:2].encode("hex").upper()
		contenthead_typeb = content[:3].encode("hex").upper()
		if contenthead_typea == "FEFF": #if do not upper, use typea == "feff"
			content = content[2:]
		elif contenthead_typea == "FFFE":
			content = content[2:]
		elif contenthead_typeb == "EFBBBF":
			content = content[3:]
		if len(content) != len(contentcopy):
			server.readhandle = open("./"+ConfigFileName, "w")
			server.readhandle.write(content)
			server.readhandle.close()
		server.readhandle.close()
		
		vmcfg = io.BytesIO(content)
		server.cfg = ConfigParser.SafeConfigParser()
		server.cfg.readfp(vmcfg)
		vmcfg.close()
		
		try:
			server.loginserverport = int(server.cfg.get("main", "loginserverport"))
			server.mapserverport = int(server.cfg.get("main", "mapserverport"))
			server.webserverport = int(server.cfg.get("main", "webserverport"))
			server.serveraddress = server.cfg.get("main", "serveraddress")
			server.defaultgmlevel = int(server.cfg.get("player", "defaultgmlevel"))
			server.loginevent = int(server.cfg.get("player", "loginevent"))
			cmds = server.cfg.options("gmlevel")
			for cmd in cmds:
				server.gmlevel[cmd] = int(server.cfg.get("gmlevel", cmd))
		except ConfigParser.NoOptionError, e:
			print e