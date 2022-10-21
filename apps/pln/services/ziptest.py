import zipfile

path = "services/trainingandtestdata.zip"
zip_object = zipfile.ZipFile(file=path, mode="r")
zip_object.extractall("./data")
zip_object.close()
