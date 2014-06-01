import re, os

def rePath(path):
	# clean the args of a path
	# clean the "\"" of a path
	try:
		# replace "system32" at the beginning of the string, most seen in drviers
		if (path[:8] == 'system32'):
			path = "%SystemRoot%\\" + path
		if (path[:11] == '\SystemRoot'):
			path = "%SystemRoot%" + path[11:]
	except:
		pass
	try:
		# replace the system var like %PATH%
		replace_array = re.findall('%[a-zA-Z0-9()]*%', path)
		for replace_pre in replace_array:
			replace_aft = os.environ.get(replace_pre[1:-1])
			path = path.replace(replace_pre, replace_aft)
	except:
		pass
	try:
		# clean path like ""C:\Program Files\VMware\VMware Tools\vmtoolsd.exe" -n vmusr"
		path = re.findall('\".*\"', path)[0]
		path = path[1:-1]
	except:
		pass
	try:
		# clean path like " C:\Windows\system32\userinit.exe,"
		path = re.match('[a-zA-Z]:.*\.[a-zA-Z]*', path).group(0)
	except:
		pass
	return path

def reFileName(name):
	# clean the extension of the filename
	try:
		name = re.match('[a-z]*(?=\.)', name).group(0)
		return name
	except:
		return name