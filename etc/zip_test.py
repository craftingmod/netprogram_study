import zipfile

zf = zipfile.ZipFile("sample.zip", "w")
zf.write("sample.xlsx")
zf.write("index.html")
zf.close()

uzf = zipfile.ZipFile("sample.zip", "r")
uzf.extractall(path="./extract")