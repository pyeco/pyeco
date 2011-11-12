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
import copy

class Item(DataAccessControl):
	def getitemdic(self, filename):
		itemdic = {}
		reader = csv.reader(file(filename, "rb"))
		def intx(i):
			if i == "" or i == ".":
				return 0
			else:
				return int(i)
		for row in reader:
			lenrow = len(row)
			if lenrow < 10:
				continue
			if row[0][0:1] == "#":
				continue
			if lenrow < 85:
				print "[ all ]", "item load error in Object.itemobj / len(row) < 85", row
				continue
			try:
				itemid = int(row[0])
			except:
				continue
			itemdic[itemid]=Item()
			itemdic[itemid].id = intx(row[0])
			itemdic[itemid].count = 1
			itemdic[itemid].warehouse = 0
			itemdic[itemid].pictid = intx(row[1])
			itemdic[itemid].name = row[3]
			itemdic[itemid].type = row[4]
			itemdic[itemid].price = intx(row[5])
			itemdic[itemid].weight = intx(row[6])
			itemdic[itemid].capa = intx(row[7])
			itemdic[itemid].stock = intx(row[16])
			itemdic[itemid].durability_max = intx(row[20])
			itemdic[itemid].eventid = intx(row[24])
			itemdic[itemid].hp = intx(row[39])
			itemdic[itemid].mp = intx(row[40])
			itemdic[itemid].sp = intx(row[41])
			itemdic[itemid].speed = intx(row[44])
			itemdic[itemid].str = intx(row[45])
			itemdic[itemid].mag = intx(row[46])
			itemdic[itemid].vit = intx(row[47])
			itemdic[itemid].dex = intx(row[48])
			itemdic[itemid].agi = intx(row[49])
			itemdic[itemid].int = intx(row[50])
			itemdic[itemid].luk = intx(row[51])
			itemdic[itemid].cha = intx(row[52])
			itemdic[itemid].atk1 = intx(row[53])
			itemdic[itemid].atk2 = intx(row[54])
			itemdic[itemid].atk3 = intx(row[55])
			itemdic[itemid].matk = intx(row[56])
			itemdic[itemid].DEF = intx(row[57])
			itemdic[itemid].mdef = intx(row[58])
			itemdic[itemid].s_hit = intx(row[59])
			itemdic[itemid].l_hit = intx(row[60])
			itemdic[itemid].magic_hit = intx(row[61])
			itemdic[itemid].s_avoid = intx(row[62])
			itemdic[itemid].l_avoid = intx(row[63])
			itemdic[itemid].magic_avoid = intx(row[64])
			itemdic[itemid].critical_hit = intx(row[65])
			itemdic[itemid].critical_avoid = intx(row[66])
			itemdic[itemid].heal_hp = intx(row[67])
			itemdic[itemid].heal_mp = intx(row[68])
			itemdic[itemid].energy = intx(row[69])
			itemdic[itemid].fire = intx(row[70])
			itemdic[itemid].water = intx(row[71])
			itemdic[itemid].wind = intx(row[72])
			itemdic[itemid].earth = intx(row[73])
			itemdic[itemid].light = intx(row[74])
			itemdic[itemid].dark = intx(row[75])
			itemdic[itemid].poison = intx(row[76])
			itemdic[itemid].stone = intx(row[77])
			itemdic[itemid].paralyze = intx(row[78])
			itemdic[itemid].sleep = intx(row[79])
			itemdic[itemid].silence = intx(row[80])
			itemdic[itemid].slow = intx(row[81])
			itemdic[itemid].confuse = intx(row[82])
			itemdic[itemid].freeze = intx(row[83])
			itemdic[itemid].stan = intx(row[84])
		return itemdic
	
	def createitem(self, itemdic, itemid):
		itemobj = Item()
		itemid = int(itemid)
		if itemdic.get(itemid) == None:
			itemid = 10000000
		itemobj = copy.deepcopy(itemdic[itemid])
		return itemobj
	
	def __init__(self):
		self.add("id", 0)
		self.add("eventid", 0)
		self.add("count", 0)
		self.add("warehouse", 0)
		self.add("pictid", 0)
		self.add("name", "")
		self.add("type", "")
		self.add("price", 0)
		self.add("weight", 0)
		self.add("capa", 0)
		self.add("stock", 0)
		self.add("durability_max", 0)
		self.add("hp", 0)
		self.add("mp", 0)
		self.add("sp", 0)
		self.add("speed", 0)
		self.add("str", 0)
		self.add("mag", 0)
		self.add("vit", 0)
		self.add("dex", 0)
		self.add("agi", 0)
		self.add("int", 0)
		self.add("luk", 0)
		self.add("cha", 0)
		self.add("atk1", 0)
		self.add("atk2", 0)
		self.add("atk3", 0)
		self.add("matk", 0)
		self.add("DEF", 0)
		self.add("mdef", 0)
		self.add("s_hit", 0)
		self.add("l_hit", 0)
		self.add("magic_hit", 0)
		self.add("s_avoid", 0)
		self.add("l_avoid", 0)
		self.add("magic_avoid", 0)
		self.add("critical_hit", 0)
		self.add("critical_avoid", 0)
		self.add("heal_hp", 0)
		self.add("heal_mp", 0)
		self.add("energy", 0)
		self.add("fire", 0)
		self.add("water", 0)
		self.add("wind", 0)
		self.add("earth", 0)
		self.add("light", 0)
		self.add("dark", 0)
		self.add("poison", 0)
		self.add("stone", 0)
		self.add("paralyze", 0)
		self.add("sleep", 0)
		self.add("silence", 0)
		self.add("slow", 0)
		self.add("confuse", 0)
		self.add("freeze", 0)
		self.add("stan", 0)
