import argparse
from datetime import datetime
import os
import sys

from Processor import Processor as Processor
from EditLogger import EditLogger

editLogger = EditLogger()



class RemovePageDuplicates(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self.pageDuplicatesResolve
		self.transform = self.pageDuplicatesTransform
		self.dict_key = 'Page'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		super().__init__()

	@editLogger('Old page dublicate removed', 'PythonScript_pageDublicatesResolve')
	def pageDuplicatesResolve(self, old, new):
		if old['Translation_Timestamp'] >= new['Translation_Timestamp']:
			return old
		elif new['Translation_Timestamp'] >= old['Translation_Timestamp']:
			return new

	@editLogger('New page instance created', 'PythonScript_pageDuplicatesTransform')
	def pageDuplicatesTransform(self, field):
		return field




class MergeLetterPages(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self.mergeLetterPagesResolve
		self.transform = self.mergeLetterPagesTransform
		self.dict_key = 'Letter'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		super().__init__()


	@editLogger('Additional page merged into Letter', 'PythonScript_mergeLetterPagesResolve')
	def mergeLetterPagesResolve(self, old, new):
		#print('merge resolve called')
		letter = old
		letter['Pages'][new['Page']] = self._mergeLetterBuildPageDict(new)
		return letter

	@editLogger('New Letter created', 'PythonScript_mergeLetterPagesTransform')
	def mergeLetterPagesTransform(self, field):
		#print('merge transform called')
		letter = field
		letter['Pages'] = {field['Page']: self._mergeLetterBuildPageDict(field)}
		return self._mergeLetterDeleteFields(letter)

	def _mergeLetterBuildPageDict(self,field):
		return {"Translation": field['Translation'], 
				"Original_Filename": field['Original_Filename'], 
				"Archive_Filename": field['Archive_Filename']}

	def _mergeLetterDeleteFields(self,letter):
		for key in ["Translation", "Page", "Original_Filename", "Archive_Filename"]:
			del letter[key]
		return letter







if __name__ == "__main__":

	message = """
	This script has two functions:
	RPD = Extracting Excel data to a Python object while removing page duplicates
	MLP = Merging pages into a dict object beloning to a single Letter object

	This script may be called directly with command-line arguments,
	or instances of RemovePageDuplicates and MergeLetterPages may
	be used in a script.

	View --help for more info on running from
	the command line.
	"""

	parser = argparse.ArgumentParser(description=message)
	parser.add_argument('--inputFilePath', '-i', help="Specify the path of an input file.")
	parser.add_argument('--outputFilePath', '-o', help="Specify the path to output file")
	parser.add_argument('--process', '-p', help="Specify a process (RPD or MLP).")


	inputFilePath = parser.parse_args().inputFilePath
	outputFilePath = parser.parse_args().outputFilePath
	process = parser.parse_args().process
	
	if not inputFilePath or not outputFilePath:
		raise ValueError('An input file [-i] and output file path [-o] must be specified.')


	if not process or (process != 'RPD' and process != 'MLP'):
		raise ValueError('A process [-p] (either RPD or MLP) must be specified')

	if process == 'RPD':
		r = RemovePageDuplicates(inputFilePath, outputFilePath)
		r.process()
		print("Data has been extracted to the shelf file '%s'" % outputFilePath)
	elif process == 'MLP':
		m = MergeLetterPages(inputFilePath, outputFilePath)
		m.process()
		print("Data has been extracted to the shelf file '%s'" % outputFilePath)

