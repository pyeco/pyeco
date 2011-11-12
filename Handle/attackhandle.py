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
import os
import sys
import time
import thread
from Object import eventobj
import traceback

class AttackHandle(DataAccessControl):
	def __init__(self):
		pass
	
	def init(self, serverobj):
		# set itemdic, mapdic, etc...
		serverobj.setlibdic(serverobj.libdic, self)
		self.add("except_count", 0)
		self.add("send", self.netio.send)
		self.add("sendmap", self.netio.sendmap)
		self.add("sendmapwithoutself", self.netio.sendmapwithoutself)
		self.add("sendserver", self.netio.sendserver)
		#self.oldtime = time.time()
	
	def attackmob(self, pc, targetsid):
		#print "attack", targetsid
		with self.lock_moblist:
			target = self.moblist.get(targetsid)
			if target == None:
				print "[ map ]", "AttackThread.attack error / mob not exist", targetsid
				pc.reset_attack_info()
				return
			if target.hp <= 0:
				#print "[ map ]", "AttackThread.attack cheat detect / mob hp < 0", pc.account, targetsid
				pc.reset_attack_info()
				return
			if not target.damagedic.get(pc.sid):
				target.damagedic[pc.sid] = 0
			damage = 10
			target.damagedic[pc.sid] += damage
			target.hp -= damage
			if target.hp < 0:
				target.hp = 0
			state01 = 0
			flag = 1 #HPダメージ
			if target.hp <= 0:
				state01 = 0x200 #行動不能
				flag = 0x4001 #HPダメージ + 消滅モーション
			#攻撃結果
			datatype,datacontent = self.createpacket.create0fa1(pc, target, \
									0, damage, flag) #attacktype, damage, flag
			self.sendmap(datatype, datacontent, self.pclist, pc, None, True)
			#現在のHP/MP/SP/EP
			datatype,datacontent = self.createpacket.create021c(target, True)
			self.sendmap(datatype, datacontent, self.pclist, pc, None, True)
			#モンスターの状態
			datatype,datacontent = self.createpacket.create157c(target, state01)
			self.sendmap(datatype, datacontent, self.pclist, pc, None, True)
			if target.hp <= 0:
				pc.reset_attack_info()
				maxdamagefrom = 0
				maxdamage = 0
				for sid, damage in target.damagedic.items():
					if damage >= maxdamage:
						maxdamage = damage
						maxdamagefrom = sid
				for p in self.pclist.itervalues():
					if not p.online:
						continue
					if int(p.map) != int(target.map):
						continue
					if int(p.sid) == int(maxdamagefrom):
						eventobj.systemmessage(p, "基本経験値 0、職業経験値 0を取得しました", True)
	
	def thread_attackhandle(self):
		"""thread attack"""
		with self.lock_print: #lock_print.acquire()	...	lock_print.release()
			print "[ all ]", "start thread_attackhandle"
			#time.sleep(10) #thread lock test (lock main thread)
		while True:
			try:
				with self.lock_pclist:
					for p in self.pclist.itervalues():
						if not p.attacking:
							continue
						if p.attacking_target == None:
							continue
						#print "p.attacking_delay", p.attacking_delay,
						#print "p.status.adelay", p.status.adelay
						p.attacking_delay += 0.03
						#p.attacking_delay += time.time() - self.oldtime
						if p.attacking_delay < p.status.adelay:
							continue
						#print "attack"
						p.attacking_delay -= p.status.adelay
						self.attackmob(p, p.attacking_target)
				#self.oldtime = time.time()
				time.sleep(0.03)
			except KeyboardInterrupt:
				print "[ all ]", "thread_attackhandle end"
				break
			except:
				self.except_count += 1
				print "[ mob ]", "thread_attackhandle error", traceback.format_exc()
				if self.except_count > 100:
					print "[ all ]", "thread_attackhandle end / except_count > 100"
					break