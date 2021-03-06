from __future__ import print_function, division, absolute_import
from fontTools.misc.py23 import *
from fontTools.misc.textTools import safeEval
from . import DefaultTable
import struct

# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6ltag.html

class table__l_t_a_g(DefaultTable.DefaultTable):

	def decompile(self, data, ttFont):
		self.version, self.flags, numTags = struct.unpack(">LLL", data[:12])
		assert self.version == 1
		self.tags = []
		for i in range(numTags):
			pos = 12 + i * 4
			offset, length = struct.unpack(">HH", data[pos:pos+4])
			tag = data[offset:offset+length].decode("ascii")
			self.tags.append(tag)

	def compile(self, ttFont):
		dataList = [struct.pack(">LLL", self.version, self.flags, len(self.tags))]
		stringPool = ""
		for tag in self.tags:
			offset = stringPool.find(tag)
			if offset < 0:
				offset = len(stringPool)
				stringPool = stringPool + tag
			offset = offset + 12 + len(self.tags) * 4
			dataList.append(struct.pack(">HH", offset, len(tag)))
		dataList.append(stringPool)
		return bytesjoin(dataList)

	def toXML(self, writer, ttFont):
		writer.simpletag("version", value=self.version)
		writer.newline()
		writer.simpletag("flags", value=self.flags)
		writer.newline()
		for tag in self.tags:
			writer.simpletag("LanguageTag", tag=tag)
			writer.newline()

	def fromXML(self, name, attrs, content, ttFont):
		if not hasattr(self, "tags"):
			self.tags = []
		if name == "LanguageTag":
			self.tags.append(attrs["tag"])
		elif "value" in attrs:
			value =  safeEval(attrs["value"])
			setattr(self, name, value)
