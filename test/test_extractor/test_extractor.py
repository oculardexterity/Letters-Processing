import pytest

import os

from Extractor.Extractor import Stream

class TestExtractor:

	def setup(self):
		self.test_sheets_dir = "test/test_extractor/test_sheets/"
		self.extractors = {name: Stream(f_name) 
							for name, f_name in self.get_test_sheets().items()}


	def get_test_sheets(self):
		files = {}
		for f in os.listdir(self.test_sheets_dir):
			if f.endswith('.xlsx') and not f.startswith('~'):
				files[f.strip('.xslx')] = self.test_sheets_dir + f
		return files


	def test_sanityTest(self):
		assert self.extractors["test_simple"].thing() == 'test'


	def test_getHeaders(self):
		assert self.extractors["test_simple"].getHeaders() == ['A_HEADER', 'B_HEADER', 'ID']

	def test_getRowData(self):
		assert list(self.extractors["test_simple"].getRowData()) == [['a_value1', 'b_value1', 1],
					    									['a_value2', 'b_value2', 2]]

	def test_buildRowTuple(self):
		self.extractors["test_simple"].id_column = "ID"
		row = ['a_value1', 'b_value1', 1]
		assert self.extractors["test_simple"].buildRowTuple(row) ==  ('1', { 'A_HEADER' : 'a_value1', 'B_HEADER': 'b_value1', 'ID': 1 } )
	
	def test_outputRows(self):
		self.extractors["test_simple"].id_column = "ID"
		print(list(self.extractors["test_simple"].outputRows()))
		assert list(self.extractors["test_simple"].outputRows()) == [('1.0', { 'A_HEADER' : 'a_value1', 'B_HEADER': 'b_value1', 'ID': 1 } ),
																		('2.0', { 'A_HEADER' : 'a_value2', 'B_HEADER': 'b_value2', 'ID': 2 } )]
	