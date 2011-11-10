#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *
import random

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000776)
		return event_id

	def main(self,pc):
		say(pc, "不思議なところに行ってみたくない？？$R"+\
					"", "タイニー", 131)
		option = ["いってみたい", "いきたくない"]
		title = "？？？"
		result = select(pc, option, title)
		if result == 1:
			say(pc, "じゃあ目をつむってね！$R"+\
					"$P"+\
					"３つ数えるね。$R"+\
					"いーち、にーい・・・さー・・・・・・$R"+\
					"$P"+\
					"・・・・・・？？$R"+\
					"なんだか・・・眠くなってきた・・・・・・。$R"+\
					"$P"+\
					"・・・・・・。$R"+\
					"", "タイニー", 131)
			x = random.randint(244, 245)
			y = random.randint(82, 83)
			warp(pc, 10071000, x, y)
			#タイニーアイランド
		else:
			say(pc, "ふーん、そうなんだぁ、$R"+\
					"つまんないー。"+\
					"", "タイニー", 131)

	"""
	作者：brokentavern
	npcname：タイニー

	message
	”不思議なところに行ってみたくない？？”
	ok→select
		？？？
		1：いってみたい
		2：いきたくない

		→1：message
			”♪♪
			じゃあ目をつむってね！”
			next
			”３つ数えるね。
			いーち、にーい・・・さー・・・・・・”
			back　next
			”・・・・・・？？
			なんだか・・・眠くなってきた・・・・・・。”
			next
			”・・・・・・。”
			back　ok→warp：タイニーアイランド[10071000]（244,82）（244,83）（245,82）（245,83）

		→2:message
			”ふーん、そうなんだぁ、
			つまんないー。”
			ok→end
	"""



