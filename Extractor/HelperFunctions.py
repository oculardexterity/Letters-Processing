import re

def extractTagContents(text,tag):
	try:
		return re.findall(r'(?<=<' + tag + r'>)[\s\S]*(?=</' + tag + r'>)', text)
	except TypeError:
		raise