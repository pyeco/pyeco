#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11002276)
		return event_id

	def main(self,pc):
		say(pc, "我輩の見立てによると$R"+\
				"キミは冒険者のようだが・・・・・・$R"+\
				"$P"+\
				"ふむ、少々、力不足のようである。$R"+\
				"$R"+\
				"キミの知り合いに$R"+\
				"腕利きの冒険者がいれば。$R"+\
				"紹介したまえ。$R"+\
				"", "セラエノ", 131)

	"""
	作者：brokentavern
	npcname：セラエノ

	message
	”我輩の見立てによると
	キミは冒険者のようだが・・・・・・”
	next
	”ふむ、少々、力不足のようである。

	キミの知り合いに
	腕利きの冒険者がいれば。
	紹介したまえ。”
	back　ok→end
	"""

