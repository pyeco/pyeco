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
import copy

class Item:
	def getitemdic(self, filename):
		itemdic={}
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
			itemdic[itemid].Id = intx(row[0])
			itemdic[itemid].Count = 1
			itemdic[itemid].Warehouse = 0
			itemdic[itemid].Pictid = intx(row[1])
			itemdic[itemid].Name = row[3]
			itemdic[itemid].Type = row[4]
			itemdic[itemid].Price = intx(row[5])
			itemdic[itemid].Weight = intx(row[6])
			itemdic[itemid].Capa = intx(row[7])
			itemdic[itemid].Stock = intx(row[16])
			itemdic[itemid].Durability_max = intx(row[20])
			itemdic[itemid].EventID = intx(row[24])
			itemdic[itemid].Hp = intx(row[39])
			itemdic[itemid].Mp = intx(row[40])
			itemdic[itemid].Sp = intx(row[41])
			itemdic[itemid].Speed = intx(row[44])
			itemdic[itemid].Str = intx(row[45])
			itemdic[itemid].Mag = intx(row[46])
			itemdic[itemid].Vit = intx(row[47])
			itemdic[itemid].Dex = intx(row[48])
			itemdic[itemid].Agi = intx(row[49])
			itemdic[itemid].Int = intx(row[50])
			itemdic[itemid].Luk = intx(row[51])
			itemdic[itemid].Cha = intx(row[52])
			itemdic[itemid].Attack1 = intx(row[53])
			itemdic[itemid].Attack2 = intx(row[54])
			itemdic[itemid].Attack3 = intx(row[55])
			itemdic[itemid].Mattack = intx(row[56])
			itemdic[itemid].Def = intx(row[57])
			itemdic[itemid].Mdef = intx(row[58])
			itemdic[itemid].S_hit = intx(row[59])
			itemdic[itemid].L_hit = intx(row[60])
			itemdic[itemid].Magic_hit = intx(row[61])
			itemdic[itemid].S_avoid = intx(row[62])
			itemdic[itemid].L_avoid = intx(row[63])
			itemdic[itemid].Magic_avoid = intx(row[64])
			itemdic[itemid].Critical_hit = intx(row[65])
			itemdic[itemid].Critical_avoid = intx(row[66])
			itemdic[itemid].Heal_hp = intx(row[67])
			itemdic[itemid].Heal_mp = intx(row[68])
			itemdic[itemid].Energy = intx(row[69])
			itemdic[itemid].Fire = intx(row[70])
			itemdic[itemid].Water = intx(row[71])
			itemdic[itemid].Wind = intx(row[72])
			itemdic[itemid].Earth = intx(row[73])
			itemdic[itemid].Light = intx(row[74])
			itemdic[itemid].Dark = intx(row[75])
			itemdic[itemid].Poison = intx(row[76])
			itemdic[itemid].Stone = intx(row[77])
			itemdic[itemid].Paralyze = intx(row[78])
			itemdic[itemid].Sleep = intx(row[79])
			itemdic[itemid].Silence = intx(row[80])
			itemdic[itemid].Slow = intx(row[81])
			itemdic[itemid].Confuse = intx(row[82])
			itemdic[itemid].Freeze = intx(row[83])
			itemdic[itemid].Stan = intx(row[84])
		return itemdic
	
	def createitem(self, itemdic, itemid):
		itemobj = Item()
		itemid = int(itemid)
		if itemdic.get(itemid) == None:
			itemid = 10000000
		itemobj = copy.deepcopy(itemdic[itemid])
		return itemobj
	
	def __init__(self):
		self.Id = None
		self.Count = None
		self.Warehouse = None
		self.Pictid = None
		self.Name = None
		self.Type = None
		self.Price = None
		self.Weight = None
		self.Capa = None
		self.Stock = None
		self.Durability_max = None
		self.Hp = None
		self.Mp = None
		self.Sp = None
		self.Speed = None
		self.Str = None
		self.Mag = None
		self.Vit = None
		self.Dex = None
		self.Agi = None
		self.Int = None
		self.Luk = None
		self.Cha = None
		self.Attack1 = None
		self.Attack2 = None
		self.Attack3 = None
		self.Mattack = None
		self.Def = None
		self.Mdef = None
		self.S_hit = None
		self.L_hit = None
		self.Magic_hit = None
		self.S_avoid = None
		self.L_avoid = None
		self.Magic_avoid = None
		self.Critical_hit = None
		self.Critical_avoid = None
		self.Heal_hp = None
		self.Heal_mp = None
		self.Energy = None
		self.Fire = None
		self.Water = None
		self.Wind = None
		self.Earth = None
		self.Light = None
		self.Dark = None
		self.Poison = None
		self.Stone = None
		self.Paralyze = None
		self.Sleep = None
		self.Silence = None
		self.Slow = None
		self.Confuse = None
		self.Freeze = None
		self.Stan = None
