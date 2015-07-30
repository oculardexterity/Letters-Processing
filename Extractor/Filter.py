from Extractor import Stream
import os
#from openpyxl import load_workbook
import sys

class Filter:
	def __init__(self):
		self.inclusionList = []
		self.exclusionList = []
		self.stream = Stream(inputFilePath, dictKey)

	def inclusionListAdd(filterList):
		self.inclusionList += filterList

	def exclusionListAdd(filterList):
		self.inclusionList += filterList

	def process(self):
		pass


class FilterList:
	def __init__(self):
		pass

	def __call__(self):
		return self.values

	def __iter__(self):
		return iter(self.values)

	def __len__(self):
		return len(self.values)


class ListFromExcel(FilterList):
	def __init__(self,filePath,column):
		if os.path.isfile(filePath) and filePath.endswith('xlsx'):
			self.filePath = filePath
			self.column = column
			self.values = self.getValuesFromFile()
			super().__init__()
		else:
 			raise TypeError("'%s' is not an Excel file" % filePath)

	def getValuesFromFile(self):
 		stream = Stream(self.filePath, self.column, sheet="ID NUMBERS")
 		return [k for k, v in stream.stream()]
 		"""
 		# Replaced with Stream() modules... haha!
 		wb = load_workbook(filename=self.filePath, read_only=True)
 		sheet = wb.active # Or some sheet title
 		return [str(row[0].value) for row in sheet.iter_rows()][1:] #List index to ignore header row
 		## Maybe change this to use Stream class -- which will allow selection by column???
 		"""

if __name__ == "__main__":
	l = ListFromExcel('spreadsheets/Completed Letters to be proofed.xlsx', 'ID#')
	print(l())