import sys

IS_PY3 = sys.version_info[0] == 3
if IS_PY3:
	_range = range
	_input = input
	_unicode = str
else:
	_range = xrange
	_input = raw_input
	_unicode = unicode