#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000804)
		return event_id

	def main(self,pc):
		say(pc, "そんなへっぴり腰じゃ当たらねぇべ！$R"+\
				"ほ〜ら、これを受けてみろ！$R"+\
				"", "けんか好きなパイレーツ", 341)
		say(pc, "やられた〜！$R"+\
				"", "気の短いパイレーツ", 362, 11000805)

	"""
	作者：brokentavern
	npcname:けんか好きなパイレーツ

	///話かけると気の短いパイレーツに爆弾を投げる
	message
	”そんなへっぴり腰じゃ当たらねぇべ！
	ほ〜ら、これを受けてみろ！”
	ok→///押すと気の短いパイレーツが倒れる（2秒ほどで起き上がる）
	npcname:気の短いパイレーツ
	message
	”やられた〜”
	ok→end
	"""