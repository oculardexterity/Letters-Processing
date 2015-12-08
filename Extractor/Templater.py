import argparse
import collections
import datetime
import jinja2
import os
import shelve
from xml.etree import ElementTree as ET

from Stream import Stream



def to_snake_case(text):
	return text.replace(' ', '_')

def replace_contrib_names(name):
	with shelve.open('editorList.shelve') as editor_list:
		if name in editor_list:
			return editor_list[name][1]
		else:
			return name.replace(" ","").replace("'"," ")

def run_templater(inputFile, outputDir):#, templateFolder):
	editors = []
	contributors = []
	wf = 0
	bf = 0
	'''
	letterPlainTemplateFile = open(templateFolder + 'letter_plain.xml').read()
	letterEnvelopeTemplateFile = open(templateFolder + 'letter_envelope.xml').read()
	postcardAMTemplateFile = open(templateFolder + 'postcard_am.xml').read()
	postcardIMTemplateFile = open(templateFolder + 'postcard_im.xml').read()
	'''

	s = Stream(inputFile, 'Letter')
	
	for key, item in s.stream():
		print("Templating item: ", key, "-type ", item["Type"])
		'''
		if item["Type"] == 'Letter':
			print(item["Pages"])
			if [p for k, p in item["Pages"].items() if p["PageType"] == 'EnvelopeType']:
				templateFile = letterEnvelopeTemplateFile
			else:
				templateFile = letterPlainTemplateFile
		elif item["Type"] == 'PostcardAM':
			templateFile = postcardAMTemplateFile
		elif item["Type"] == 'PostcardIM':
			templateFile = postcardIMTemplateFile
		else:
			templateFile = letterPlainTemplateFile




		
		'''
		item["ProcessingVersion"] = "2"

		#print(len(item["Contributor_List"]), set(item["Contributor_List"]))
		new_cont_list = []
		item["Editors"] = []  
		with shelve.open('editorList.shelve') as editor_list:
			
			for editor in item["Contributor_List"]:
				if editor in editor_list and "Python" not in editor:
					if editor_list[editor] != ("Susan Schreibman", "SS"):
						item["Editors"].append(editor_list[editor])
				elif editor != "NULL":
					new_cont_list.append(editor)

		item["Contributor_List"] = new_cont_list

		#contributors += item["Contributor_List"]
		template_log = { 
					'editType': 'TEI template built', 
					'editor': "PythonScript", 
					'datetime': str(datetime.datetime.now())[:-7].replace(" ", "T")}

		item["Edits"].append(template_log)

		item["Edits"] = sorted(item["Edits"], key=lambda f: datetime.datetime.strptime(f['datetime'], "%Y-%m-%dT%H:%M:%S"))

		

		templateFile = open('newTemplate.xml').read()

		env = jinja2.Environment()
		env.globals.update(sorted=sorted, to_snake=to_snake_case,replace_contribs=replace_contrib_names) 

		template = env.from_string(templateFile)


	
	
	
	


		#print(item["Letter"])

		#for k, v in item.items():
		#	print(k, type(k), v)
		del item[None]

		templatedText = template.render(item)
		f = open(outputDir+key+".xml", 'w')

		#f = open("pagesList.xml", 'a')
		f.write(templatedText)
		f.close()

		# A dirty checker for wellformedness
		try:
			ET.fromstring(templatedText)
			wf += 1
		except Exception as e:
			#print(key, " is BAD:: ", e)
			bf += 1

	#print('GOOD: ', wf)
	#print('BAD: ', bf)
	#print(editors)
	#print(list(set(contributors)))

if __name__ == '__main__':
	message = """
		Builds a shelve file or xlsx file into XML files using a specified template
	"""

	parser = argparse.ArgumentParser(description=message)
	parser.add_argument('--inputFilePath', '-i', help="Specify the path of an input file.")
	parser.add_argument('--outputDir', '-d', help="Specify the directory to output XML files")
	#parser.add_argument('--templateFolder', '-t', help="Specify a template folder")

	inputFilePath = parser.parse_args().inputFilePath
	outputDir = parser.parse_args().outputDir
	#templateFolder = parser.parse_args().templateFolder

	if not (inputFilePath and outputDir): #and templateFolder):
		raise ValueError('You are missing necessary arguments. Run --help for more information.')
	
	run_templater(inputFilePath, outputDir)#, templateFolder)

