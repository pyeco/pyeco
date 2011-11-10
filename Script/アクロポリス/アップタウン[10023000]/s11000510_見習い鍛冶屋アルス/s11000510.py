#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000510)
		return event_id

	def main(self,pc):
		say(pc, "ああ、どうしよう・・・・・・。$R"+\
				"また材料が足りない・・・・・・。$R"+\
				"", "見習い鍛冶屋アルス", 131)
		#ここからは未実装

	"""
	作者：brokentavern
	npcname：見習い鍛冶屋アルス

	message
	”ああ、どうしよう・・・・・・。
	また材料が足りない・・・・・・。”
	ok
	///２回目以降はここから
	”『固い石ころ』１０個なきゃ・・・・・・。
	俺は、俺は・・・・・・。

	破滅だ・・・・・・。”
	ok→end

	※収集品と個数はランダム
	"""
