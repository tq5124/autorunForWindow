import re

def rePath(path):
	# clean the args of a path
	# clean the "\"" of a path
	try:
		# clean path like ""C:\Program Files\VMware\VMware Tools\vmtoolsd.exe" -n vmusr"
		path = re.match('\".*\"', path).group(0)
		path = path[1:-1]
	except:
		pass
	try:
		# clean path like " C:\Windows\system32\userinit.exe,"
		path = re.match('[a-zA-Z].*[a-zA-Z]', path).group(0)
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