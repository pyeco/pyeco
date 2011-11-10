#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000509)
		return event_id

	def main(self,pc):
		say(pc, "・・・・・・久々のアクロポリスだ$R"+\
				"人の多さに、めまいがしてくるな。$R"+\
				"", "ソロ", 131)

	"""
	作者：brokentavern
	npcname:ソロ

	message
	”・・・・・・久々のアクロポリスだ。
	人の多さに、めまいがしてくるな。”
	ok
	///２回目以降はここから
	”・・・・・・。”
	next
	”『アーチンスロー』１７０個を
	持ってないか？”
	back　ok→end

	※収集品と個数はランダム
	"""

