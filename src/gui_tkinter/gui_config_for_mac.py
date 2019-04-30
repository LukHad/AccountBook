from sys import platform

# <start> Configure the Application menubar entry for Mac (Python -> Appname)
# requirements:
#   pyobjc==4.1; pip3 install pyobjc; installs several other moduls
if platform == 'darwin':
    from Foundation import NSBundle
    bundle = NSBundle.mainBundle()
    if bundle:
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info and info['CFBundleName'] == 'Python':
            info['CFBundleName'] = "AccountBook"
# <end>
