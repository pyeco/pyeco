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
#
import ConfigParser
import sys
import os
import io
import traceback

TYPE_TOPS = ["ARMOR_UPPER",
			"ONEPIECE",
			"COSTUME",
			"BODYSUIT",
			"WEDDING",
			"OVERALLS",
			"FACEBODYSUIT",
			"ONEPIECE"
			]
TYPE_RIGHT = ["CLAW",
			"HAMMER",
			"STAFF",
			"SWORD",
			"AXE",
			"SPEAR",
			"HANDBAG",
			"GUN",
			"ETC_WEAPON",
			"SHORT_SWORD",
			"RAPIER",
			"BOOK",
			"DUALGUN",
			"RIFLE",
			"THROW",
			"ROPE",
			"BULLET",
			"ARROW",
			]
TYPE_LEFT = ["BOW",
			"SHIELD",
			"LEFT_HANDBAG",
			"ACCESORY_FINGER",
			"STRINGS",
			]
TYPE_SHOES = ["LONGBOOTS",
			"BOOTS",
			"SHOES",
			"HALFBOOTS",
			]
TYPE_PET = ["BACK_DEMON",
			"PET",
			"RIDE_PET",
			"PET_NEKOMATA",
			]

class PC:
	def __init__(self):
		self.pcinit()

	"""def __setattr__(self, attr, value):
		#print attr, value
		self.__dict__[attr] = value
		if self.__dict__.get("online") != True:
			return
		type_updatepc = ["hair", "haircolor", "wig"]
		#import eventobj
		if attr in type_updatepc:
			eventobj.updatepc(self)"""

	def setequip(self, pc, iid, itemobj, itemdic):
		#print pc
		iid = int(iid)
		old = list()
		new = 0
		item = pc.item.get(iid)
		if item == None:
			return old, new
		#頭
		if item.Type == "HELM":
			if pc.equip.head != 0:
				old.append(pc.equip.head)
			pc.equip.head = iid
			new = 6
		elif item.Type == "ACCESORY_HEAD":
			if pc.equip.head != 0:
				old.append(pc.equip.head)
			pc.equip.head = iid
			new = 7
		#顔
		elif item.Type == "FULLFACE":
			if pc.equip.face != 0:
				old.append(pc.equip.face)
			pc.equip.face = iid
			new = 6 #8 before ver315
		elif item.Type == "ACCESORY_FACE":
			if pc.equip.face != 0:
				old.append(pc.equip.face)
			pc.equip.face = iid
			new = 8 #9 before ver315
		#胸アクセサリ
		elif item.Type == "ACCESORY_NECK" or  item.Type == "JOINT_SYMBOL":
			if pc.equip.chestacce != 0:
				old.append(pc.equip.chestacce)
			pc.equip.chestacce = iid
			new = 10
		#上半身
		elif item.Type in TYPE_TOPS:
			if pc.equip.tops != 0:
				old.append(pc.equip.tops)
			if item.Type == "ONEPIECE" and pc.equip.bottoms != 0:
				old.append(pc.equip.bottoms)
				pc.equip.bottoms = 0
			pc.equip.tops = iid
			new = 11
		#下半身
		elif item.Type == "ARMOR_LOWER" or item.Type == "SLACKS" :
			if pc.equip.bottoms != 0:
				old.append(pc.equip.bottoms)
			if pc.equip.tops != 0:
				cache = pc.item.get(pc.equip.tops)
				if cache != None and cache.Type == "ONEPIECE":
					old.append(pc.equip.tops)
					pc.equip.tops = 0
			pc.equip.bottoms = iid
			new = 12
		#背中
		elif item.Type == "BACKPACK":
			if pc.equip.backpack != 0:
				old.append(pc.equip.backpack)
			pc.equip.backpack = iid
			new = 13
		#右手装備
		elif item.Type in TYPE_RIGHT:
			if pc.equip.right != 0:
				old.append(pc.equip.right)
			pc.equip.right = iid
			new = 14
		#左手装備
		elif item.Type in TYPE_LEFT:
			if pc.equip.left != 0:
				old.append(pc.equip.left)
			pc.equip.left = iid
			new = 15
		#靴
		elif item.Type in TYPE_SHOES:
			if pc.equip.shoes != 0:
				old.append(pc.equip.shoes)
			pc.equip.shoes = iid
			new = 16
		#靴下
		elif item.Type == "SOCKS":
			if pc.equip.socks != 0:
				old.append(pc.equip.socks)
			pc.equip.socks = iid
			new = 17
		#ペット
		elif item.Type in TYPE_PET:
			if pc.equip.pet != 0:
				old.append(pc.equip.pet)
			pc.equip.pet = iid
			new = 18
		return old,new

	def unsetequip(self, pc, iid):
		#print pc
		iid = int(iid)
		if iid == 0:
			return
		elif pc.equip.head == iid:
			pc.equip.head = 0
		elif pc.equip.face == iid:
			pc.equip.face = 0
		elif pc.equip.chestacce == iid:
			pc.equip.chestacce = 0
		elif pc.equip.tops == iid:
			pc.equip.tops = 0
		elif pc.equip.bottoms == iid:
			pc.equip.bottoms = 0
		elif pc.equip.backpack == iid:
			pc.equip.backpack = 0
		elif pc.equip.right == iid:
			pc.equip.right = 0
		elif pc.equip.left == iid:
			pc.equip.left = 0
		elif pc.equip.shoes == iid:
			pc.equip.shoes = 0
		elif pc.equip.socks == iid:
			pc.equip.socks = 0
		elif pc.equip.pet == iid:
			pc.equip.pet = 0

	def equiplist(self, pc):
		l = list()
		if pc.equip.head !=  0:
			l.append(pc.equip.head)
		if pc.equip.face !=  0:
			l.append(pc.equip.face)
		if pc.equip.chestacce !=  0:
			l.append(pc.equip.chestacce)
		if pc.equip.tops !=  0:
			l.append(pc.equip.tops)
		if pc.equip.bottoms !=  0:
			l.append(pc.equip.bottoms)
		if pc.equip.backpack !=  0:
			l.append(pc.equip.backpack)
		if pc.equip.right !=  0:
			l.append(pc.equip.right)
		if pc.equip.left !=  0:
			l.append(pc.equip.left)
		if pc.equip.shoes !=  0:
			l.append(pc.equip.shoes)
		if pc.equip.socks !=  0:
			l.append(pc.equip.socks)
		if pc.equip.pet !=  0:
			l.append(pc.equip.pet)
		return l

	def calcstatus(self,pc):
		pc.status.minatk1 = (pc.Str + pc.Stradd + ( (pc.Str + pc.Stradd) / 9) ** 2 )
		pc.status.minatk1 = pc.status.minatk1 * (1 + ( (pc.Dex + pc.Dexadd) * 1.5 ) / 160 )
		pc.status.minatk2 = pc.status.minatk1
		pc.status.minatk3 = pc.status.minatk1

	def makenewpc(self):
		newpc = PC()
		#newpc.sort = PC.sort()
		#newpc.equip = PC.equip()
		#newpc.status = PC.status()
		newpc.cfg = ConfigParser.SafeConfigParser()
		newpc.cfg.add_section("main")
		newpc.cfg.add_section("status")
		newpc.cfg.add_section("equip")
		newpc.cfg.add_section("sort")
		newpc.cfg.add_section("item")
		newpc.cfg.add_section("warehouse")
		newpc.cfg.add_section("dic")
		newpc.account = "None"
		newpc.charid = "None"
		newpc.sid = "None"
		newpc.name = "None"
		newpc.password = "None"
		newpc.delpassword = "None"
		newpc.race = 0
		newpc.form = 0
		newpc.gender = 1
		newpc.hair = 7
		newpc.haircolor = 1
		newpc.wig = 65535
		newpc.face = 1
		newpc.base_lv = 0
		newpc.ex = 0
		newpc.wing = 0
		newpc.wingcolor = 0
		newpc.job = 0
		newpc.map = 30203000
		newpc.lv_base = 1
		newpc.lv_job1 = 1
		newpc.lv_job2x = 1
		newpc.lv_job2t = 1
		newpc.lv_job3 = 1
		newpc.gold = 0
		newpc.x = 13
		newpc.y = 8
		newpc.dir = 6
		newpc.Str = 8
		newpc.Dex = 3
		newpc.Int = 3
		newpc.Vit = 10
		newpc.Agi = 4
		newpc.Mag = 4
		newpc.Stradd = 2
		newpc.Dexadd = 1
		newpc.Intadd = 1
		newpc.Vitadd = 2
		newpc.Agiadd = 1
		newpc.Magadd = 1
		newpc.item = {}
		newpc.warehouse = {}
		newpc.sort.item = []
		newpc.sort.warehouse = []
		newpc.sort.item.append(1)
		newpc.sort.item.append(2)
		newpc.sort.item.append(3)
		newpc.sort.item.append(4)
		newpc.sort.item.append(5)
		newpc.item[1] = self.itemobj.createitem(self.itemdic, 50000055)
		newpc.item[2] = self.itemobj.createitem(self.itemdic, 50010300)
		newpc.item[3] = self.itemobj.createitem(self.itemdic, 50060100)
		newpc.item[4] = self.itemobj.createitem(self.itemdic, 10020114)
		newpc.item[5] = self.itemobj.createitem(self.itemdic, 60010082)
		newpc.equip.head = 0
		newpc.equip.face = 0
		newpc.equip.chestacce = 0
		newpc.equip.tops = 1
		newpc.equip.bottoms = 2
		newpc.equip.backpack = 0
		newpc.equip.right = 0
		newpc.equip.left = 0
		newpc.equip.shoes = 3
		newpc.equip.socks = 0
		newpc.equip.pet = 0
		newpc.dic = {}
		newpc.skill_list = []
		return newpc

	def setfunc(self,itemobj,itemdic):
		self.itemobj = itemobj
		self.itemdic = itemdic

	def csv(self,var):
		var = var.split(",")
		while True:
			try:
				var.remove("")
			except:
				break
		return var

	def saveallconfig(self, pc, ConfigFileName):
		if pc.wait_for_delete:
			return
		pc.cfg.remove_section("main")
		pc.cfg.add_section("main")
		pc.cfg.set("main", "charid", str(pc.charid))
		#pc.cfg.set("main", "charid", str(pc.sid))
		pc.cfg.set("main", "name", str(pc.name))
		pc.cfg.set("main", "password", str(pc.password))
		pc.cfg.set("main", "delpassword", str(pc.delpassword))
		pc.cfg.set("main", "gmlevel", str(pc.gmlevel))
		pc.cfg.set("main", "race", str(pc.race))
		pc.cfg.set("main", "form", str(pc.form))
		pc.cfg.set("main", "gender", str(pc.gender))
		pc.cfg.set("main", "hair", str(pc.hair))
		pc.cfg.set("main", "haircolor", str(pc.haircolor))
		pc.cfg.set("main", "wig", str(pc.wig))
		pc.cfg.set("main", "face", str(pc.face))
		pc.cfg.set("main", "base_lv", str(pc.base_lv))
		pc.cfg.set("main", "ex", str(pc.ex))
		pc.cfg.set("main", "wing", str(pc.wing))
		pc.cfg.set("main", "wingcolor", str(pc.wingcolor))
		pc.cfg.set("main", "job", str(pc.job))
		pc.cfg.set("main", "map", str(pc.map))
		pc.cfg.set("main", "lv_base", str(pc.lv_base))
		pc.cfg.set("main", "lv_job1", str(pc.lv_job1))
		pc.cfg.set("main", "lv_job2x", str(pc.lv_job2x))
		pc.cfg.set("main", "lv_job2t", str(pc.lv_job2t))
		pc.cfg.set("main", "lv_job3", str(pc.lv_job3))
		pc.cfg.set("main", "gold", str(pc.gold))
		pc.cfg.set("main", "x", str(pc.x))
		pc.cfg.set("main", "y", str(pc.y))
		pc.cfg.set("main", "dir", str(pc.dir))
		
		pc.cfg.remove_section("status")
		pc.cfg.add_section("status")
		pc.cfg.set("status", "str", str(pc.Str))
		pc.cfg.set("status", "dex", str(pc.Dex))
		pc.cfg.set("status", "int", str(pc.Int))
		pc.cfg.set("status", "vit", str(pc.Vit))
		pc.cfg.set("status", "agi", str(pc.Agi))
		pc.cfg.set("status", "mag", str(pc.Mag))
		pc.cfg.set("status", "stradd", str(pc.Stradd))
		pc.cfg.set("status", "dexadd", str(pc.Dexadd))
		pc.cfg.set("status", "intadd", str(pc.Intadd))
		pc.cfg.set("status", "vitadd", str(pc.Vitadd))
		pc.cfg.set("status", "agiadd", str(pc.Agiadd))
		pc.cfg.set("status", "magadd", str(pc.Magadd))
		
		pc.cfg.remove_section("equip")
		pc.cfg.add_section("equip")
		pc.cfg.set("equip", "head", str(pc.equip.head))
		pc.cfg.set("equip", "face", str(pc.equip.face))
		pc.cfg.set("equip", "chestacce", str(pc.equip.chestacce))
		pc.cfg.set("equip", "tops", str(pc.equip.tops))
		pc.cfg.set("equip", "bottoms", str(pc.equip.bottoms))
		pc.cfg.set("equip", "backpack", str(pc.equip.backpack))
		pc.cfg.set("equip", "right", str(pc.equip.right))
		pc.cfg.set("equip", "left", str(pc.equip.left))
		pc.cfg.set("equip", "shoes", str(pc.equip.shoes))
		pc.cfg.set("equip", "socks", str(pc.equip.socks))
		pc.cfg.set("equip", "pet", str(pc.equip.pet))
		
		pc.cfg.remove_section("item")
		pc.cfg.add_section("item")
		itemlist = sorted(pc.item, key=int)
		for x in itemlist:
			x = int(x)
			itemcfg = "%s,%s"%(pc.item[x].Id, pc.item[x].Count)
			pc.cfg.set("item", str(x), itemcfg)
		sort = ""
		for x in pc.sort.item:
			sort = sort+","+str(x)
		if len(sort) > 1:
			sort = sort[1:]
		pc.cfg.set("sort", "item", sort)
		
		pc.cfg.remove_section("warehouse")
		pc.cfg.add_section("warehouse")
		warehouse_itemlist = sorted(pc.warehouse, key=int)
		for x in warehouse_itemlist:
			x = int(x)
			warehouse_itemcfg = "%s,%s,%s"%(pc.warehouse[x].Id, \
							pc.warehouse[x].Count, pc.warehouse[x].Warehouse)
			pc.cfg.set("warehouse", str(x), warehouse_itemcfg)
		warehouse_sort = ""
		for x in pc.sort.warehouse:
			warehouse_sort += ",%s"%(x, )
		if len(warehouse_sort) > 1:
			warehouse_sort = warehouse_sort[1:]
		pc.cfg.set("sort", "warehouse", warehouse_sort)
		
		pc.cfg.remove_section("dic")
		pc.cfg.add_section("dic")
		pcdiclist = sorted(pc.dic)
		for x in pcdiclist:
			pc.cfg.set("dic", str(x), str(pc.dic[x]))
		
		# [10000000, 10000001] --> "10000000,10000001"
		def list_to_str(l):
			def appendspliter(item):
				return "%s," % (str(item), )
			return "".join(map(appendspliter, l))
		pc.cfg.remove_section("skill")
		pc.cfg.add_section("skill")
		pc.cfg.set("skill", "list", list_to_str(pc.skill_list))
		#print list_to_str(pc.skill_list)
		
		pc.writehandle = open("./"+ConfigFileName,"w")
		pc.cfg.write(pc.writehandle)
		pc.writehandle.close()

	def loadallconfig(self, pc, ConfigFileName):
		pc.readhandle = open("./"+ConfigFileName,"r")
		content = pc.readhandle.read()
		pc.readhandle.close()
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
			pc.readhandle = open("./"+ConfigFileName, "w")
			pc.readhandle.write(content)
			pc.readhandle.close()
		pc.readhandle.close()
		
		vmcfg = io.BytesIO(content)
		pc.cfg = ConfigParser.SafeConfigParser()
		pc.cfg.readfp(vmcfg)
		vmcfg.close()
		
		try:
			pc.charid = int(pc.cfg.get("main","charid"))
			pc.sid = int(pc.cfg.get("main","charid"))
			pc.name = pc.cfg.get("main","name")
			pc.password = pc.cfg.get("main","password")
			pc.delpassword = pc.cfg.get("main","delpassword")
			pc.gmlevel = int(pc.cfg.get("main","gmlevel"))
			pc.race = int(pc.cfg.get("main","race"))
			pc.form = int(pc.cfg.get("main","form"))
			try:
				pc.gender = int(pc.cfg.get("main","gender"))
			except:
				pc.gender = int(pc.cfg.get("main","sex"))
			pc.hair = int(pc.cfg.get("main","hair"))
			pc.haircolor = int(pc.cfg.get("main","haircolor"))
			pc.wig = int(pc.cfg.get("main","wig"))
			pc.face = int(pc.cfg.get("main","face"))
			pc.base_lv = int(pc.cfg.get("main","base_lv"))
			pc.ex = int(pc.cfg.get("main","ex"))
			pc.wing = int(pc.cfg.get("main","wing"))
			pc.wingcolor = int(pc.cfg.get("main","wingcolor"))
			pc.job = int(pc.cfg.get("main","job"))
			pc.map = int(pc.cfg.get("main","map"))
			pc.lv_base = int(pc.cfg.get("main","lv_base"))
			pc.lv_job1 = int(pc.cfg.get("main","lv_job1"))
			pc.lv_job2x = int(pc.cfg.get("main","lv_job2x"))
			pc.lv_job2t = int(pc.cfg.get("main","lv_job2t"))
			pc.lv_job3 = int(pc.cfg.get("main","lv_job3"))
			pc.gold = int(pc.cfg.get("main","gold"))
			pc.x = int(pc.cfg.get("main","x"))
			pc.y = int(pc.cfg.get("main","y"))
			pc.dir = int(pc.cfg.get("main","dir"))
			
			pc.Str = int(pc.cfg.get("status","str"))
			pc.Dex = int(pc.cfg.get("status","dex"))
			pc.Int = int(pc.cfg.get("status","int"))
			pc.Vit = int(pc.cfg.get("status","vit"))
			pc.Agi = int(pc.cfg.get("status","agi"))
			pc.Mag = int(pc.cfg.get("status","mag"))
			pc.Stradd = int(pc.cfg.get("status","stradd"))
			pc.Dexadd = int(pc.cfg.get("status","dexadd"))
			pc.Intadd = int(pc.cfg.get("status","intadd"))
			pc.Vitadd = int(pc.cfg.get("status","vitadd"))
			pc.Agiadd = int(pc.cfg.get("status","agiadd"))
			pc.Magadd = int(pc.cfg.get("status","magadd"))
			
			#{item_id:item_object, ...}
			pc.item = {}
			pc.sort.item = map(int, self.csv(pc.cfg.get("sort","item")))
			for x in pc.sort.item: # x is item id
				itemcfg = map(int, self.csv(pc.cfg.get("item", str(x))))
				itemid = itemcfg[0]
				itemcount = itemcfg[1]
				item = self.itemobj.createitem(self.itemdic, itemid)
				item.Count = itemcount
				pc.item[int(x)] = item
			
			#{item_id:item_object, ...}
			pc.warehouse = {}
			pc.sort.warehouse = map(int, self.csv(pc.cfg.get("sort", "warehouse")))
			for x in pc.sort.warehouse: # x is item id
				warehouse_itemcfg = map(int, self.csv(pc.cfg.get("warehouse", str(x))))
				warehouse_itemid = warehouse_itemcfg[0]
				warehouse_itemcount = warehouse_itemcfg[1]
				warehouse_id = warehouse_itemcfg[2]
				warehouse_item = self.itemobj.createitem(self.itemdic, warehouse_itemid)
				warehouse_item.Count = warehouse_itemcount
				warehouse_item.Warehouse = warehouse_id
				pc.warehouse[int(x)] = warehouse_item
			
			pc.equip.head = int(pc.cfg.get("equip","head"))
			pc.equip.face = int(pc.cfg.get("equip","face"))
			pc.equip.chestacce = int(pc.cfg.get("equip","chestacce"))
			pc.equip.tops = int(pc.cfg.get("equip","tops"))
			pc.equip.bottoms = int(pc.cfg.get("equip","bottoms"))
			pc.equip.backpack = int(pc.cfg.get("equip","backpack"))
			pc.equip.right = int(pc.cfg.get("equip","right"))
			pc.equip.left = int(pc.cfg.get("equip","left"))
			pc.equip.shoes = int(pc.cfg.get("equip","shoes"))
			pc.equip.socks = int(pc.cfg.get("equip","socks"))
			pc.equip.pet = int(pc.cfg.get("equip","pet"))
			
			try:
				pcdiclist = pc.cfg.options("dic")
			except ConfigParser.NoSectionError:
				pcdiclist = {}
			pc.dic = {}
			if pcdiclist:
				for x in pcdiclist:
					pc.dic[x] = pc.cfg.get("dic", str(x))
			#print pc.dic
			
			try:
				skill_list = pc.cfg.get("skill","list")
			except ConfigParser.NoSectionError:
				#print "[ pc  ]", "reset skill / ",
				#print pc.name.decode("utf-8").encode(sys.getfilesystemencoding())
				skill_list = ""
			# "10000000,10000001" --> [10000000, 10000001]
			pc.skill_list = list(map(int, filter(None, skill_list.split(","))))
		
		except ConfigParser.NoOptionError, e:
			print e

	def reset_attack_info(self):
		if not self.attacking:
			return
		print "[ pc  ]", "stop attacking from",
		print traceback.extract_stack()[-2][2]
		self.attacking = False
		with self.e.lock_pclist:
			self.attacking = False
			self.attacking_target = None
			self.attacking_delay = 0
	
	def pcinit(self):
		self.client = None
		self.mapclient = None
		self.account = None
		self.charid = None
		self.sid = None # server id
		
		self.online = False
		self.online_login = False
		self.visible = False
		self.loginevent = False
		self.attacking = False
		self.attacking_target = None
		self.attacking_delay = 0
		self.wait_for_delete = False
		
		self.selectresult = None
		self.motion = 111
		self.effect = None
		self.tradestate = 0
		self.tradelist = None
		self.tradereturnlist = None
		self.isnpctrade = False
		self.warehouse_open = None
		self.e = None
		
		self.name = None
		self.password = None
		self.delpassword = None
		self.gmlevel = None
		self.race = None
		self.form = None
		self.gender = None
		self.hair = None
		self.haircolor = None
		self.wig = None
		self.face = None
		self.base_lv = None
		self.ex = None
		self.wing = None
		self.wingcolor = None
		self.job = None
		self.map = None
		self.lv_base = None
		self.lv_job1 = None
		self.lv_job2x = None
		self.lv_job2t = None
		self.lv_job3 = None
		self.gold = None
		
		self.Str = None
		self.Dex = None
		self.Int = None
		self.Vit = None
		self.Agi = None
		self.Mag = None
		self.Stradd = None
		self.Dexadd = None
		self.Intadd = None
		self.Vitadd = None
		self.Agiadd = None
		self.Magadd = None
		
		self.skill_list = None
		
		self.x = None
		self.y = None
		self.dir = None
		self.rawx = None
		self.rawy = None
		self.rawdir = None
		
		self.item = None
		self.warehouse = None
		self.dic = None
		self.battlestatus = None
		
		self.logout = False
		self.sendmapserver = False
		
		self.sort = self.SortClass()
		self.equip = self.EquipClass()
		self.status = self.StatusClass()

	class SortClass:
		def __init__(self):
			self.item = None
			self.warehouse = None
	class EquipClass:
		def __init__(self):
			self.head = None
			self.face = None
			self.chestacce = None
			self.tops = None
			self.bottoms = None
			self.backpack = None
			self.right = None
			self.left = None
			self.shoes = None
			self.socks = None
			self.pet = None
	class StatusClass:
		def __init__(self):
			self.maxhp = 86
			self.maxmp = 40
			self.maxsp = 34
			self.maxep = 30
			self.hp = 86
			self.mp = 40
			self.sp = 34
			self.ep = 30
			self.speed = 410
			self.minatk1 = 100
			self.minatk2 = 100
			self.minatk3 = 100
			self.maxatk1 = 100
			self.maxatk2 = 100
			self.maxatk3 = 100
			self.minmatk = 100
			self.maxmatk = 100
			self.leftdef = 50
			self.rightdef = 30
			self.leftmdef = 30
			self.rightmdef = 20
			self.shit = 7
			self.lhit = 0 # ...
			self.mhit = 7
			self.chit = 0
			self.savoid = 0 # ...
			self.lavoid = 12
			self.hpheal = 0
			self.mpheal = 0
			self.spheal = 0
			self.aspd = 750 #190
			self.cspd = 187
			self.adelay = 2 * (1 - self.aspd/1000.0)
			self.maxcapa = 1000
			self.maxrightcapa = 0
			self.maxleftcapa = 0
			self.maxbackcapa = 0
			self.maxpayl = 1000
			self.maxrightpayl = 0
			self.maxleftpayl = 0
			self.maxbackpayl = 0
			self.capa = 30
			self.rightcapa = 0
			self.leftcapa = 0
			self.backcapa = 0
			self.payl = 30
			self.rightpayl = 0
			self.leftpayl = 0
			self.backpayl = 0




