import argparse
from datetime import datetime
import os
from openpyxl import load_workbook
import shelve
from Stream import Stream
import sys



class Processor:
	def __init__(self): # f, outputFilePath):
		self.stream = Stream(self.inputFilePath, self.dict_key)
		self.new_shelf_file = self.outputFilePath


	def process(self):
		with ShelveManager(self.new_shelf_file) as new_shelf:
			for index, fields in self.stream.stream():

				if index in new_shelf:
					#print('index in new shelf')
					new_shelf[index] = self.resolve(new_shelf[index], fields)
				else:
					#print('index not in new shelf')
					new_shelf[index] = self.transform(fields)
		
		
class ShelveManager:
	def __init__(self, shelfFile, auto=False):
		self.shelfFile = shelfFile
		

	def __enter__(self):
		self.manageFile()
		
		# Set and return shelf object
		self.shelf = shelve.open(self.shelfFile)
		return self.shelf

	def __exit__(self, type, value, traceback):
		self.shelf.close()
	
	def manageFile(self):
		if os.path.isfile(self.shelfFile):
			if input("\nDo you wish to overwrite data file '%s'? (y/n): " % self.shelfFile) == 'y':
				os.remove(self.shelfFile)
				print('\nFile overwriting')
			else:
				sys.exit('\nProcess stopped to prevent data file overwrite')



class RemovePageDuplicates(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self.pageDuplicatesResolve
		self.transform = self.pageDuplicatesTransform
		self.dict_key = 'Page'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		super().__init__()

	def pageDuplicatesResolve(self, old, new):
		if old['Translation_Timestamp'] >= new['Translation_Timestamp']:
			return old
		elif new['Translation_Timestamp'] >= old['Translation_Timestamp']:
			return new

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


	def mergeLetterPagesResolve(self, old, new):
		#print('merge resolve called')
		letter = old
		letter['Pages'][new['Page']] = self.mergeLetterBuildPageDict(new)
		return letter

	def mergeLetterPagesTransform(self, field):
		#print('merge transform called')
		letter = field
		letter['Pages'] = {field['Page']: self.mergeLetterBuildPageDict(field)}
		return self.mergeLetterDeleteFields(letter)

	def mergeLetterBuildPageDict(self,field):
		return {"Translation": field['Translation'], 
				"Original_Filename": field['Original_Filename'], 
				"Archive_Filename": field['Archive_Filename']}

	def mergeLetterDeleteFields(self,letter):
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

