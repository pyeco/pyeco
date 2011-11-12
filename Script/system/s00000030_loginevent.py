#!/bin/python
# -*- coding: utf-8 -*-
from Object.eventobj import *

class Script:
	def get_id(self):
		event_id = []
		event_id.append("00000030")
		return event_id
	def main(self, pc):
		pass#do nothing
		systemmessage(pc, "---------------------------------------")
		systemmessage(pc, "pyeco 0.51.3 / 2011-11-13")
		systemmessage(pc, "./Script/system/s00000030_loginevent.py")
		systemmessage(pc, "---------------------------------------")