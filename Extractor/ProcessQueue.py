import Extractor as Extractor
from Processor import Filter as Filter
import Filter as FilterLists
import Cleaners
import PageTypeLoggers
import wrapOpener
import FixAddrLinesDates
import BuildCollectionIdnos

import os

class ProcessQueue:
	def __init__(self, config):
		self.output_directory = config["output_directory"]
		self.shelve_directory = config["shelve_directory"]
		self.inputFilePath = config["inputFilePath"]

		self.filter_configs = config["filter_configs"]
		self.editLogger_configs = config["editLogger_configs"]

		self.output_file_name = ""

	def __call__(self):
		self.run_Extractor_RPD()
		self.run_Extractor_MLP()
		self.run_Filter()
		self.run_EditLogger()
		self.run_Cleaners()
		self.run_PageTypeLoggers()
		self.run_WrapOpener()
		self.run_FixAddrLines()
		self.run_BuildCollectionIdnos()
		self.run_StreamOutput()

	

	def run_Extractor_RPD(self):
		self.output_file_name = 'ExtractorRPD'
		r = Extractor.RemovePageDuplicates(self.inputFilePath, self.output_file_path())
		#print(self.output_file_name)
		r.process()

	def run_Extractor_MLP(self):
		self.update_file_names('ExtractorMLP')
		m = Extractor.MergeLetterPages(self.input_file_path(), self.output_file_path())
		#print(self.input_file_name, self.output_file_name)
		m.process()

	def run_Filter(self):
		self.update_file_names('FilterComplete')
		incList = FilterLists.ListFromExcel(self.filter_configs["inclusionFilePath"],
									   self.filter_configs["inclusionColumnHeader"],
									   date=self.filter_configs["cutoffDate"])
		f = Filter(self.input_file_path(), self.output_file_path())
		f.inclusionListAdd(incList)
		f.filter()

	def run_EditLogger(self):
		''' Script written in **horrible** way -- only option to call from command line '''
		self.update_file_names('OmekaEditsLogged')
		command = "python Extractor/EditLogger.py -i " + self.input_file_path() \
					+ ' -o ' + self.output_file_path() + ' -f ' \
					+ "'" + self.editLogger_configs["editFilePath"] + "'"
		os.system(command)

	def run_Cleaners(self):
		self.update_file_names('TagsCleaned')
		fix_tags = Cleaners.FixTags(self.input_file_path(), self.output_file_path())
		fix_tags.process()


	def run_PageTypeLoggers(self):
		self.update_file_names('PageTypesLogged')
		logger = PageTypeLoggers.PageTypeLogger(self.input_file_path(), self.output_file_path())
		logger.process()

	def run_WrapOpener(self):
		self.update_file_names('WrapOpener')
		w = wrapOpener.WrapOpenerAndCloser(self.input_file_path(), self.output_file_path())
		w.process()

	def run_FixAddrLines(self):
		self.update_file_names('FixAddrDateLines')
		f = FixAddrLinesDates.FixAddrLineDate(self.input_file_path(), self.output_file_path())
		f.process()

	def run_BuildCollectionIdnos(self):
		self.update_file_names('BuildCollectionIdnos')
		b = BuildCollectionIdnos.BuildCollectionIdnos(self.input_file_path(), self.output_file_path())
		b.process()

	def run_StreamOutput(self):
		''' Quick sanity check by outputting the entire finished doc '''
		command = "python Extractor/Stream.py -f " + self.output_file_path() \
					+ ' -k Letter'
		os.system(command)

	'''
	Util functions for managing file names and paths
	'''
	def input_file_path(self):
		return self.shelve_directory + self.input_file_name + '.shelve'

	def output_file_path(self):
		return self.shelve_directory + self.output_file_name + '.shelve'

	def update_file_names(self, addition):
		self.input_file_name = self.output_file_name
		self.output_file_name = self.input_file_name + "_" + addition



if __name__ == '__main__':
	config = {
		"inputFilePath": 'spreadsheets/newDump.xlsx',
		"shelve_directory": 'testfiles/shelves/',
		"output_directory": 'testfiles/output/',
		"filter_configs" : {
			"inclusionFilePath": "spreadsheets/Completed Letters to be proofed_new.xlsx",
			"inclusionColumnHeader": "ID",
			"cutoffDate": "2 October 2015"
		},
		"editLogger_configs": {
			"editFilePath": "spreadsheets/Completed Letters to be proofed_new.xlsx"
		}
	}


	p = ProcessQueue(config)
	p()