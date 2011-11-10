#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000081)
		return event_id

	def main(self,pc):
		say(pc, "疲れたときはポーションに限るよな！$R"+\
				"$R"+\
				"食べ物みたいに、またなくていいし。$R"+\
				"便利、便利。$R"+\
				"", "爺さんの子供", 131)

	"""
	作者：brokentavern
	npcname：爺さんの子供

	message
	”疲れたときはポーションに限るよな！

	食べ物みたいに、またなくていいし。
	便利、便利。”
	ok→end
	"""

