def handleUploadedFile(f):
    if f:
        print("File has been uploaded successfully!")
    with open(f, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def checkCSV(f):
    if f.name[-4:] == ".csv":
        print("File is .csv")
        return True
    else:
        print("File is not .csv")
        return False
