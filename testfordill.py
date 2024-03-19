try:
    from dill.source import getsource
    print("Your system has dill installed.")
except:
    print("You must install the 'dill' package. The procedure to do this will vary.\nFor cygwin running Python 3.9, type: /usr/bin/python3.9 -m pip install dill")
