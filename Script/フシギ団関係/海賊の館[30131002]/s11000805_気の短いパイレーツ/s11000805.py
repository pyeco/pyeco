#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *
import random

class Script:
	def get_id(self):
		event_id = []
		event_id.append(11000805)
		return event_id

	def main(self,pc):
		x = random.randint(0, 99)
		if x < 50:
			say(pc, "フシギ団とケンカ！$R"+\
					"負けない、負けない！！$R"+\
					"", "気の短いパイレーツ", 255)
		else:
			say(pc,"打倒、フシギ団！！$R"+\
					"やつら、シマを狙う悪い奴！$R"+\
					"", "気の短いパイレーツ", 255)

	"""
	作者：brokentavern
	npcname:気の短いパイレーツ

	///1回目
	message
	”フシギ団とケンカ！
	負けない、負けない！！”
	ok→end

	///2回目
	message
	”打倒、フシギ団！！
	やつら、シマを狙う悪い奴！”
	ok→end

	///話すたびに1回目と2回目を交互に
	"""
