import xlrd

class Extractor:
	def __init__(self, f):
		self.sheet = xlrd.open_workbook(f).sheet_by_index(0) 

	def thing(self): # A sanity test
		return 'test'

	def getHeaders(self):
		return 'nonsense'