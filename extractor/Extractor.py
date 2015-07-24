import os
import shelve
from openpyxl import load_workbook

from datetime import datetime




class Merge(Stream):
	def __init__(self, f, merge_type, outputFilePath):
		super().__init__(f)
		self.merge_type = merge_type
		if merge_type == 'remove_page_duplicates':
			self.resolve = self.pageDuplicatesResolve
			self.transform = self.pageDuplicatesTransform
			self.id_column = 'Page'
		elif merge_type == 'merge_letter_pages':
			self.resolve = self.mergeLetterPagesResolve
			self.transform = self.mergeLetterPagesTransform
			self.id_column = 'Letter'
		
		if os.path.isfile(outputFilePath):
			os.remove(outputFilePath)

		self.new_shelf_file = outputFilePath


	def merge(self):
		with shelve.open(self.new_shelf_file) as new_shelf:
			for index, fields in self.stream():

				# Set up ID clash
				if self.merge_type == 'merge_letter_pages':
					index = str(fields['Letter'])

				if index in new_shelf:
					#print('index in new shelf')
					new_shelf[index] = self.resolve(new_shelf[index], fields)
				else:
					#print('index not in new shelf')
					new_shelf[index] = self.transform(fields)
		
		

	def pageDuplicatesResolve(self, old, new):

		#print(old['Translation_Timestamp'], new['Translation_Timestamp'])

		if old['Translation_Timestamp'] >= new['Translation_Timestamp']:
			return old
		elif new['Translation_Timestamp'] >= old['Translation_Timestamp']:
			return new

	def pageDuplicatesTransform(self, field):
		return field

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

	startTime = datetime.now()
	merge = Merge('spreadsheets/1916letters_all_translations07072015.xlsx', 'remove_page_duplicates', 'output/datemerge.shelve')
	print(datetime.now() - startTime)
	merge.merge()
	print(datetime.now() - startTime)
	merge = Merge('output/datemerge.shelve', 'merge_letter_pages', 'output/lettermerge.shelve')
	merge.merge()
	print(datetime.now() - startTime)


