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
from Object import eventobj
import ConfigParser
import sys
import os
import io
import traceback
import StringIO

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
CALL_UPDATEPC_WHEN_CHANGE = ["name",
						"race",
						"form",
						"gender",
						"hair",
						"haircolor",
						"wig",
						"face",
						"base_lv",
						"ex",
						"wing",
						"wingcolor",
						#"motion",
						"lv_base"]

class PC(DataAccessControl):
	def __init__(self, global_itemobj, global_itemdic):
		self.pcinit()
		self.add("cfg", None) #ConfigParser.SafeConfigParser()
		self.add("readhandle", None) #open(path, "rb")
		self.add("writehandle", None) #open(path, "wb")
		self.add("itemobj", global_itemobj)
		self.add("itemdic", global_itemdic)
	
	def __setattr__(self, name, value):
		DataAccessControl.__setattr__(self, name, value)
		if name in CALL_UPDATEPC_WHEN_CHANGE and self.online and self.e:
			#print "eventobj.updatepc(self)", name
			eventobj.updatepc(self)
	
	def setequip(self, iid, itemobj, itemdic):
		#print pc
		iid = int(iid)
		old = [] #unset list
		new = 0
		item = self.item.get(iid)
		if item == None:
			return old, new
		#頭
		if item.type == "HELM":
			if self.equip.head != 0:
				old.append(self.equip.head)
			self.equip.head = iid
			new = 6
		elif item.type == "ACCESORY_HEAD":
			if self.equip.head != 0:
				old.append(self.equip.head)
			self.equip.head = iid
			new = 7
		#顔
		elif item.type == "FULLFACE":
			if self.equip.face != 0:
				old.append(self.equip.face)
			self.equip.face = iid
			new = 6 #8 before ver315
		elif item.type == "ACCESORY_FACE":
			if self.equip.face != 0:
				old.append(self.equip.face)
			self.equip.face = iid
			new = 8 #9 before ver315
		#胸アクセサリ
		elif item.type == "ACCESORY_NECK" or item.type == "JOINT_SYMBOL":
			if self.equip.chestacce != 0:
				old.append(self.equip.chestacce)
			self.equip.chestacce = iid
			new = 10
		#上半身
		elif item.type in TYPE_TOPS:
			if self.equip.tops != 0:
				old.append(self.equip.tops)
			if item.type == "ONEPIECE" and self.equip.bottoms != 0:
				old.append(self.equip.bottoms)
				self.equip.bottoms = 0
			self.equip.tops = iid
			new = 11
		#下半身
		elif item.type == "ARMOR_LOWER" or item.type == "SLACKS" :
			if self.equip.bottoms != 0:
				old.append(self.equip.bottoms)
			if self.equip.tops != 0:
				cache = self.item.get(self.equip.tops)
				if cache != None and cache.type == "ONEPIECE":
					old.append(self.equip.tops)
					self.equip.tops = 0
			self.equip.bottoms = iid
			new = 12
		#背中
		elif item.type == "BACKPACK":
			if self.equip.backpack != 0:
				old.append(self.equip.backpack)
			self.equip.backpack = iid
			new = 13
		#右手装備
		elif item.type in TYPE_RIGHT:
			if self.equip.right != 0:
				old.append(self.equip.right)
			self.equip.right = iid
			new = 14
		#左手装備
		elif item.type in TYPE_LEFT:
			if self.equip.left != 0:
				old.append(self.equip.left)
			self.equip.left = iid
			new = 15
		#靴
		elif item.type in TYPE_SHOES:
			if self.equip.shoes != 0:
				old.append(self.equip.shoes)
			self.equip.shoes = iid
			new = 16
		#靴下
		elif item.type == "SOCKS":
			if self.equip.socks != 0:
				old.append(self.equip.socks)
			self.equip.socks = iid
			new = 17
		#ペット
		elif item.type in TYPE_PET:
			if self.equip.pet != 0:
				old.append(self.equip.pet)
				eventobj.unsetpet(self)
			self.equip.pet = iid
			new = 18
		return old, new
	
	def unsetequip(self, iid):
		#print pc
		iid = int(iid)
		if iid == 0:
			return
		elif self.equip.head == iid:
			self.equip.head = 0
		elif self.equip.face == iid:
			self.equip.face = 0
		elif self.equip.chestacce == iid:
			self.equip.chestacce = 0
		elif self.equip.tops == iid:
			self.equip.tops = 0
		elif self.equip.bottoms == iid:
			self.equip.bottoms = 0
		elif self.equip.backpack == iid:
			self.equip.backpack = 0
		elif self.equip.right == iid:
			self.equip.right = 0
		elif self.equip.left == iid:
			self.equip.left = 0
		elif self.equip.shoes == iid:
			self.equip.shoes = 0
		elif self.equip.socks == iid:
			self.equip.socks = 0
		elif self.equip.pet == iid:
			self.equip.pet = 0
			eventobj.unsetpet(self)
	
	def equiplist(self):
		l = []
		if self.equip.head !=  0:
			l.append(self.equip.head)
		if self.equip.face !=  0:
			l.append(self.equip.face)
		if self.equip.chestacce !=  0:
			l.append(self.equip.chestacce)
		if self.equip.tops !=  0:
			l.append(self.equip.tops)
		if self.equip.bottoms !=  0:
			l.append(self.equip.bottoms)
		if self.equip.backpack !=  0:
			l.append(self.equip.backpack)
		if self.equip.right !=  0:
			l.append(self.equip.right)
		if self.equip.left !=  0:
			l.append(self.equip.left)
		if self.equip.shoes !=  0:
			l.append(self.equip.shoes)
		if self.equip.socks !=  0:
			l.append(self.equip.socks)
		if self.equip.pet !=  0:
			l.append(self.equip.pet)
		return l
	
	def calcstatus(self):
		self.status.minatk1 = (self.str + self.stradd + ((self.str + self.stradd) / 9) ** 2)
		self.status.minatk1 = self.status.minatk1 * (1 + ((self.dex + self.dexadd) * 1.5) / 160)
		self.status.minatk2 = self.status.minatk1
		self.status.minatk3 = self.status.minatk1
	
	def csv(self, var):
		var = var.split(",")
		while True:
			try:
				var.remove("")
			except:
				break
		return var
	
	def loadallconfig(self, ConfigFileName):
		self.readhandle = open("./%s"%ConfigFileName,"rb")
		content = self.readhandle.read()
		self.readhandle.close()
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
			self.readhandle = open("./%s"%ConfigFileName, "wb")
			self.readhandle.write(content)
			self.readhandle.close()
		self.readhandle.close()
		
		vmcfg = StringIO.StringIO(content.replace("\r\n", "\n"))
		self.cfg = ConfigParser.SafeConfigParser()
		self.cfg.readfp(vmcfg)
		vmcfg.close()
		
		try:
			self.charid = int(self.cfg.get("main","charid"))
			self.sid = int(self.cfg.get("main","charid"))
			self.name = self.cfg.get("main","name")
			self.password = self.cfg.get("main","password")
			self.delpassword = self.cfg.get("main","delpassword")
			self.gmlevel = int(self.cfg.get("main","gmlevel"))
			self.race = int(self.cfg.get("main","race"))
			self.form = int(self.cfg.get("main","form"))
			try:
				self.gender = int(self.cfg.get("main","gender"))
			except:
				self.gender = int(self.cfg.get("main","sex"))
			self.hair = int(self.cfg.get("main","hair"))
			self.haircolor = int(self.cfg.get("main","haircolor"))
			self.wig = int(self.cfg.get("main","wig"))
			self.face = int(self.cfg.get("main","face"))
			self.base_lv = int(self.cfg.get("main","base_lv"))
			self.ex = int(self.cfg.get("main","ex"))
			self.wing = int(self.cfg.get("main","wing"))
			self.wingcolor = int(self.cfg.get("main","wingcolor"))
			self.job = int(self.cfg.get("main","job"))
			self.map = int(self.cfg.get("main","map"))
			self.lv_base = int(self.cfg.get("main","lv_base"))
			self.lv_job1 = int(self.cfg.get("main","lv_job1"))
			self.lv_job2x = int(self.cfg.get("main","lv_job2x"))
			self.lv_job2t = int(self.cfg.get("main","lv_job2t"))
			self.lv_job3 = int(self.cfg.get("main","lv_job3"))
			self.gold = int(self.cfg.get("main","gold"))
			self.x = int(self.cfg.get("main","x"))
			self.y = int(self.cfg.get("main","y"))
			self.dir = int(self.cfg.get("main","dir"))
			
			self.str = int(self.cfg.get("status","str"))
			self.dex = int(self.cfg.get("status","dex"))
			self.int = int(self.cfg.get("status","int"))
			self.vit = int(self.cfg.get("status","vit"))
			self.agi = int(self.cfg.get("status","agi"))
			self.mag = int(self.cfg.get("status","mag"))
			self.stradd = int(self.cfg.get("status","stradd"))
			self.dexadd = int(self.cfg.get("status","dexadd"))
			self.intadd = int(self.cfg.get("status","intadd"))
			self.vitadd = int(self.cfg.get("status","vitadd"))
			self.agiadd = int(self.cfg.get("status","agiadd"))
			self.magadd = int(self.cfg.get("status","magadd"))
			
			#{item_id:item_object, ...}
			self.item = {}
			self.sort.item = map(int, self.csv(self.cfg.get("sort", "item")))
			for i in self.sort.item: #i:item id
				itemcfg = map(int, self.csv(self.cfg.get("item", str(i))))
				itemid = itemcfg[0]
				itemcount = itemcfg[1]
				item = self.itemobj.createitem(self.itemdic, itemid)
				item.count = itemcount
				self.item[i] = item
			
			#{item_id:item_object, ...}
			self.warehouse = {}
			self.sort.warehouse = map(int, self.csv(self.cfg.get("sort", "warehouse")))
			for i in self.sort.warehouse: #i:item id
				warehouse_itemcfg = map(int, self.csv(self.cfg.get("warehouse", str(i))))
				warehouse_itemid = warehouse_itemcfg[0]
				warehouse_itemcount = warehouse_itemcfg[1]
				warehouse_id = warehouse_itemcfg[2]
				warehouse_item = self.itemobj.createitem(self.itemdic, warehouse_itemid)
				warehouse_item.count = warehouse_itemcount
				warehouse_item.warehouse = warehouse_id
				self.warehouse[i] = warehouse_item
			
			self.equip.head = int(self.cfg.get("equip","head"))
			self.equip.face = int(self.cfg.get("equip","face"))
			self.equip.chestacce = int(self.cfg.get("equip","chestacce"))
			self.equip.tops = int(self.cfg.get("equip","tops"))
			self.equip.bottoms = int(self.cfg.get("equip","bottoms"))
			self.equip.backpack = int(self.cfg.get("equip","backpack"))
			self.equip.right = int(self.cfg.get("equip","right"))
			self.equip.left = int(self.cfg.get("equip","left"))
			self.equip.shoes = int(self.cfg.get("equip","shoes"))
			self.equip.socks = int(self.cfg.get("equip","socks"))
			self.equip.pet = int(self.cfg.get("equip","pet"))
			
			try:
				pcdiclist = self.cfg.options("dic")
			except ConfigParser.NoSectionError:
				pcdiclist = {}
			self.dic = {}
			if pcdiclist:
				for name in pcdiclist:
					self.dic[name] = self.cfg.get("dic", str(name))
			#print self.dic
			
			try:
				skill_list = self.cfg.get("skill", "list")
			except ConfigParser.NoSectionError:
				#print "[ pc  ]", "reset skill / ",
				#print self.name.decode("utf-8").encode(sys.getfilesystemencoding())
				skill_list = ""
			# "10000000,10000001" --> [10000000, 10000001]
			self.skill_list = list(map(int, filter(None, skill_list.split(","))))
		
		except ConfigParser.NoOptionError, e:
			print e
	
	def saveallconfig(self, ConfigFileName):
		if self.wait_for_delete:
			return
		if ConfigFileName.find("..") != -1:
			return
		self.cfg = ConfigParser.SafeConfigParser()
		self.cfg.remove_section("main")
		self.cfg.add_section("main")
		self.cfg.set("main", "charid", str(self.charid))
		self.cfg.set("main", "name", str(self.name))
		self.cfg.set("main", "password", str(self.password))
		self.cfg.set("main", "delpassword", str(self.delpassword))
		self.cfg.set("main", "gmlevel", str(self.gmlevel))
		self.cfg.set("main", "race", str(self.race))
		self.cfg.set("main", "form", str(self.form))
		self.cfg.set("main", "gender", str(self.gender))
		self.cfg.set("main", "hair", str(self.hair))
		self.cfg.set("main", "haircolor", str(self.haircolor))
		self.cfg.set("main", "wig", str(self.wig))
		self.cfg.set("main", "face", str(self.face))
		self.cfg.set("main", "base_lv", str(self.base_lv))
		self.cfg.set("main", "ex", str(self.ex))
		self.cfg.set("main", "wing", str(self.wing))
		self.cfg.set("main", "wingcolor", str(self.wingcolor))
		self.cfg.set("main", "job", str(self.job))
		self.cfg.set("main", "map", str(self.map))
		self.cfg.set("main", "lv_base", str(self.lv_base))
		self.cfg.set("main", "lv_job1", str(self.lv_job1))
		self.cfg.set("main", "lv_job2x", str(self.lv_job2x))
		self.cfg.set("main", "lv_job2t", str(self.lv_job2t))
		self.cfg.set("main", "lv_job3", str(self.lv_job3))
		self.cfg.set("main", "gold", str(self.gold))
		self.cfg.set("main", "x", str(self.x))
		self.cfg.set("main", "y", str(self.y))
		self.cfg.set("main", "dir", str(self.dir))
		
		self.cfg.remove_section("status")
		self.cfg.add_section("status")
		self.cfg.set("status", "str", str(self.str))
		self.cfg.set("status", "dex", str(self.dex))
		self.cfg.set("status", "int", str(self.int))
		self.cfg.set("status", "vit", str(self.vit))
		self.cfg.set("status", "agi", str(self.agi))
		self.cfg.set("status", "mag", str(self.mag))
		self.cfg.set("status", "stradd", str(self.stradd))
		self.cfg.set("status", "dexadd", str(self.dexadd))
		self.cfg.set("status", "intadd", str(self.intadd))
		self.cfg.set("status", "vitadd", str(self.vitadd))
		self.cfg.set("status", "agiadd", str(self.agiadd))
		self.cfg.set("status", "magadd", str(self.magadd))
		
		self.cfg.remove_section("equip")
		self.cfg.add_section("equip")
		self.cfg.set("equip", "head", str(self.equip.head))
		self.cfg.set("equip", "face", str(self.equip.face))
		self.cfg.set("equip", "chestacce", str(self.equip.chestacce))
		self.cfg.set("equip", "tops", str(self.equip.tops))
		self.cfg.set("equip", "bottoms", str(self.equip.bottoms))
		self.cfg.set("equip", "backpack", str(self.equip.backpack))
		self.cfg.set("equip", "right", str(self.equip.right))
		self.cfg.set("equip", "left", str(self.equip.left))
		self.cfg.set("equip", "shoes", str(self.equip.shoes))
		self.cfg.set("equip", "socks", str(self.equip.socks))
		self.cfg.set("equip", "pet", str(self.equip.pet))
		
		self.cfg.remove_section("item")
		self.cfg.add_section("item")
		self.cfg.remove_section("sort")
		self.cfg.add_section("sort")
		for i in sorted(self.item, key=int):
			info = "%s,%s"%(self.item[i].id, self.item[i].count)
			self.cfg.set("item", str(i), info)
		sort = ""
		for i in self.sort.item:
			sort += ",%s"%i
		if len(sort) >1:
			sort = sort[1:]
		self.cfg.set("sort", "item", sort)
		
		self.cfg.remove_section("warehouse")
		self.cfg.add_section("warehouse")
		for i in sorted(self.warehouse, key=int):
			info = "%s,%s,%s"%(self.warehouse[i].id,
					self.warehouse[i].count, self.warehouse[i].warehouse)
			self.cfg.set("warehouse", str(i), info)
		sort_warehouse = ""
		for i in self.sort.warehouse:
			sort_warehouse += ",%s"%i
		if len(sort_warehouse) > 1:
			sort_warehouse = sort_warehouse[1:]
		self.cfg.set("sort", "warehouse", sort_warehouse)
		
		self.cfg.remove_section("dic")
		self.cfg.add_section("dic")
		for i in sorted(self.dic):
			self.cfg.set("dic", str(i), str(self.dic[i]))
		
		# [10000000, 10000001] --> "10000000,10000001"
		def list_to_str(l):
			def appendspliter(item):
				return "%s,"%item
			return "".join(map(appendspliter, l))
		self.cfg.remove_section("skill")
		self.cfg.add_section("skill")
		self.cfg.set("skill", "list", list_to_str(self.skill_list))
		#print list_to_str(self.skill_list)
		
		vmcfg = StringIO.StringIO()
		self.writehandle = open("./%s"%ConfigFileName, "wb")
		self.cfg.write(vmcfg)
		self.writehandle.write(vmcfg.getvalue().replace("\r\n", "\n").replace("\n", "\r\n"))
		self.writehandle.close()
	
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
	
	def makenewpc(self):
		newpc = PC(self.itemobj, self.itemdic)
		newpc.cfg = ConfigParser.SafeConfigParser()
		newpc.cfg.add_section("main")
		newpc.cfg.add_section("status")
		newpc.cfg.add_section("equip")
		newpc.cfg.add_section("sort")
		newpc.cfg.add_section("item")
		newpc.cfg.add_section("warehouse")
		newpc.cfg.add_section("dic")
		newpc.account = ""
		newpc.charid = 0
		newpc.sid = 0
		newpc.name = ""
		newpc.password = ""
		newpc.delpassword = ""
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
		newpc.str = 8
		newpc.dex = 3
		newpc.int = 3
		newpc.vit = 10
		newpc.agi = 4
		newpc.mag = 4
		newpc.stradd = 2
		newpc.dexadd = 1
		newpc.intadd = 1
		newpc.vitadd = 2
		newpc.agiadd = 1
		newpc.magadd = 1
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
	
	def pcinit(self):
		self.add("client", None) #None -> any type
		self.add("mapclient", None)
		self.add("account", "")
		self.add("charid", 0)
		self.add("sid", 0) #server id
		
		self.add("online", False) # online on mapserver
		self.add("online_login", False) #online on loginserver
		self.add("visible", False)
		self.add("loginevent", False)
		self.add("attacking", False)
		self.add("attacking_target", None)
		self.add("attacking_delay", 0)
		self.add("wait_for_delete", False)
		
		self.add("selectresult", None) #int or None
		self.add("motion", 111)
		self.add("effect", None)
		self.add("tradestate", 0)
		self.add("tradelist", [])
		self.add("tradereturnlist", [])
		self.add("isnpctrade", False)
		self.add("warehouse_open", None) #int or None
		self.add("e", None)
		
		self.add("name", "")
		self.add("password", "")
		self.add("delpassword", "")
		self.add("gmlevel", 0)
		self.add("race", 0)
		self.add("form", 0)
		self.add("gender", 0)
		self.add("hair", 0)
		self.add("haircolor", 0)
		self.add("wig", 0)
		self.add("face", 0)
		self.add("base_lv", 0)
		self.add("ex", 0)
		self.add("wing", 0)
		self.add("wingcolor", 0)
		self.add("job", 0)
		self.add("map", 0)
		self.add("lv_base", 0)
		self.add("lv_job1", 0)
		self.add("lv_job2t", 0)
		self.add("lv_job2x", 0)
		self.add("lv_job3", 0)
		self.add("gold", 0)
		
		self.add("str", 0)
		self.add("dex", 0)
		self.add("int", 0)
		self.add("vit", 0)
		self.add("agi", 0)
		self.add("mag", 0)
		self.add("stradd", 0)
		self.add("dexadd", 0)
		self.add("intadd", 0)
		self.add("vitadd", 0)
		self.add("agiadd", 0)
		self.add("magadd", 0)
		
		self.add("x", 0)
		self.add("y", 0)
		self.add("dir", 0)
		self.add("rawx", 0)
		self.add("rawy", 0)
		self.add("rawdir", 0)
		
		self.add("skill_list", [])
		self.add("item", {})
		self.add("warehouse", {})
		self.add("dic", {})
		self.add("battlestatus", 0)
		self.add("wrprank", 0)
		
		self.add("pet", None) #Pet()
		self.add("kanban", "")
		
		self.add("logout", False)
		self.add("sendmapserver", False)
		
		self.add("sort", self.SortClass())
		self.add("equip", self.EquipClass())
		self.add("status", self.StatusClass())

	class SortClass(DataAccessControl):
		def __init__(self):
			self.add("item", [])
			self.add("warehouse", [])
	class EquipClass(DataAccessControl):
		def __init__(self):
			self.add("head", 0)
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
	class StatusClass(DataAccessControl):
		def __init__(self):
			self.add("maxhp", 100)
			self.add("maxmp", 40)
			self.add("maxsp", 50)
			self.add("maxep", 30)
			self.add("hp", 100)
			self.add("mp", 40)
			self.add("sp", 50)
			self.add("ep", 30)
			
			self.add("minatk1", 100)
			self.add("minatk2", 100)
			self.add("minatk3", 100)
			self.add("maxatk1", 100)
			self.add("maxatk2", 100)
			self.add("maxatk3", 100)
			self.add("minmatk", 100)
			self.add("maxmatk", 100)
			
			self.add("leftdef", 50)
			self.add("rightdef", 30)
			self.add("leftmdef", 30)
			self.add("rightmdef", 20)
			self.add("shit", 7)
			self.add("lhit", 0)
			self.add("mhit", 7)
			self.add("chit", 0)
			self.add("savoid", 0)
			self.add("lavoid", 12)
			
			self.add("hpheal", 0)
			self.add("mpheal", 0)
			self.add("spheal", 0)
			self.add("aspd", 750) #190
			self.add("cspd", 187)
			self.add("speed", 410)
			self.add("adelay", 2*(1-self.aspd/1000.0)) #attack delay
			
			self.add("maxcapa", 1000)
			self.add("maxrightcapa", 0)
			self.add("maxleftcapa", 0)
			self.add("maxbackcapa", 0)
			self.add("maxpayl", 1000)
			self.add("maxrightpayl", 0)
			self.add("maxleftpayl", 0)
			self.add("maxbackpayl", 0)
			self.add("capa", 30)
			self.add("rightcapa", 0)
			self.add("leftcapa", 0)
			self.add("backcapa", 0)
			self.add("payl", 30)
			self.add("rightpayl", 0)
			self.add("leftpayl", 0)
			self.add("backpayl", 0)
