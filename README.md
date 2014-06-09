# autorunForWindow

check auto run services and process by searching in registry and folders, tested on Window7/64, python 2.7.4/64

## Install

requried

* python 2.7 64bit
* pywin32 64bit
* window7 64bit(I have not tested the 32bit, but I think it works)

## Run

wget https://github.com/tq5124/autorunForWindow/archive/1.0.tar.gz
tar -xf autorunForWindow-1.0.tar.gz
cd autorunForWindow-1.0/py
python autorun.py
cd ..
//open the index.html in brower

## lib api

It will be pleaced if anyone need lib file here

* py/lib/registry.py
    * readRegistry(method, hiveKey, key, name="", sysBit=64)
        * method
            * "readValue": read a value from registry
            * "readItems": read all subkeys
            * "readKeys": read all values
        * hiveKey
            * "HKLM": read the HKEY_LOCAL_MACHINE
            * else: just the same
        * key
            * the path of key in registry
            * eg: "Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"
        * name
            * only used in readValue
        * sysBit
            * firstly designed for [window registry redirection](http://msdn.microsoft.com/en-us/library/windows/desktop/aa384232(v=vs.85).aspx), because I try to run a 32bit python in window 64. Now this arg has been **abandoned**!
* py/lib/filespy
    * getFileProperties(path)
        * give the path and return a dict of file informations
        * copy from [stackoverflow](http://stackoverflow.com/a/7993095/2301667), thanks `Helmut N.`
    * getAllFiles(path)
        * read all files under the path
    * readAsBinary(path, offset)
        * path
            * the path of the file to read
        * offset
            * begin at the offset
            * read 2 byte as length
            * read (length) byte from the rest of the file
* py/lib/regex.py
    * rePath(path)
        * reform the path, please check the comment in the file for more information
    * reFileName(name)
        * clean the extension name
