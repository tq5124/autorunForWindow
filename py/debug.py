import wmi
c = wmi.WMI ()

stopped_services = c.Win32_Service (StartMode="Auto")
if stopped_services:
  for s in stopped_services:
    print s.Caption, "service is not running"
else:
  print "No auto services stopped"