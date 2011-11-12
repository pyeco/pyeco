#!/usr/bin/python
# -*- coding:utf-8 -*-
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
import threading
import traceback
import inspect
#self.__dict__[name_VALUE] = value
#self.__dict__[name_TYPE] = value_type
PYTHON_TYPE = [str, int, float, list, dict, tuple, type, bool] #object
class DataAccessControl:
	def initDataAccessControl():
		pass
	def raise_when_exist(self, key_name, key_type):
		if key_name in self.__dict__:
			raise AttributeError, "%s exist"%key_name
		elif key_type in self.__dict__:
			raise AttributeError, "%s exist"%key_type
	def raise_when_not_exist(self, key_name, key_type):
		if key_name not in self.__dict__:
			raise AttributeError, "%s not exist"%key_name
		elif key_type not in self.__dict__:
			raise AttributeError, "%s not exist"%key_type
	def transform_value_type(self, value, value_type):
		if value_type != None and type(value) != value_type:
			return value_type(value)
		else:
			return value
	def add(self, name, value):
		if type(value) not in PYTHON_TYPE:
			value_type = None #any type
		else:
			value_type = type(value)
		#print "add", name, value, value_type
		key_name, key_type = "%s_VALUE"%name, "%s_TYPE"%name
		self.raise_when_exist(key_name, key_type)
		value = self.transform_value_type(value, value_type)
		self.__dict__[key_name] = value
		self.__dict__[key_type] = value_type
	def __getattr__(self, name):
		"""only called for things that Python can't find in __dict__"""
		#print "__getattr__", name
		key_name, key_type = "%s_VALUE"%name, "%s_TYPE"%name
		self.raise_when_not_exist(key_name, key_type)
		value = self.__dict__[key_name]
		value_type = self.__dict__[key_type]
		value = self.transform_value_type(value, value_type)
		return value
	def __setattr__(self, name, value):
		#print "__setattr__", name, value
		key_name, key_type = "%s_VALUE"%name, "%s_TYPE"%name
		self.raise_when_not_exist(key_name, key_type)
		value_type = self.__dict__[key_type]
		value = self.transform_value_type(value, value_type)
		self.__dict__[key_name] = value
	def __delattr__(self, name):
		#print "__delattr__", name
		key_name, key_type = "%s_VALUE"%name, "%s_TYPE"%name
		self.raise_when_not_exist(key_name, key_type)
		del self.__dict__[key_name]
		self.__dict__[key_name] = self.__dict__[key_type]