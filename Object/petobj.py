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
import csv
class Pet:
	def getpetdic(self, filename):
		petdic={}
		reader = csv.reader(file(filename, "rb"))
		def intx(i):
			if i == "":
				return 0
			else:
				return int(i)
		for row in reader:
			if len(row) <= 1:
				continue
			if row[0][0:1] == "#":
				continue
			try:
				petid = int(row[0])
			except:
				continue
			petdic[petid]=Pet()
			petdic[petid].id = intx(row[0])
			petdic[petid].name = row[1]
			petdic[petid].pictid = row[2]
			petdic[petid].item[1].id = petdic[petid].pictid
			petdic[petid].hp = row[19]
			petdic[petid].maxhp = row[19]
		return petdic
	
	def __init__ (self):
		
		self.id = 0 #pet id
		self.pictid = 0 #pet pictid
		self.sid = 0 #server id
		self.charid = 0 #fake pc #equal server id
		self.name = ""
		self.master = None # PC()
		self.hp = 0
		self.maxhp = 0
		self.map = 0
		self.x = 0
		self.y = 0
		self.dir = 0
		self.rawx = 0
		self.rawy = 0
		self.rawdir = 0
		self.speed = 310 #410
		self.motion = 0
		self.lv_base = 1
		#for CreatePacket.create020e
		self.race = 0
		self.form = 0
		self.gender = 1
		self.hair = 0
		self.haircolor = 0
		self.wig = 0
		self.face = 0
		self.base_lv = 0
		self.ex = 0
		self.wing = 0
		self.wingcolor = 0
		self.wrprank = 0
		self.item = {1: self.FakeHeadItem()}
		self.equip = self.EquipClass()
	
	class FakeHeadItem:
		def __init__(self):
			self.id = 0
			self.type = "HELM"
	class EquipClass:
		def __init__(self):
			self.head = 1
			self.face = 0
			self.chestacce = 0
			self.tops = 0
			self.bottoms = 0
			self.backpack = 0
			self.right = 0
			self.left = 0
			self.shoes = 0
			self.socks = 0
			self.pet = 0
