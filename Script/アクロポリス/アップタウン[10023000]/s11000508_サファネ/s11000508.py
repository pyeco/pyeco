#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000508)
		return event_id

	def main(self,pc,event):
		say(pc, "素敵ですわ、素敵ですわ！$R"+\
				"$R"+\
				"道行く人々がみんなオシャレ。$R"+\
				"さすがアクロポリスですわね〜。$R"+\
				"$P"+\
				"私、オシャレが大好きなんですの。$R"+\
				"洋服の素材を買いに来たんですけど$R"+\
				"なかなか売ってないんですのね。$R"+\
				"", "サファネ", 131)
		#ここからは未実装

	"""
	作者：brokentavern
	npcname：サファネ

	message
	”素敵ですわ、素敵ですわ！

	道行く人々がみんなオシャレ。
	さすがアクロポリスですわね〜。”
	next
	”私、オシャレが大好きなんですの。
	洋服の素材を買いに来たんですけど
	なかなか売ってないんですのね。”
	back　ok
	///２回目以降はここから
	”ふぅ、困ってしまいました・・・。

	『青い粉末』３個お持ちでしたら
	ゆずっていただけないかしら？”
	ok→end

	※収集品と個数はランダム
	"""



