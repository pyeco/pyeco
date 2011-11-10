#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000070)
		return event_id

	def main(self,pc):
		say(pc, "きれいな花じゃのう。$R"+\
				"", "街のおじいさん", 131)

	"""
	作者：brokentavern
	npcname：街のおじいさん

	message
	”きれいな花じゃのう。”
	ok→end
	"""


