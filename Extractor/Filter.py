from Extractor import Stream # is this right? From Stream import Stream surely???
import os
import shelve
#from openpyxl import load_workbook
import sys

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
		
		with shelve.open(self.new_shelve_file) as new_shelf:
			for index, fields in self.stream.stream():
				#print(str(index))
				if str(index)+'.0'  in self.inclusionList and str(index)+'.0' not in self.exclusionList:
					print(index)
					new_shelf[index] = fields
		

# Extract these to different file and import...
class FilterList:
	def __init__(self):
		pass

	def __call__(self):
		return self.values

	def __iter__(self):
		return iter(self.values)

	def __len__(self):
		return len(self.values)


class ListFromDirectory(FilterList):
	def __init__(self,path):
		if os.path.isdir(path):
			self.path = path
			self.values = self.getValuesFromDirFiles()
			super().__init__()
		else:
			raise TypeError("'%s' is not a directory" % path)

	def getValuesFromDirFiles(self):
		return [str(f[:-4]) for f in os.listdir(self.path) if f.endswith('.xml')]


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
	
	incList = ListFromExcel('spreadsheets/Completed Letters to be proofed.xlsx', 'ID#')
	

	exList = ListFromDirectory('xmlfiles')


	f = Filter('output/lettermerge.shelve', 'output/filtered.shelve')
	
	f.inclusionListAdd(incList)
	f.exclusionListAdd(exList)

	f.filter()