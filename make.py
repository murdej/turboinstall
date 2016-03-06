#!/usr/bin/env python

from os import listdir
from os.path import isfile, join

def readFileContents(fileName):
	with open(fileName, 'r') as fileHandle:
		return fileHandle.read()

def writeFileContents(fileName, content):
	with open(fileName, 'w') as fileHandle:
		fileHandle.write(content)
		fileHandle.close()


installScripts = ""
installScriptsPath = './installScripts'

for fileName in listdir(installScriptsPath):
	fileName = join(installScriptsPath, fileName)
	if isfile(fileName) and fileName.endswith('py'):
		print("Loading installScript '" + fileName + '"')
		installScripts += readFileContents(fileName)

mainTemplate = readFileContents('turboinstall.template.py')

writeFileContents('turboinstall.py', mainTemplate.replace('{{installScripts}}', installScripts))
