'''
2014.05
done by tq5124
https://github.com/tq5124
'''

import json
import lib.registry as reg
import lib.files as files
import lib.regex as regex

gl = {}

def logon(input='json/logon.json'):
	print "Logon:"
	data = json.load(file(input))
	output = []
	for item in data:
		# different method to read details, like registry or folders
		print "read from ", item['path'], '...',
		if (item['method'][:4] == 'read'):
			# read and out from registry
			info = reg.readRegistry(item['method'], item['hiveKey'], item['path'], item['name'])
			try:
				if (item['method'][-1:] == 's'):
					temp = []
					for i in info:
						name = i[1]
						path = pathCheck(i[2])
						fileInfo = files.getFileProperties(path)
						try:
							desc = fileInfo['StringFileInfo']['FileDescription']
							pub = fileInfo['StringFileInfo']['CompanyName']
						except:
							desc= ''
							pub = ''
						temp.append({
							"name": name,
							"path": path,
							"Description": desc,
							"Publisher": pub
						})
					output.append({
						"*": "keys",
						"path": item['hiveKey'] + "\\" + item['path'],
						"keys": temp
					})
				else:
					path = pathCheck(info)
					fileInfo = files.getFileProperties(path)
					output.append({
						"*": "key",
						"path": item['hiveKey'] + "\\" + item['path'],
						"name": info,
						"path": path,
						"Description": fileInfo['StringFileInfo']['FileDescription'],
						"Publisher": fileInfo['StringFileInfo']['CompanyName']
					})
				print 'done'
			except Exception, e:
				print 'failed: ', info, e
		elif (item['method'][:3] == 'sys'):
			# read and out from folder
			path = pathCheck(item['path'])
			info = files.getAllFiles(path)
			temp = []
			for f in info:
				try:
					fileInfo = files.getFileProperties(path + '\\' + f)
					try:
						path = fileInfo['Path']
					except:
						pass
					try:
						desc = fileInfo['StringFileInfo']['FileDescription']
					except:
						desc = ''
					try:
						pub = fileInfo['StringFileInfo']['CompanyName']
					except:
						pub = ''
					temp.append({
						"name": f,
						"path": path,
						"Description": desc,
						"Publisher": pub
					})
				except: 
					pass
			output.append({
				"*": "files",
				"path": path,
				"keys": temp
			})
			print 'done'


	# output to json
	print 
	print "writting into output/logon.json ...",
	with open('output/logon.json', 'w') as outfile:
		json.dump(output, outfile, indent=4)
	print 'done'
	print

def systemPath(input='json/systemPath.json'):
	print 'reading system path files ...',
	gl['systemPath'] = {}
	data = json.load(file(input))
	for path in data:
		temp = files.getAllFiles(path)
		for i in temp:
			j = regex.reFileName(i)
			gl['systemPath'][j] = path + '\\' + i
	print 'done'
	print 
	return

def pathCheck(path):
	try:
		if (path.find('\\') < 0):
			# if only *.* provided, first change to *, then find path
			path = regex.reFileName(path)
			path = gl['systemPath'][path]
		path = regex.rePath(path)
	except:
		path = ''
	return path


if __name__ == "__main__":
	# debug
	# print fileInfo()
	# print reg.readRegistry('readValue', 'HKLM', 'System\\CurrentControlSet\\Control\\Terminal Server\\Wds\\rdpwd', 'StartupPrograms')
	#exit()
	
	# read system path files as a global resource
	systemPath('json/systemPath.json')

	# read logon items from registry and folder
	logon('json/logon.json')