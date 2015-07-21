import pytest

import os

from Extractor.Extractor import Extractor

class TestExtractor:

	def setup(self):
		self.test_sheets_dir = "test/test_extractor/test_sheets"
		self.extractors = {name: Extractor(f_name) 
							for name, f_name in self.get_test_sheets().items()}


	def get_test_sheets(self):
		files = {}
		for f in os.listdir(self.test_sheets_dir):
			if f.endswith('.xlsx') and not f.startswith('~'):
				files[f.strip('.xslx')] = f
		return files




	def test_sanityTest(self):
		assert self.extractors["test_simple"].thing() == 'test'


	def test_getHeaders(self):
		assert self.extractors["test_simple"].getHeaders == ['A_HEADER', 'B_HEADER', u'ID']