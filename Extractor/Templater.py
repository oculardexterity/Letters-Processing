import argparse
import jinja2
import os
from xml.etree import ElementTree as ET

from Stream import Stream

def to_snake_case(text):
	return text.replace(' ', '_')

def run_templater(inputFile, outputDir, templateFolder):
	wf = 0
	bf = 0

	letterPlainTemplateFile = open(templateFolder + 'letter_plain.xml').read()
	letterEnvelopeTemplateFile = open(templateFolder + 'letter_envelope.xml').read()
	postcardAMTemplateFile = open(templateFolder + 'postcard_am.xml').read()
	postcardIMTemplateFile = open(templateFolder + 'postcard_im.xml').read()


	s = Stream(inputFile, 'Letter')
	for key, item in s.stream():
		print(key, item["Type"])

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




		



		env = jinja2.Environment()
		env.globals.update(sorted=sorted, to_snake=to_snake_case)

		template = env.from_string(templateFile)


	
	
	# Dirty counter for well-formedness
	


	
		templatedText = template.render(item)
		f = open(outputDir+key+".xml", 'w')
		f.write(templatedText)
		f.close()

		# A dirty checker for wellformedness
		try:
			ET.fromstring(templatedText)
			wf += 1
		except Exception as e:
			print(key, " is BAD:: ", e)
			bf += 1

	print('GOOD: ', wf)
	print('BAD: ', bf)


if __name__ == '__main__':
	message = """
		Builds a shelve file or xlsx file into XML files using a specified template
	"""

	parser = argparse.ArgumentParser(description=message)
	parser.add_argument('--inputFilePath', '-i', help="Specify the path of an input file.")
	parser.add_argument('--outputDir', '-d', help="Specify the directory to output XML files")
	parser.add_argument('--templateFolder', '-t', help="Specify a template folder")

	inputFilePath = parser.parse_args().inputFilePath
	outputDir = parser.parse_args().outputDir
	templateFolder = parser.parse_args().templateFolder

	if not (inputFilePath and outputDir and templateFolder):
		raise ValueError('You are missing necessary arguments. Run --help for more information.')
	
	run_templater(inputFilePath, outputDir, templateFolder)

