#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000807)
		return event_id

	def main(self,pc):
		say(pc, "親分、なかの綿かえてくでよ。$R"+\
				"むにゃ、むにゃ･･････。$R"+\
				"", "寝ているパイレーツ", 255)

	"""
	作者：brokentavern
	npcname:寝ているパイレーツ

	message
	”親分、なかの綿かえてくでよ。
	むにゃ、むにゃ･･････。”
	ok→end
	"""

