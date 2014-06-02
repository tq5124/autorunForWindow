import os, struct
import win32api, win32com.client 

def getFileProperties(fname):
    # from http://stackoverflow.com/a/7993095/2301667

    """
    Read all properties of the given file return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
    
    # if *.lnk, redirect to the real file
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(fname)
        fname = shortcut.Targetpath
        props = getFileProperties(fname)
        props['Path'] = fname
        return props
    except:
        pass
    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struct
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        props = {}

    return props

def getAllFiles(path):
    try:
        return os.listdir(path)
    except:
        return 'error'

def readAsBinary(path, offset):
    try:
        with open(path, 'rb') as file_t:
            file_t.read(offset)
            length = struct.unpack("h", file_t.read(2))
            return file_t.read(length[0]*2)[::2]
    except Exception, e:
        print e
        return ""

if __name__ == "__main__":
    print readAsBinary("C:\Windows\Tasks\GoogleUpdateTaskMachineCore.job", 0x46)
    #print getFileProperties("C:\Windows\system32\DRIVERS\WUDFRd.sys")