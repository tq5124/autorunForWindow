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
			info = reg.readRegistry(item['method'], item['hiveKey'], item['path'], item['name'], item['sysBit'])
			try:
				assert(info)
				if (item['method'][-1:] == 's'):
					temp = []
					for i in info:
						name = i[1]
						path = pathCheck(i[2])
						fileInfo = files.getFileProperties(path)
						pub, desc = getDescPub(fileInfo)
						temp.append({
							"name": name,
							"path": path,
							"desc": desc,
							"pub": pub
						})
					output.append({
						"type": "keys",
						"path": item['hiveKey'] + "\\" + item['path'],
						"keys": temp
					})
				else:
					path = pathCheck(info)
					fileInfo = files.getFileProperties(path)
					output.append({
						"type": "key",
						"path": item['hiveKey'] + "\\" + item['path'],
						"keys": [{
							"name": info,
							"path": path,
							"desc": fileInfo['StringFileInfo']['FileDescription'],
							"pub": fileInfo['StringFileInfo']['CompanyName']
						}]
					})
				print 'done'
			except Exception, e:
				print 'failed: registry no found'
		elif (item['method'][:3] == 'sys'):
			# read and out from folder
			try:
				assert(info)
				path = pathCheck(item['path'])
				info = files.getAllFiles(path)
				temp = []
				for f in info:
					try:
						fileInfo = files.getFileProperties(path + '\\' + f)
						try:
							f_path = fileInfo['Path']
						except:
							pass
						pub, desc = getDescPub(fileInfo)
						temp.append({
							"name": f,
							"path": f_path,
							"desc": desc,
							"pub": pub
						})
					except: 
						pass
				output.append({
					"type": "files",
					"path": path,
					"keys": temp
				})
				print 'done'
			except:
				print 'failed: registry no found'

	# output to json
	with open('output/logon.js', 'w') as outfile:
		outfile.write("var logon = ")
		json.dump(output, outfile, indent=4)
	print

def service():
	print "Service:",
	print "reading from HKLM\\SYSTEM\\CurrentControlSet\\services...",
	output = []
	services = reg.readRegistry("readItems", "HKLM", "SYSTEM\\CurrentControlSet\\services")
	for item in services:
		serviceType = reg.readRegistry("readValue", "HKLM", "SYSTEM\\CurrentControlSet\\services\\" + item, "Type")
		serviceStart = reg.readRegistry("readValue", "HKLM", "SYSTEM\\CurrentControlSet\\services\\" + item, "Start")
		if (serviceType == "" or serviceType == 1 or serviceType == 2 or serviceStart == "" or serviceStart == 3 or serviceStart == 4):
			continue
		try:
			imagePath = reg.readRegistry("readValue", "HKLM", "SYSTEM\\CurrentControlSet\\services\\" + item + "\\Parameters", "ServiceDll")
			if imagePath == "":
				imagePath = reg.readRegistry("readValue", "HKLM", "SYSTEM\\CurrentControlSet\\services\\" + item, "ImagePath")
			imagePath = pathCheck(imagePath)
			fileInfo = files.getFileProperties(imagePath)
			pub, desc = getDescPub(fileInfo)
			output .append({
				"name": item,
				"path": imagePath,
				"desc": desc,
				"pub": pub
			})
		except:
			pass
	print "done"
	print
	with open('output/services.js', 'w') as outfile:
		outfile.write("var services = ")
		json.dump(output, outfile, indent=4)

def internetExplorer(input="json/interExplorer.json"):
	print "Explorer:"
	data = json.load(file(input))
	output = []
	for place in data:
		print "reading from ", place['reg'], "...",
		try:
			temp = []
			if (place['reg'].find('UrlSearchHook') > -1):
				allBHO = reg.readRegistry("readKeys", place['hiveKey'], place['reg'])
				print "\n***", allBHO
			else:
				allBHO = reg.readRegistry("readItems", place['hiveKey'], place['reg'])
			for bho in allBHO:
				if (type(bho) is list):
					bho = bho[1]
				clsid_name = reg.readRegistry("readValue", "HKLM", place['clsid'] + bho, "")
				clsid_path = reg.readRegistry("readValue", "HKLM", place['clsid'] + bho + "\\InprocServer32", "")
				fileInfo = files.getFileProperties(clsid_path)
				pub, desc = getDescPub(fileInfo)
				temp.append({
					"name": clsid_name,
					"path": clsid_path,
					"desc": desc,
					"pub": pub
				})
			print "done"
		except Exception, e:
			print "failed: registry no found"
		output.append({
			"reg": place['hiveKey'] + '\\' + place['reg'],
			"keys": temp
		})

	with open('output/internetExplorer.js', 'w') as outfile:
		outfile.write("var internetExplorer = ")
		json.dump(output, outfile, indent=4)
	print 

