import os
import shelve
from Stream import Stream


class Filter:
	def __init__(self, inputFilePath, outputFilePath):
		self.inclusionList = []
		self.exclusionList = []
		self.stream = Stream(inputFilePath, 'Letter')
		self.new_shelve_file = outputFilePath

	def inclusionListAdd(self, filterList):
		self.inclusionList += filterList()

	def exclusionListAdd(self, filterList):
		self.exclusionList += filterList()

	def filter(self):
		
		with ShelveManager(self.new_shelve_file) as new_shelf:
			for index, fields in self.stream.stream():
				#print(str(index))
				if str(index)+'.0'  in self.inclusionList and str(index)+'.0' not in self.exclusionList:
					print(index)
					new_shelf[index] = fields

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
					print(index, new_shelf[index])
		
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