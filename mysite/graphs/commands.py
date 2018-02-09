from .forms import *
from csv import DictReader
def handleUploadedFile(f):
    if f:
        print("File has been uploaded successfully!")
        print("First character of file {x}".format(x = f.read(0)))
        for line in f:
            print(line.rstrip())
            break

def checkCSV(f):
    if f.name[-4:] == ".csv":
        print("File is .csv")
        return True
    else:
        print("File is not .csv")
        return False