def drivers():
	print "drivers:"
	output = []
	print "reading from HKLM\\SYSTEM\\CurrentControlSet\\services ... ",
	services = reg.readRegistry("readItems", "HKLM", "SYSTEM\\CurrentControlSet\\services")
	for item in services:
		serviceType = reg.readRegistry("readValue", "HKLM", "SYSTEM\\CurrentControlSet\\services\\" + item, "Type")
		if (serviceType != 1):
			continue
		try:
			imagePath = reg.readRegistry("readValue", "HKLM", "SYSTEM\\CurrentControlSet\\services\\" + item, "ImagePath")
			imagePath = pathCheck(imagePath)
			fileInfo = files.getFileProperties(imagePath)
			pub, desc = getDescPub(fileInfo)
			output .append({
				"name": item,
				"path": imagePath,
				"desc": desc,
				"pub": pub
			})
		except:
			pass
	print "done"
	print
	with open('output/drivers.js', 'w') as outfile:
		outfile.write("var drivers = ")
		json.dump(output, outfile, indent=4)

def scheduledTasks():
	taskPath = "C:\Windows\Tasks"
	print "Secheduled Tasks:"
	print "reading from ", taskPath, "...",
	output = []
	allTasks = files.getAllFiles(taskPath)
	for item in allTasks:
		if (item[-4:] != '.job'):
			continue
		path = files.readAsBinary(taskPath + '\\' + item, 0x46)
		fileInfo = files.getFileProperties(path)
		pub, desc = getDescPub(fileInfo)
		output .append({
			"name": item,
			"path": path,
			"desc": desc,
			"pub": pub
		})
	print "done"
	print
	with open('output/scheduledTasks.js', 'w') as outfile:
		outfile.write("var scheduledTasks = ")
		json.dump(output, outfile, indent=4)

def bootExecute():
	regPath = "HKLM\System\CurrentControlSet\Control\Session Manager\BootExecute"
	print "Boot Execute:"
	print "read from ", regPath, "...",
	output = {}
	item = reg.readRegistry("readValue", "HKLM", "System\CurrentControlSet\Control\Session Manager", "BootExecute")
	item = item[0].split(' ')
	name = item[0]
	path = item[1]
	try:
		path = pathCheck(path)
		fileInfo = files.getFileProperties(path)
		pub, desc = getDescPub(fileInfo)
		output = {
			"name": name,
			"path": path,
			"desc": desc,
			"pub": pub
		}
	except:
		output = {
			"name": item,
			"path": '',
			"desc": '',
			"pub": ''
		}
	print "done"
	print
	with open('output/bootExecute.js', 'w') as outfile:
		outfile.write("var bootExecute = ")
		json.dump(output, outfile, indent=4)

def knownDlls():
	regPath = "HKLM\System\CurrentControlSet\Control\Session Manager\KnownDlls"
	print "Known Dlls:"
	print "read from ", regPath, "...",
	output = []
	allDlls = reg.readRegistry("readKeys", "HKLM", "System\CurrentControlSet\Control\Session Manager\KnownDlls")
	for item in allDlls:
		try:
			name = item[1]
			if (name.find('Directory') >= 0):
				continue
			path = pathCheck(item[2])
			pub, desc = getDescPub(files.getFileProperties(path))
			output.append({
				"name": name,
				"path": path,
				"desc": desc,
				"pub": pub
			})
		except:
			continue
	print "done"
	print
	with open("output/knownDlls.js", 'w') as outfile:
		outfile.write("var knownDlls = ")
		json.dump(output, outfile, indent=4)

def winsocket():
	regPath = "HKLM\System\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9"
	print "winsocket providers:"
	print "read from ", regPath, "...",
	output = []
	allsockets = reg.readRegistry("readItems", "HKLM", "System\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries")
	for item in allsockets:
		try:
			name = reg.readRegistry("readValue", "HKLM", "System\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries\\" + item, "ProtocolName")
			name = getWinsockName(name)
			text = reg.readRegistry("readValue", "HKLM", "System\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries\\" + item, "PackedCatalogItem")
			path = pathCheck(text[:text.find('.dll')] + ".dll")
			pub, desc = getDescPub(files.getFileProperties(path))
			output.append({
				"name": name,
				"path": path,
				"desc": desc,
				"pub": pub
			})
		except:
			continue
	print "done"
	print
	with open("output/winsocket.js", 'w') as outfile:
		outfile.write("var winsocket = ")
		json.dump(output, outfile, indent=4)

