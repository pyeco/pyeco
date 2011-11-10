#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000808)
		return event_id

	def main(self,pc):
		say(pc, "ここらのシマは、おいらたちのもの！$R"+\
				"飛空庭は勝手に使わせないぞ！$R"+\
				"", "休憩中のパイレーツ", 255)

	"""
	作者：brokentavern
	npcname:休憩中のパイレーツ

	message
	”ここらのシマは、おいらたちのもの！
	飛空庭は勝手に使わせないぞ！”
	ok→end
	"""

