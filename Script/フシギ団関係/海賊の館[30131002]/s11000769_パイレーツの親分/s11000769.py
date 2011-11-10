#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000769)
		return event_id

	def main(self,pc):
		say(pc, "わっはっは！$R"+\
				"おいらはパイレーツの親分だ。$R"+\
				"ん、この奥に何があるかって？$R"+\
				"$P"+\
				"秘密だ、秘密！$R"+\
				"タイニーアイランドへの$R"+\
				"秘密の入り口なんて存在しないんだぞ！$R"+\
				"$R"+\
				"わかったら、あっちいけ！$R"+\
				"", "パイレーツの親分", 131)

	"""
	作者：brokentavern
	npcname:パイレーツの親分

	message
	”わっはっは！
	おいらはパイレーツの親分だ。
	ん、この奥に何があるかって？”
	next
	”秘密だ、秘密！
	タイニーアイランドへの
	秘密の入り口なんて存在しないんだぞ！

	わかったら、あっちいけ！”
	back　ok→end
	"""

