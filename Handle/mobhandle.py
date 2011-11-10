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
import time
import thread
import random
from Object.eventobj import *
try:
	import traceback
except ImportError, e:
	print "import error", e
	exceptinfo = sys.exc_info
else:
	exceptinfo = traceback.format_exc
	
class MobHandle:
	def __init__(self, serverobj):
		"""__init__"""
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		self.except_count = 0
	
	def get_new_point(self, mob, tox=None, toy=None, minx=-1, maxx=1, miny=-1, maxy=1):
		"""get new point"""
		if tox == None:
			movex = int(mob.x)+random.choice((minx, maxx))
		else:
			movex = int(tox)
		if toy == None:
			movey = int(mob.x)+random.choice((miny, maxy))
		else:
			movey = int(toy)
		centerx = int(mob.centerx)
		centery = int(mob.centery)
		moveable_area = int(mob.moveable_area)
		if movex > centerx+moveable_area:
			movex = centerx+moveable_area
		if movey > centery+moveable_area:
			movey = centery+moveable_area
		if movex < centerx-moveable_area:
			movex = centerx-moveable_area
		if movey < centery-moveable_area:
			movey = centery-moveable_area
		if movex < 0:
			movex = 0
		if movex > 255:
			movex = 255
		if movey < 0:
			movey = 0
		if movey > 255:
			movey = 255
		return movex, movey
	
	def move(self, mob, tox=None, toy=None):
		"""mob move"""
		if tox == None and toy == None:
			mob.last_move_count += 1
			if mob.last_move_count < 5:
				return
		mob.last_move_count = 0
		movex, movey = self.get_new_point(mob, tox, toy)
		#print "[ mob ]", "movemob", mob.x, mob.y, "->", movex, movey
		mobmove(mob, movex, movey, self.pclist, self.mapdic, \
				self.netio, self.createpacket)
	
	def get_active_map_list(self):
		"""プレイヤーがいるマップのリストを返す"""
		active_map_list = []
		for pc in self.pclist.itervalues():
			if not pc.online:
				continue
			if int(pc.map) not in active_map_list:
				active_map_list.append(int(pc.map))
		return active_map_list
	
	def clean_dead_mob(self, mob):
		"""clean dead mob"""
		delete_mob_list = []
		if mob.hp <= 0:
			mob.die += 1
		else:
			mob.die = 0
		if mob.die > 5:
			return mob.sid
		else:
			return None
	
	def delete_mob(self, delete_mob_list):
		"""delete mob"""
		#print "delete list", delete_mob_list
		for delete_sid in delete_mob_list:
			delete_mob = self.moblist.get(delete_sid)
			if delete_mob:
				#print "delete", delete_mob.sid
				#モンスター消去
				datatype,datacontent = self.createpacket.create1225(delete_sid)
				self.netio.sendmap(datatype, datacontent, self.pclist, delete_mob, None)
				del self.moblist[delete_sid]
	
	def counter_attack(self, mob):
		"""counter attack"""
		counter_attack_mode = False
		maxdamagefrom = 0
		maxdamage = 0
		for sid, damage in mob.damagedic.items():
			if damage >= maxdamage:
				maxdamage = damage
				maxdamagefrom = sid
		if not maxdamage:
			return counter_attack_mode
		#
		for p in self.pclist.itervalues():
			if not p.online:
				continue
			if int(p.map) != int(mob.map):
				continue
			if int(p.sid) == int(maxdamagefrom):
				pcx = int(p.x)
				pcy = int(p.y)
				mobcx = int(mob.centerx)
				mobcy = int(mob.centery)
				mobaa = int(mob.moveable_area)
				mobx = int(mob.x)
				moby = int(mob.y)
				tox = 0
				toy = 0
				diffcx = abs(pcx-mobcx)
				diffcy = abs(pcy-mobcy)
				diffx = abs(pcx-mobx)
				diffy = abs(pcy-moby)
				#print "pcx", pcx, "pcy", pcy,
				#print "mobcx", mobcx, "mobcy", mobcy,
				#print "mobaa", mobaa,
				#print "mobx", mobx, "moby", moby,
				#print "diffcx", diffcx, "diffcy", diffcy,
				#print "diffx", diffx, "diffy", diffy
				if diffcx > mobaa:
					break
				if diffcy > mobaa:
					break
				#
				counter_attack_mode = True
				if diffx <= 1 and diffy <= 1:
					mob.counter_attack_delay_count += 1
					if mob.counter_attack_delay_count <= 1:
						continue
					mob.counter_attack_delay_count = 0
					#攻撃結果
					datatype,datacontent = self.createpacket.create0fa1(mob, p, \
										0, 0, 1) #attacktype, damage, flag
					self.netio.sendmap(datatype, datacontent, self.pclist, mob, None)
				else:
					#move to pc
					if pcx > mobx:
						tox = mobx + 1
					else:
						tox = mobx - 1
					if pcy > moby:
						toy = moby + 1
					else:
						toy = moby - 1
					self.move(mob, tox, toy)
				#break
		return counter_attack_mode
	
	def thread_mobhandle(self):
		"""thread mobhandle"""
		with self.lock_print: #lock_print.acquire()	...	lock_print.release()
			print "[ all ]", "start thread_mobhandle"
			#time.sleep(10) #thread lock test (lock main thread)
		while True:
			try:
				with self.lock_moblist and self.lock_pclist:
					active_map_list = []
					delete_mob_list = []
					counter_attack_mode = None
					#
					active_map_list = self.get_active_map_list()
					#
					for mob in self.moblist.itervalues():
						#print mob.sid
						#clean dead mob
						data = self.clean_dead_mob(mob)
						if data:
							delete_mob_list.append(data)
						#
						if int(mob.map) not in active_map_list:
							#プレイヤーがいないマップのmobはここからの処理を行わない
							continue
						if mob.die:
							continue
						#counter attack
						counter_attack_mode = self.counter_attack(mob)
						#move
						if not counter_attack_mode:
							self.move(mob)
					#delete mob
					self.delete_mob(delete_mob_list)
					#self.lock release
				#print "sleep"
				time.sleep(1)
			except KeyboardInterrupt:
				print "[ all ]", "thread_mobhandle end"
				break
			except:
				self.except_count += 1
				print "[ mob ]", "thread_mobhandle error", exceptinfo()
				if self.except_count > 100:
					print "[ all ]", "thread_mobhandle end / except_count > 100"
					break
	
	
	
	
	
	
	