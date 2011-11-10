#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000155)
		return event_id

	def main(self,pc):
		say(pc, "私の名前は、エリーナ。$R"+\
				"エミルの世界に興味があって$R"+\
				"いろいろ見てまわってるんだ。$R"+\
				"$P"+\
				"もう少しキミが強くなったら$R"+\
				"イイこと教えて、あ・げ・る♪$R"+\
				"$R"+\
				"約束ね！$R"+\
				"", "エリーナ", 131)

	"""
	作者：brokentavern
	npcname：エリーナ

	message
	”私の名前は、エリーナ。

	エミルの世界に興味があって
	いろいろ見てまわってるんだ。”
	next
	”もう少しキミが強くなったら
	イイこと教えて、あ・げ・る♪

	約束ね！”
	back　ok→end
	"""


