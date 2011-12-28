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
import sys
import BaseHTTPServer
import SimpleHTTPServer
import posixpath
import urllib
import threading
import hashlib
from Object.pcobj import PC
import traceback

def convpoststr(text):
	text = str(text)
	while True:
		decodeindex = text.find("%")
		if decodeindex == -1:
			break
		else:
			try:
				text = text[:decodeindex]+\
					text[decodeindex+1:decodeindex+3].decode("hex")+\
					text[decodeindex+3:]
			except:
				text = text[:decodeindex]+\
					text[decodeindex+1:decodeindex+3]+\
					text[decodeindex+3:]
	return text

class HTTPHandle(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def translate_path(self,path):
		path = path.split('?',1)[0]
		path = path.split('#',1)[0]
		path = posixpath.normpath(urllib.unquote(path))
		words = path.split('/')
		words = filter(None, words)
		path = os.getcwd()+"/Htdocs"
		for word in words:
			drive, word = os.path.splitdrive(word)
			head, word = os.path.split(word)
			if word in (os.curdir, os.pardir): continue
			path = os.path.join(path, word)
		return path
		#return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self,path)
	
	def do_POST(self):
		self.send_response(200)
		self.end_headers()
		post = self.rfile.read(int(self.headers["Content-Length"]))
		if post.find("deleteaccount=") == 0:
			message = self.checkpost_delete(post)
		else:
			message = self.checkpost(post)
		self.wfile.write(str(message))
	
	def log_message(self,format,*args):
		pass
	
	def checkpost(self, post):
		#print "[ web ]", "checkpost", post
		message = None
		post = post.split("&")
		postdic = {}
		for x in post:
			x = x.replace("\r","")
			x = x.replace("\n","")
			if x.find("account=") == 0:
				postdic["account"] = x.replace("account=","")
			elif x.find("charactername=") == 0:
				postdic["charactername"] = x.replace("charactername=","")
				postdic["charactername"] = convpoststr(postdic["charactername"])
			elif x.find("password=") == 0:
				postdic["password"] = x.replace("password=","")
			elif x.find("deletepassword=") == 0:
				postdic["deletepassword"] = x.replace("deletepassword=","")
			elif x.find("gender=") == 0:
				postdic["gender"] = x.replace("gender=","")
			elif x.find("race=") == 0:
				postdic["race"] = x.replace("race=","")
			elif x.find("face=") == 0:
				postdic["face"] = x.replace("face=","")
		while True:
			if not postdic.get("account"):
				message = "please input account"
				break
			elif len(postdic.get("account")) > 30:
				message = "account too long"
				break
			elif postdic.get("account").find("..") != -1:
				message = "account can not include .."
				break
			elif not postdic.get("account").isalnum():
				message = "please input an alphanumeric account"
				break
			elif self.pclist.get(postdic.get("account")):
				message = "account exist<br>please try another"
				break
			if not postdic.get("charactername"):
				message = "please input character name"
				break
			elif len(postdic.get("charactername")) > 30:
				message = "character name too long"
				break
			else:
				for p in self.pclist.values():
					if str(postdic.get("charactername")) == p.name:
						message = "character name exist<br>please try another"
						break
			if not postdic.get("password"):
				message = "please input password"
				break
			elif len(postdic.get("password")) > 30:
				message = "password too long"
				break
			elif not postdic.get("password").isalnum():
				message = "please input an alphanumeric password"
				break
			if not postdic.get("deletepassword"):
				message = "please input deletepassword"
				break
			elif len(postdic.get("deletepassword")) > 30:
				message = "deletepassword too long"
				break
			elif not postdic.get("deletepassword").isalnum():
				message = "please input an alphanumeric deletepassword"
				break
			break
		if not message:
			#print "[ web ]", "start create", postdic
			if self.createaccount(postdic):
				message = "register success"
				print "[ web ]", "account", postdic.get("account"),
				print "register success"
				#print postdic
			else:
				message = "unknow error"
		return message
	
	def checkpost_delete(self, post):
		#print "[ web ]", "checkpost_delete", post
		message = None
		post = post.split("&")
		postdic = {}
		for x in post:
			x = x.replace("\r","")
			x = x.replace("\n","")
			if x.find("deleteaccount=") == 0:
				postdic["deleteaccount"] = x.replace("deleteaccount=","")
			elif x.find("password=") == 0:
				postdic["password"] = x.replace("password=","")
			elif x.find("deletepassword=") == 0:
				postdic["deletepassword"] = x.replace("deletepassword=","")
		while True:
			if not postdic.get("deleteaccount"):
				message = "please input account"
				break
			elif postdic.get("deleteaccount").find("..") != -1:
				message = "account can not include .."
				break
			elif not self.pclist.get(postdic.get("deleteaccount")):
				message = "account not exist<br>please try another"
				break
			if not postdic.get("password"):
				message = "please input password"
				break
			elif len(postdic.get("password")) > 30:
				message = "password too long"
				break
			if not postdic.get("deletepassword"):
				message = "please input deletepassword"
				break
			elif len(postdic.get("deletepassword")) > 30:
				message = "deletepassword too long"
				break
			password = str(postdic.get("password"))
			password = str(hashlib.md5(password).hexdigest())
			delpc = self.pclist.get(postdic.get("deleteaccount"))
			#print "[ web ]", "checkpassword", delpc.password, password
			if delpc.password != password:
				message = "wrong password"
				break
			deletepassword = postdic.get("deletepassword")
			deletepassword = hashlib.md5(deletepassword).hexdigest()
			delpc = self.pclist.get(postdic.get("deleteaccount"))
			#print "[ web ]", "checkdelpassword", delpc.delpassword, deletepassword
			if delpc.delpassword != deletepassword:
				message = "wrong password"
				break
			break
		if not message:
			#print "[ web ]", "start delete", postdic
			if self.deleteaccount(postdic):
				message = "success, delete account wait for the server restart."
				print "[ web ]", "account", postdic.get("deleteaccount"),
				print "delete success"
				#print postdic
			else:
				message = "account data not found"
		return message
	
	def deleteaccount(self, postdic):
		deleteaccount = True
		try:
			self.pclist.get(postdic.get("deleteaccount")).wait_for_delete = True
			os.remove("./UserDB/%s.ini"%(postdic.get("deleteaccount") ,))
		except:
			deleteaccount = False
		return deleteaccount
	
	def createaccount(self, postdic):
		createsuccess = False
		account = postdic.get("account")
		charactername = postdic.get("charactername")
		password = postdic.get("password")
		password = hashlib.md5(password).hexdigest()
		deletepassword = postdic.get("deletepassword")
		deletepassword = hashlib.md5(deletepassword).hexdigest()
		with self.lock_pclist and self.lock_moblist:
			if not self.pclist.get(account):
				existid = []
				for p in self.pclist.values():
					try:
						existid.append(int(p.sid))
					except:
						print "[ web ]", "createaccount error at append pc sid", traceback.format_exc()
				existid.extend(self.moblist.keys()) #maybe need map(int, keys)
				newcharid = 100
				while newcharid in existid:
					newcharid += 1
				newcharid = int(newcharid)
				gmlevel = int(self.serverobj.defaultgmlevel)
				#self.serverobj.newcharid = int(newcharid)+1
				self.serverobj.saveallconfig("server.ini")
				newpc = PC(self.itemobj, self.itemdic)
				newpc = newpc.makenewpc()
				newpc.account = account
				newpc.charid = newcharid
				newpc.sid = newcharid
				newpc.name = charactername
				newpc.password = password
				newpc.delpassword = deletepassword
				newpc.gmlevel = gmlevel
				if postdic.get("gender"):
					newpc.gender = int(postdic.get("gender"))
					if newpc.gender == 0:
						#スモック♂
						newpc.item[1] = self.itemobj.createitem(self.itemdic, 50000000)
						newpc.item[3] = self.itemobj.createitem(self.itemdic, 50060150)
				if postdic.get("race"):
					newpc.race = int(postdic.get("race"))
				if postdic.get("face"):
					newpc.face = int(postdic.get("face"))
				self.pclist[account] = newpc
				self.pclist[account].saveallconfig("UserDB/%s.ini"%account)
				createsuccess = True
		return createsuccess

class WebServer:
	def listen_thread(self, serverobj):
		webserverport = int(serverobj.webserverport)
		serverobj.setlibdic(serverobj.libdic, HTTPHandle)
		server = BaseHTTPServer.HTTPServer(("0.0.0.0",webserverport), HTTPHandle)
		server.serve_forever()
	def create_listen_thread(self, serverobj):
		self.lock_pclist = serverobj.lock_pclist
		self.lock_moblist = serverobj.lock_moblist
		args = (serverobj, )
		self.thread_listen=threading.Thread(target=self.listen_thread, args=(args))
		self.thread_listen.setDaemon(True)
		self.thread_listen.start()
		with serverobj.lock_print:
			print "[ web ] listening", serverobj.serveraddress, serverobj.webserverport