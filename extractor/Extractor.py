import os
import shelve
import xlrd

class Stream:
	def __init__(self, f):
		# Dependent on file type:
		if f.endswith('xlsx'):
			self.sheet = xlrd.open_workbook(f).sheet_by_index(0)
			self.headers = self.getHeaders()
			self.stream = self.outputRowsFromFile
		elif f.endswith('shelve'):
			self.shelf = shelve.open(f)
			self.stream = outputRowsFromShelf
		else:
			raise ValueError("File must be an Excel spreadsheet or a Shelve file")


	def thing(self): # A sanity test
		return 'test'

	def getHeaders(self):
		headers = [self.sheet.cell(0, col_index).value for col_index in range(self.sheet.ncols)]
		return headers

	def getRowData(self):
		yield from [[self.sheet.cell(i, col_index).value 
						for col_index in range(self.sheet.ncols)]
						for i in range(1,self.sheet.nrows)]

	def buildRowTuple(self, row):
		id_index = self.headers.index(self.id_column)
		return (str(row[id_index]), {self.headers[i]: cell for i, cell in enumerate(row)})
	
	def outputRowsFromFile(self):
		yield from [self.buildRowTuple(row) for row in self.getRowData()]
	
	
	def outputRowsFromShelf(self):
		yield from [(k,v) for item in self.shelf]


class Merge(Stream):
	def __init__(self, f, merge_type, outputFilePath):
		super().__init__(f)
		if merge_type == 'remove_page_duplicates':
			self.resolve = self.pageDuplicatesResolve
			self.transform = self.pageDuplicatesTransform
			self.id_column = 'ID'
		elif merge_type == 'merge_letter_pages':
			self.resolve = self.mergeLetterPagesResolve
			self.transform = self.mergeLetterPagesTransform
			self.id_column = 'Letter'
		
		if os.path.isfile(outputFilePath):
			os.remove(outputFilePath)

		self.shelf_file = outputFilePath


	def merge(self):
		with shelve.open(self.shelf_file) as new_shelf:
			for index, fields in self.stream():

				print(type(self.resolve))
				# Set up a clash of ids...

				if index in new_shelf:
					print('index in new shelf')
					new_shelf[index] = self.resolve(new_shelf[index], fields)
				else:
					print('index not in new shelf')
					new_shelf[index] = self.transform(fields)
		
			for k, v in new_shelf.items():
				print(k, v)

	def pageDuplicatesResolve(self, old, new):
		if old['DT'] > new['DT']:
			return old
		elif new['DT'] > old['DT']:
			return new

	def pageDuplicatesTransform(self, field):
		return field

	def mergeLetterPagesResolve(self, old, new):
		letter_key = a

	def mergeLetterPagesTransform(self, field):
		return field

if __name__ == "__main__":
	merge = Merge('spreadsheets/test_datetime.xlsx', 'remove_page_duplicates', 'output/datemerge.shelve')
	
	merge.merge()

	

