#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000085)
		return event_id

	def main(self,pc):
		say(pc, "こんにちわ。どこに行くの？$R"+\
				"", "爺さんの彼女", 131)

	"""
	作者：brokentavern
	npcname：爺さんの彼女

	message
	”こんにちわ。どこに行くの？”
	ok→end
	"""


