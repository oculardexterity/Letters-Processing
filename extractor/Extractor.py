from datetime import datetime
import os
from openpyxl import load_workbook
import shelve
from Stream import Stream



class Processor:
	def __init__(self): # f, outputFilePath):
		self.stream = Stream(self.inputFilePath, self.dict_key)
		if os.path.isfile(self.outputFilePath):
			os.remove(self.outputFilePath)
		self.new_shelf_file = self.outputFilePath


	def process(self):
		with shelve.open(self.new_shelf_file) as new_shelf:
			for index, fields in self.stream.stream():

				if index in new_shelf:
					#print('index in new shelf')
					new_shelf[index] = self.resolve(new_shelf[index], fields)
				else:
					#print('index not in new shelf')
					new_shelf[index] = self.transform(fields)
		
		

	

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
	#r = RemovePageDuplicates('spreadsheets/1916letters_all_translations07072015.xlsx','output/testout.shelve')
	#r.process()

	m = MergeLetterPages('output/testout.shelve', 'lettermerge.shelve')
	m.process()
