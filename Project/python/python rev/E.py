#zip file open 
import zipfile 
archive = zipfile.ZipFile('D:\python-3.14-docs-html.zip','r')
imgfile = archive.open