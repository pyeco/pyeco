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
class Mob:
	def getmobdic(self, filename):
		mobdic={}
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
				mobid = int(row[0])
			except:
				continue
			mobdic[mobid]=Mob()
			mobdic[mobid].id = intx(row[0])
			mobdic[mobid].name = row[1]
		return mobdic
	
	def __init__ (self):
		self.id = 0
		self.sid = 0 #server id #ある程度を越えるとnpcとして見なされる
		self.charid = 0 #fake pc #equal server id
		self.name = ""
		self.map = 0
		self.x = 0
		self.y = 0
		self.dir = 0
		self.centerx = 0
		self.centery = 0
		self.rawx = 0
		self.rawy = 0
		self.rawdir = 0
		self.speed = 420
		self.hp = 100
		self.maxhp = 100
		self.mp = 1
		self.maxmp = 1
		self.sp = 1
		self.maxsp = 1
		self.ep = 0
		self.maxep = 0
		
		self.npc = False
		self.last_move_count = 0
		self.counter_attack_delay_count = 0
		self.moveable_area = 5
		self.die = 0 #hide after 5 sec
		self.damagedic = None #if set {} , will bug on copy.copy
