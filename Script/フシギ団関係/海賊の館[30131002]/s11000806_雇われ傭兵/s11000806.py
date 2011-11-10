#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000806)
		return event_id

	def main(self,pc):
		say(pc, "俺は、あのタイニーに雇われた傭兵だ。$R"+\
				"金払いも悪くない。$R"+\
				"しばらくの間は、ここにいるつもりだ。$R"+\
				"", "雇われ傭兵", 131)

	"""
	作者：brokentavern
	npcname:雇われ傭兵

	message
	”俺は、あのタイニーに雇われた傭兵だ。
	金払いも悪くない。
	しばらくの間は、ここにいるつもりだ。”
	ok→end
	"""

