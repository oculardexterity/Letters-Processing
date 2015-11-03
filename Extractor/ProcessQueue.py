from Extractor import Extractor as Extractor

class ProcessQueue:
	def __init__(self, inputFilePath, shelve_directory, output_directory):
		self.output_directory = output_directory
		self.shelve_directory = shelve_directory
		self.inputFilePath = inputFilePath


		self.output_file_name = ""

	def __call__(self):
		self.run_Extractor_RPD()
		self.run_Extractor_MLP()

	

	def run_Extractor_RPD(self):
		self.output_file_name = 'ExtractorRPD'
		r = Extractor.RemovePageDuplicates(self.inputFilePath, self.output_file_path())
		r.process()

	def run_Extractor_MLP(self):
		self.update_file_names('ExtractorMLP')
		m = MergeLetterPages(self.input_file_path(), self.output_file_path())
		m.process()



	def input_file_path(self):
		return self.shelve_directory + self.input_file_name + '.shelve'

	def output_file_path(self):
		return self.shelve_directory + self.output_file_name + '.shelve'

	def update_file_names(self, addition):
		self.input_file_name = self.output_file_name
		self.output_file_name = self.input_file_name + "_" + addition



if __