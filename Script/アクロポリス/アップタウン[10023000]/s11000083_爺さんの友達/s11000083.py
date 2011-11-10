#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000083)
		return event_id

	def main(self,pc):
		say(pc, "ハ・・・$R"+\
				"$P"+\
				"ハック！$R"+\
				"$P"+\
				"・・・・・・。$R"+\
				"$P"+\
				"（ムズムズ・・・・・・。）$R"+\
				"$P"+\
				"（ムズッ！？）$R"+\
				"$P"+\
				"フエッ・・・・・・。$R"+\
				"ハ・・・$R"+\
				"$P"+\
				"ハッ！$R"+\
				"$P"+\
				"ハック！$R"+\
				"$P"+\
				"・・・・・・。$R"+\
				"$P"+\
				"（でないか・・・・・・。）$R"+\
				"$P"+\
				"（う〜、すっきりしない！）$R"+\
				"$P"+\
				"（なんとか出ないかな？）$R"+\
				"$P"+\
				"（ムズムズ・・・・・・。）$R"+\
				"$P"+\
				"・・・・・・。$R"+\
				"$P"+\
				"（無理か。）$R"+\
				"$P"+\
				"ハーックション！！$R"+\
				"$P"+\
				"・・・・・・・・・・・・$R"+\
				"$P"+\
				"あー、すっきりした。$R"+\
				"", "爺さんの友達", 131)

	"""
	作者：brokentavern
	npcname：爺さんの友達

	message
	”ハ・・・”
	next
	”ハック！”
	back　next
	”・・・・・・。”
	back　next
	”（ムズムズ・・・・・・。）”
	back　next
	”（ムズッ！？）”
	back　next
	”フエッ・・・・・・。
	ハ・・・”
	back　next
	”ハッ！”
	back　next
	”ハック！”
	back　next
	”・・・・・・。”
	back　next
	”（でないか・・・・・・。）”
	back　next
	”（う〜、すっきりしない！）”
	back　next
	”（なんとか出ないかな？）”
	back　next
	”（ムズムズ・・・・・・。）”
	back　next
	”・・・・・・。”
	back　next
	”（無理か。）”
	back　next
	”ハーックション！！”
	back　next
	”・・・・・・・・・・・・”
	back　next
	”あー、すっきりした。”
	back　ok→end
	"""







