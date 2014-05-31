import wmi

def getService(mode=""):
	c = wmi.WMI ()
	data =[]
	services = c.Win32_Service (StartMode=mode)
	for s in services:
		data.append({
			"name": s.Name,
			"path": s.PathName,
			"startMode": s.StartMode,
			"serviceType": s.ServiceType
		})
	return data

if __name__ == "__main__":
    services = getService('Auto')
    print services