def winlogon(input='json/winLogon.json'):
	print "winlogon:"
	output = []
	data = json.load(file(input))
	for item in data:
		temp = []
		try:
			print "read from ", item['path'], '...',
			if (item['method'] == 'readValue'):
				name = item['name']
				path = reg.readRegistry(item['method'], item['hiveKey'], item['path'], item['name'], item['sysBit'])
				assert(path)
				path = pathCheck(path)
				pub, desc = getDescPub(files.getFileProperties(path))
				temp.append({
					"name": name,
					"path": path,
					"desc": desc,
					"pub": pub
				})
			elif (item['method'] == 'readItems'):
				allItems = reg.readRegistry(item['method'], item['hiveKey'], item['path'], item['name'], item['sysBit'])
				for i in allItems:
					name = i
					try:
						path = reg.readRegistry('readValue', 'HKLM', item['path'] + "\\" + i, 'DllName', item['sysBit'])
						assert(path)
					except:
						continue
					path = pathCheck(path)
					pub, desc = getDescPub(files.getFileProperties(path))
					temp.append({
						"name": name,
						"path": path,
						"desc": desc,
						"pub": pub
					})
			print "done"
			output.append({
				"path": item['hiveKey'] + '\\' + item['path'],
				"keys": temp,
				"type": 'key'
			})
		except:
			print "fail"
			output.append({
				"path": item['hiveKey'] + '\\' + item['path'],
				"keys": [],
				"type": 'unknow'
			})

	with open("output/winLogon.js", 'w') as outfile:
		outfile.write("var winLogon = ")
		json.dump(output, outfile, indent=4)

def imageHijacks(input='json/imageHijacks.json'):
	print "imageHijacks:"
	output = []
	data = json.load(file(input))
	for item in data:
		temp = []
		try:
			print "read from ", item['path'], '...',
			if (item['method'] == 'readValue'):
				name = item['name']
				path = reg.readRegistry(item['method'], item['hiveKey'], item['path'], item['name'], item['sysBit'])
				path = pathCheck(path)
				assert(path)
				pub, desc = getDescPub(files.getFileProperties(path))
				temp.append({
					"name": name,
					"path": path,
					"desc": desc,
					"pub": pub
				})
			elif (item['method'] == 'readItems'):
				allItems = reg.readRegistry(item['method'], item['hiveKey'], item['path'], '', item['sysBit'])
				for i in allItems:
					name = i
					try:
						path = reg.readRegistry('readValue', 'HKLM', item['path'] + "\\" + i, item['name'], item['sysBit'])
						assert(path)
					except:
						continue
					path = pathCheck(path)
					pub, desc = getDescPub(files.getFileProperties(path))
					temp.append({
						"name": name,
						"path": path,
						"desc": desc,
						"pub": pub
					})
			print "done"
			output.append({
				"path": item['hiveKey'] + '\\' + item['path'],
				"keys": temp,
				"type": 'key'
			})
		except:
			print "fail"
			output.append({
				"path": item['hiveKey'] + '\\' + item['path'],
				"keys": [],
				"type": 'unknow'
			})

	with open("output/imageHijacks.js", 'w') as outfile:
		outfile.write("var imageHijacks = ")
		json.dump(output, outfile, indent=4)


def getWinsockName(name):
	if (name.find(".dll") == -1):
		return name
	index = name.rfind("\\")
	name = name[index+1:]
	name = name.split(",")
	dict = {
		"wshtcpip.dll": {
			"-60100": "MSAFD Tcpip [TCP/IP]",
			"-60101": "MSAFD Tcpip [UDP/IP]",
			"-60102": "MSAFD Tcpip [RAW/IP]",
			"-60103": "Tcpip"
		},
		"wshqos.dll":{
			"-100": "RSVP TCPv6 Service Provider",
			"-101": "RSVP TCP Service Provider",
			"-102":	"RSVP UDPv6 Service Provider",
			"-103": "RSVP UDP Service Provider"
		},
		"wship6.dll":{
			"-60100": "MSAFD Tcpip [TCP/IPv6]",
			"-60101": "MSAFD Tcpip [UDP/IPv6]",
			"-60102": "MSAFD Tcpip [RAW/IPv6]"
		}
	}
	return dict[name[0]][name[1]]

def getDescPub(fileInfo):
	try:
		desc = fileInfo['StringFileInfo']['FileDescription']
	except:
		desc = ''
	try:
		pub = fileInfo['StringFileInfo']['CompanyName']
	except:
		pub = ''
	return pub, desc

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
	except:
		pass
	try:
		path = regex.rePath(path)
	except:
		pass
	return path


if __name__ == "__main__":
	# read system path files as a global resource
	systemPath('json/systemPath.json')

	# debug
<<<<<<< HEAD
	#internetExplorer()
=======
	#bootExecute()
>>>>>>> 79d55cdb9c568d0c9145acadf56e3f09d3e02371
	#exit()

	# read items from registry and folder
	logon('json/logon.json')
	service()
	internetExplorer()
	drivers()
	scheduledTasks()
	bootExecute()
	knownDlls()
	winsocket()
	winlogon()
	imageHijacks()

	print
	print "finish! open the index.html to see GUI output"