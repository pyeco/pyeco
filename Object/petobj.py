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
import csv
class Pet(DataAccessControl):
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
		self.add("id", 0) #pet id
		self.add("pictid", 0) #pet pictid
		self.add("sid", 0) #server id
		self.add("charid", 0) #fake pc #equal server id
		self.add("name", "")
		self.add("master", None) # PC()
		self.add("hp", 0)
		self.add("maxhp", 0)
		self.add("map", 0)
		self.add("x", 0)
		self.add("y", 0)
		self.add("dir", 0)
		self.add("rawx", 0)
		self.add("rawy", 0)
		self.add("rawdir", 0)
		self.add("speed", 310) #410
		self.add("motion", 0)
		self.add("lv_base", 1)
		#for CreatePacket.create020e
		self.add("race", 0)
		self.add("form", 0)
		self.add("gender", 1)
		self.add("hair", 0)
		self.add("haircolor", 0)
		self.add("wig", 0)
		self.add("face", 0)
		self.add("base_lv", 0)
		self.add("ex", 0)
		self.add("wing", 0)
		self.add("wingcolor", 0)
		self.add("wrprank", 0)
		self.add("item", {1: self.FakeHeadItem()})
		self.add("equip", self.EquipClass())
	
	class FakeHeadItem(DataAccessControl):
		def __init__(self):
			self.add("id", 0)
			self.add("type", "HELM")
	class EquipClass(DataAccessControl):
		def __init__(self):
			self.add("head", 1)
			self.add("face", 0)
			self.add("chestacce", 0)
			self.add("tops", 0)
			self.add("bottoms", 0)
			self.add("backpack", 0)
			self.add("right", 0)
			self.add("left", 0)
			self.add("shoes", 0)
			self.add("socks", 0)
			self.add("pet", 0)
