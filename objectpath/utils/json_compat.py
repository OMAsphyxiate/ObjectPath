#!/usr/bin/env python
try:
	import ujson as json
except ImportError:
	try:
		import json
	except ImportError:
		try:
			import simplejson as json
		except ImportError:
			raise Exception("JSONNotFound")

from objectpath import ITER_TYPES, STR_TYPES, py2JSON
from objectpath.utils.colorify import * # pylint: disable=W0614

load=json.load
def loads(s):
	if s.find("u'")!=-1:
		s=s.replace("u'","'")
	s=s.replace("'",'"')
	try:
		return json.loads(s) # ,object_hook=object_hook)
	except ValueError as e:
		raise Exception(str(e)+" "+s)

#def dumps(s,default=None):
#	return json.dumps(s,default=default, indent=2, separators=(',',':'))
dumps=json.dumps
dump=json.dump

LAST_LIST=None

def printJSON(o, length=5,depth=5):
	spaces=2

	def plus():
		currDepth[0]+=1

	def minus():
		currDepth[0]-=1

	def out(s):
		try:
			s=str(s)
		except Exception:
			pass
		if not ret:
			ret.append(s)
		elif ret[-1][-1]=="\n":
			ret.append(currDepth[0]*spaces*" "+s)
		else:
			ret.append(s)

	def rec(o):
		if type(o) in ITER_TYPES:
			o=list(o)
			if currDepth[0]>=depth:
				out("<array of "+str(len(o))+" items>\n")
			out("[")
			if len(o) > 0:
				if len(o) > 1:
					out("\n")
					plus()
				for i in o[0:length]:
					rec(i)
					out(",\n")

				if len(o)>length:
					out("... ("+str(len(o)-length)+" more items)\n")
				else:
					ret.pop()
					if len(o) > 1:
						out("\n")
				if len(o) > 1:
					minus()
			out("]")

		elif type(o) is dict:
			if currDepth[0]>depth:
				out("...\n")
			keys=o.keys()
			out("{")
			if len(keys) > 0:
				if len(keys) > 1:
					plus()
					out("\n")
				for k in o.keys():
					out(string('"'+str(k)+'"')+": ")
					rec(o[k])
					out(",\n")
				ret.pop()
				if len(keys) > 1:
					minus()
					out("\n")
			out("}")
		else:
			if type(o) in [int,float]:
				out(const(o))
			elif o in [None, False, True]:
				out(const(py2JSON(o)))
			elif type(o) in STR_TYPES:
				out(string('"'+o+'"'))
			else:
				out(string(o))

	currDepth=[0]
	ret=[]
	rec(o)
	currDepth[0]=0
	return "".join(ret)
