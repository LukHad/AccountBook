import nose
import os

test_files = ["tests.test_TransactionBook",
              "tests.test_Filter"]


os.system("nosetests " + " ".join(test_files))



