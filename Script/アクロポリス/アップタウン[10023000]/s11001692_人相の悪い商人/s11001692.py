#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11001692)
		return event_id

	def main(self,pc):
		say(pc, "ゼェゼェ・・・・・・$R"+\
				"$R"+\
				"・・・・・・も、もう走れねえ・・・・・・。$R"\
				, "人相の悪い商人", 131)

	"""
	作者：brokentavern
	npcname：人相の悪い商人

	message
	”ゼェゼェ・・・・・・。

	・・・・・・も、もう走れねえ・・・・・・。”
	ok→end
	"""

