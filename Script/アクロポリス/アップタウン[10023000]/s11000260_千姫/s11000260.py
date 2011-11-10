#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000260)
		return event_id

	def main(self, pc):
		say(pc, "ウフフフフ・・・・・・。$R"+\
				"", "千姫", 131)

	"""
	作者：brokentavern
	npcname：千姫

	message
	”ウフフフフ・・・・・・。”
	ok→end
	"""


