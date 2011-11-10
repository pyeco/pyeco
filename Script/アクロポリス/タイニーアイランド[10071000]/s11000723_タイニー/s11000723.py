#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *
import random

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000723)
		return event_id

	def main(self,pc):
		say(pc, "こんにちわ！$R"+\
				"", "タイニー", 131)
		say(pc, "どうする？$R"+\
				"タイニーアイランドから出る？$R"+\
				"", "タイニー", 131)
		option = ["帰る", "やめておく"]
		title = "どうする？"
		result = select(pc, option, title)
		if result == 1:
			say(pc, "えー？$R"+\
					"本当に帰っちゃうのー？$R"+\
					"", "タイニー", 131)
			option01 = ["帰る", "やめておく"]
			title01 = "どうする？"
			result01 = select(pc, option, title)
			if result01 == 1:
				say(pc, "そっかぁー。$R"+\
						"じゃあしょうがないね。$R"+\
						"$R"+\
						"君を元の世界に帰してあげるよ。$R"+\
						"$P"+\
						"タイニーアイランドはみんなの夢の国！$R"+\
						"$R"+\
						"またいつでも来てね！$R"+\
						"待ってるからね♪$R"+\
						"", "タイニー", 131)
				x = random.randint(126, 127)
				y = random.randint(149, 150)
				warp(pc, 10023000, x, y)
				#アップタウン
			else:
				pass
		else:
			pass

	"""
	作者：brokentavern
	npcname：タイニー

	message
	”こんにちわ！”
	ok
	”どうする？
	タイニーアイランドから出る？”
	ok→select
		どうする？
		1：帰る
		2：やめておく

		→1：message
			”えー？
			本当に帰っちゃうのー？”
			ok→select
				どうする？
				1：帰る
				2：やめておく

				→1：message
					”そっかぁー。
					じゃあしょうがないね。

					君を元の世界に帰してあげるよ。”
					next
					”タイニーアイランドはみんなの夢の国！

					またいつでも来てね！
					待ってるからね♪”
					back　ok→warp：アップタウン[10023000]（126,149）（127,149）（126,150）（127,150）

				→2:end

		→2:end
	"""




