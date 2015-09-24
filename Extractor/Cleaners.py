import re

from Processor import Processor as Processor
from EditLogger import EditLogger


editLogger = EditLogger()

class FixAmpersands(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self._fix_ampersands
		self.transform = self._fix_ampersands
		self.dict_key = 'Letter'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		super().__init__()

	@editLogger('Replaced nonvalid ampersands with &amp;', 'PythonScript_CleanersFixAmpersands')
	def _fix_ampersands(self, row):
		new_row = row
		reg = r'&(?!\S+[^;])'
		mod = '&amp;'
		for key, page in row["Pages"].items():
			modified_page =  re.sub(reg, mod, page["Translation"])
			new_row["Pages"][key]["Translation"] = modified_page
		return new_row

if __name__ == '__main__':
	fix_amps = FixAmpersands('output/omekaProofEditsLogged.shelve','output/fixAmperands.shelve')
	fix_amps.process()
