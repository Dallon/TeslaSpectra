import os
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/foobar.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/
print(script_dir)
var = '/json/storedpatentname.json'
print(script_dir + var)
