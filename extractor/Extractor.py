import xlrd

class Extractor:
	def __init__(self, f):
		self.sheet = xlrd.open_workbook(f).sheet_by_index(0)
		self.headers = self.getHeaders()
		self.data = {}

	def thing(self): # A sanity test
		return 'test'

	def getHeaders(self):
		headers = [self.sheet.cell(0, col_index).value for col_index in range(self.sheet.ncols)]
		return headers

	def getRowData(self):
		yield from [[self.sheet.cell(i, col_index).value 
						for col_index in range(self.sheet.ncols)]
						for i in range(1,self.sheet.nrows)]

	def buildRowDict(self, row):
		id_index = self.headers.index(self.id_column)
		return {str(row[id_index]) : {self.headers[i]: cell for i, cell in enumerate(row)}}
		

