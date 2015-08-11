import dateparser
import datetime
import os
import shelve
import sys

from Processor import Filter
from Stream import Stream		

### Filterlist should inherit from list type --- self=values...
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
	def __init__(self,filePath,column, date=None):
		if os.path.isfile(filePath) and filePath.endswith('xlsx'):
			self.filePath = filePath
			self.column = column
			self.date = dateparser.parse(date) or datetime.datetime.now()
			print(self.date)
			self.values = list(self.getValuesFromFile())
			super().__init__()
		else:
 			raise TypeError("'%s' is not an Excel file" % filePath)

	def getValuesFromFile(self):
 		stream = Stream(self.filePath, self.column, sheet="ID NUMBERS")
 		
 		for k, v in stream.stream():
 			print(v['DATE'] < self.date)
 			if k != 'None' and v['DATE'] < self.date:
	 			yield str(k) + '.0'



if __name__ == "__main__":
	
	incList = ListFromExcel('spreadsheets/Completed Letters to be proofed.xlsx', 'ID', date='7 July')
	

	exList = ListFromDirectory('xmlfiles')


	f = Filter('output/letterMerge.shelve', 'output/filtered.shelve')
	
	f.inclusionListAdd(incList)
	f.exclusionListAdd(exList)

	f.filter()