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
		#self.newcharid = None
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
		#-------------------------------
		server.cfg.set("player","defaultgmlevel", str(server.defaultgmlevel))
		server.cfg.set("player","loginevent", str(server.loginevent))
		#-------------------------------
		server.cfg.set("gmlevel","user", str(server.gmlevel["user"]))
		server.cfg.set("gmlevel","dustbox", str(server.gmlevel["dustbox"]))
		server.cfg.set("gmlevel","reloadscript", str(server.gmlevel["reloadscript"]))
		server.cfg.set("gmlevel","printitem", str(server.gmlevel["printitem"]))
		server.cfg.set("gmlevel","shop", str(server.gmlevel["shop"]))
		server.cfg.set("gmlevel","warehouse", str(server.gmlevel["warehouse"]))
		server.cfg.set("gmlevel","servermessage", str(server.gmlevel["servermessage"]))
		server.cfg.set("gmlevel","giveitem", str(server.gmlevel["giveitem"]))
		server.cfg.set("gmlevel","updategold", str(server.gmlevel["updategold"]))
		server.cfg.set("gmlevel","takeitem", str(server.gmlevel["takeitem"]))
		server.cfg.set("gmlevel","countitem", str(server.gmlevel["countitem"]))
		server.cfg.set("gmlevel","event", str(server.gmlevel["event"]))
		server.cfg.set("gmlevel","warp", str(server.gmlevel["warp"]))
		server.cfg.set("gmlevel","hair", str(server.gmlevel["hair"]))
		server.cfg.set("gmlevel","hc", str(server.gmlevel["hc"]))
		server.cfg.set("gmlevel","face", str(server.gmlevel["face"]))
		server.cfg.set("gmlevel","wig", str(server.gmlevel["wig"]))
		server.cfg.set("gmlevel","ex", str(server.gmlevel["ex"]))
		server.cfg.set("gmlevel","wing", str(server.gmlevel["wing"]))
		server.cfg.set("gmlevel","wc", str(server.gmlevel["wc"]))
		server.cfg.set("gmlevel","motion", str(server.gmlevel["motion"]))
		server.cfg.set("gmlevel","effect", str(server.gmlevel["effect"]))
		server.cfg.set("gmlevel","speed", str(server.gmlevel["speed"]))
		server.cfg.set("gmlevel","sell", str(server.gmlevel["sell"]))
		server.cfg.set("gmlevel","warpraw", str(server.gmlevel["warpraw"]))
		server.cfg.set("gmlevel","whereraw", str(server.gmlevel["whereraw"]))
		server.cfg.set("gmlevel","mob", str(server.gmlevel["mob"]))
		server.cfg.set("gmlevel","killallmob", str(server.gmlevel["killallmob"]))
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
			#server.newcharid = server.cfg.get("main","newcharid")
			server.loginserverport = int(server.cfg.get("main", "loginserverport"))
			server.mapserverport = int(server.cfg.get("main", "mapserverport"))
			server.webserverport = int(server.cfg.get("main", "webserverport"))
			server.serveraddress = server.cfg.get("main", "serveraddress")
			
			server.defaultgmlevel = int(server.cfg.get("player", "defaultgmlevel"))
			server.loginevent = int(server.cfg.get("player", "loginevent"))
			
			server.gmlevel["user"] = int(server.cfg.get("gmlevel", "user"))
			server.gmlevel["dustbox"] = int(server.cfg.get("gmlevel", "dustbox"))
			server.gmlevel["reloadscript"] = int(server.cfg.get("gmlevel", "reloadscript"))
			server.gmlevel["printitem"] = int(server.cfg.get("gmlevel", "printitem"))
			server.gmlevel["shop"] = int(server.cfg.get("gmlevel", "shop"))
			server.gmlevel["warehouse"] = int(server.cfg.get("gmlevel", "warehouse"))
			server.gmlevel["servermessage"] = int(server.cfg.get("gmlevel", "servermessage"))
			server.gmlevel["giveitem"] = int(server.cfg.get("gmlevel", "giveitem"))
			server.gmlevel["updategold"] = int(server.cfg.get("gmlevel", "updategold"))
			server.gmlevel["takeitem"] = int(server.cfg.get("gmlevel", "takeitem"))
			server.gmlevel["countitem"] = int(server.cfg.get("gmlevel", "countitem"))
			server.gmlevel["event"] = int(server.cfg.get("gmlevel", "event"))
			server.gmlevel["warp"] = int(server.cfg.get("gmlevel", "warp"))
			server.gmlevel["hair"] = int(server.cfg.get("gmlevel", "hair"))
			server.gmlevel["hc"] = int(server.cfg.get("gmlevel", "hc"))
			server.gmlevel["face"] = int(server.cfg.get("gmlevel", "face"))
			server.gmlevel["wig"] = int(server.cfg.get("gmlevel", "wig"))
			server.gmlevel["ex"] = int(server.cfg.get("gmlevel", "ex"))
			server.gmlevel["wing"] = int(server.cfg.get("gmlevel", "wing"))
			server.gmlevel["wc"] = int(server.cfg.get("gmlevel", "wc"))
			server.gmlevel["motion"] = int(server.cfg.get("gmlevel", "motion"))
			server.gmlevel["effect"] = int(server.cfg.get("gmlevel", "effect"))
			server.gmlevel["speed"] = int(server.cfg.get("gmlevel", "speed"))
			server.gmlevel["sell"] = int(server.cfg.get("gmlevel", "sell"))
			server.gmlevel["warpraw"] = int(server.cfg.get("gmlevel", "warpraw"))
			server.gmlevel["whereraw"] = int(server.cfg.get("gmlevel", "whereraw"))
			server.gmlevel["mob"] = int(server.cfg.get("gmlevel", "mob"))
			server.gmlevel["killallmob"] = int(server.cfg.get("gmlevel", "killallmob"))
		except ConfigParser.NoOptionError, e:
			print e