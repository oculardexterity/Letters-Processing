import argparse
import jinja2
import os

from Stream import Stream

def to_snake_case(text):
	return text.replace(' ', '_')

def run_templater(inputFile, outputDir, tmpF):
	templateFile = open(tmpF).read() 
	env = jinja2.Environment()
	env.globals.update(sorted=sorted, to_snake=to_snake_case)

	template = env.from_string(templateFile)


	s = Stream(inputFile, 'Letter')
	for key, item in s.stream():
		templatedText = template.render(item)
		f = open(outputDir+key+".xml", 'w')
		f.write(templatedText)
		f.close()


if __name__ == '__main__':
	message = """
		Builds a shelve file or xlsx file into XML files using a specified template
	"""

	parser = argparse.ArgumentParser(description=message)
	parser.add_argument('--inputFilePath', '-i', help="Specify the path of an input file.")
	parser.add_argument('--outputDir', '-d', help="Specify the directory to output XML files")
	parser.add_argument('--templateFile', '-t', help="Specify a template to run")

	inputFilePath = parser.parse_args().inputFilePath
	outputDir = parser.parse_args().outputDir
	templateFile = parser.parse_args().templateFile

	if not (inputFilePath and outputDir and templateFile):
		raise ValueError('You are missing necessary arguments. Run --help for more information.')
	
	run_templater(inputFilePath, outputDir, templateFile)

