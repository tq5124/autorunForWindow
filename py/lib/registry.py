import _winreg

def ReadRegistryValue(path, name="", start_key = None):
    # from http://code.activestate.com/recipes/578689-get-a-value-un-windows-registry/
    try:
        if (isinstance(path, str) or type(path) is unicode):
            path = path.split("\\")
        if start_key is None:
            start_key = getattr(_winreg, path[0])
            return ReadRegistryValue(path[1:], name, start_key)
        else:
            subkey = path.pop(0)
        try:
            with _winreg.OpenKey(start_key, subkey) as handle:
                assert handle
                if path:
                    return ReadRegistryValue(path, name, handle)
                else:
                    desc, i = None, 0
                    while not desc or desc[0] != name:
                        desc = _winreg.EnumValue(handle, i)
                        i += 1
                    return desc[1]
        except:
            return ""
    except:
        return ""

def ReadRegistryItems(hiveKey, key):
    """ Read all items under one key, return a array """
    # from http://stackoverflow.com/questions/5227107/python-code-to-read-registry
    data = []
    try:
        keyHandle = _winreg.OpenKey(hiveKey, key, 0, _winreg.KEY_READ)
        for i in xrange(0, _winreg.QueryInfoKey(keyHandle)[0]):
            try:
                skey_name = _winreg.EnumKey(keyHandle, i)
                data.append(skey_name)
            except:
                pass
    except:
        data = ""
    return data

def ReadRegistryKeys(hiveKey, key, sysBit=64):
    # read all keys under one key, return a dict
    data =[]
    try:
        aReg = _winreg.ConnectRegistry(None, hiveKey)
        sysBit = _winreg.KEY_WOW64_64KEY if sysBit == 64 else _winreg.KEY_WOW64_32KEY
        aKey = _winreg.OpenKey(aReg, key, 0, _winreg.KEY_READ | sysBit) 
        for i in range(1024):                                           
            try:
                n,v,t = _winreg.EnumValue(aKey,i)
                data.append([i,n,v,t])
            except EnvironmentError:
                break          
        _winreg.CloseKey(aKey)
    except:
        data = ""
    return data

def TestReadItems():
    outputData = ReadRegistryItems(_winreg.HKEY_LOCAL_MACHINE, "Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Browser Helper Objects")
    print outputData

def TestReadKeys():
    outputData = ReadRegistryKeys(_winreg.HKEY_LOCAL_MACHINE, "Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run", 32)
    print outputData

def TestReadValue():
    bios_vendor = ReadRegistryValue("HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\Terminal Server\\Wds\\rdpwd", "StartupPrograms")
    print bios_vendor
    
def readRegistry(method, hiveKey, key, name="", sysBit=64):
    fullKey = ""
    if (hiveKey == 'HKCR'):
        hiveKey = _winreg.HKEY_CLASSES_ROOT
        hive = "HKEY_CLASSES_ROOT"
    elif (hiveKey == 'HKCU'):
        hiveKey = _winreg.HKEY_CURRENT_USER
        hive = "HKEY_CURRENT_USER"
    elif (hiveKey == 'HKLM'):
        hiveKey = _winreg.HKEY_LOCAL_MACHINE
        hive = "HKEY_LOCAL_MACHINE"
    elif (hiveKey == 'HKU'):
        hiveKey = _winreg.HKEY_USERS
        hive = "HKEY_USERS"
    elif (hiveKey == 'HKCC'):
        hiveKey = _winreg.HKEY_CURRENT_CONFIG
        hive = "HKEY_CURRENT_CONFIG"
    else:
        return 'error'

    if (method == "readItems"):
        return ReadRegistryItems(hiveKey, key)
    elif (method == "readKeys"):
        return ReadRegistryKeys(hiveKey, key)
    elif (method == "readValue"):
        return ReadRegistryValue(key, name, hiveKey)
    else:
        return 'error'


if __name__ == "__main__":
    #Test()
    print 'test read items'
    TestReadItems()
    print 'test read keys'
    TestReadKeys()
    print 'test read value'
    TestReadValue()