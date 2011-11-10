#!/usr/bin/python
# -*- coding: utf-8 -*-
#License BSD
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
	
import os
import socket
import sys
import rijndael
try:
	import traceback
except ImportError, e:
	print "import error", e
	exceptinfo = sys.exc_info
else:
	exceptinfo = traceback.format_exc
	
class CryptIO:
	def encode(self,code,realcodesize=None):
		try:
			key = "00000000000000000000000000000000"
			key = key.decode("hex")
			code = code.decode("hex")
			if realcodesize == None:
				realcodesize = len(code)
			codesize = len(code)
			if codesize == 0:
				return None
			if codesize == 16:
				r = rijndael.rijndael(key, block_size = 16)
				code = r.encrypt(code)
			elif codesize > 16:
				while codesize % 16 != 0:
					code = code.encode("hex")
					code = code + "00"
					code = code.decode("hex")
					codesize = len(code)
				r = rijndael.rijndael(key, block_size = 16)
				text = ""
				while len(code) > 15:
					fragment = code[:16]
					code = code[16:]
					fragment = r.encrypt(fragment)
					text = text + fragment
				code = text
			elif codesize > 0 and codesize < 16:
				while codesize < 16:
					code = code.encode("hex")
					code = code + "00"
					code = code.decode("hex")
					codesize = len(code)
				r = rijndael.rijndael(key, block_size = 16)
				code = r.encrypt(code)
			length_raw = realcodesize
			length_crypt = ((codesize + 7) / 8)
			length_crypt = int(length_crypt)
			length_crypt = length_crypt * 8
			length_raw = hex(length_raw)
			length_crypt = hex(length_crypt)
			length_raw = length_raw[2:]
			length_crypt = length_crypt[2:]
			while len(length_raw) < 8:
				length_raw = "0" + length_raw
			while len(length_crypt) < 8:
				length_crypt = "0" + length_crypt
			#print length_raw, length_crypt
			length_raw = length_raw.decode("hex")
			length_crypt = length_crypt.decode("hex")
			data = length_crypt + length_raw + code
		except Exception:
			print "[crypt]","error on encode /", exceptinfo()
			data = None
		return data

	def decode(self,code):
		try:
			key = "00000000000000000000000000000000"
			key = key.decode("hex")
			if len(code) < 16:
				return None,None
			textlength = int(code[8:16],16)
			code = code[16:]
			code = code.decode("hex")
			codesize = len(code)
			if codesize == 0:
				return None,None
			if codesize % 16 != 0:
				print "error on decode: block size don't match",code.encode("hex")
				return None,None
			r = rijndael.rijndael(key, block_size = 16)
			if codesize > 16:
				text = ""
				while len(code) > 15:
					fragment = code[:16]
					code = code[16:]
					fragment = r.decrypt(fragment)
					text = text + fragment
			elif codesize == 16:
				text = r.decrypt(code)
			text = text.encode("hex")
		except Exception:
			print "[crypt]","error on decode /", exceptinfo()
			text,textlength = None,None
		return text,textlength
	
	