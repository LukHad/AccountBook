import nose
import os
import glob

test_files = glob.glob('test_*.py')
os.system("nosetests " + " ".join(test_files))



