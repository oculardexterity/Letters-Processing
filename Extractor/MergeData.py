from Processor import Processor
from Stream import Stream





class MergeData(Processor):
	"""
	Classes inheriting from MergeData must implement a get_data_to_merge() function.
	"""

	def __init__(self, inputFilePath, outputFilePath, dict_key):
		#self.resolve = self.merge  # This shouldn't need to be called....
		self.transform = self.merge
		self.dict_key = dict_key
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath

		'''
		### Implement in the subclass...
		self.dataField = dataField
		self.dataToMerge = dataToMerge # This should be a list of objects...
		'''
		super().__init__()

	def merge(self, row):
		if str(row[self.dict_key]) + '.0' in self.data:
			if self.dataField in row:
				if type(self.dataField) is list:
					row[self.dataField].append(self.dataToMerge)
					return row
				else:
					raise TypeError('Cannot append data to a non-list object.')
			else:
				row[self.dataField] = self.get_merge_data(row, self.row_match_field)
				return row
		else:
			return row



   
class EditLogger(MergeData):
	def __init__(self, inputFilePath, outputFilePath, editDetails):
		self.row_match_field = 'Letter'
		self.editDetails = editDetails

		## This should be passed in --- maybe as a DATA_TO_MERGE class, like the FilterList classes?
		## Would only need half as many classes then!
		## Why does the filter class need to be a class?
	    self.data = Stream(self.editDetails['dataFile'], self.editDetails['matchColumn'],\
											 sheet=self.editDetails['dataSheet']).as_dict()
		self.dataField = "Edits"
		super().__init__(inputFilePath, outputFilePath, 'Letter')
		
    
	def get_merge_data(self, row, match_field):
		identifier = str(row[match_field]) + '.0'

		return [{"EditType": self.editDetails['type'], "Editor": self.data[identifier][self.editDetails['editor']]}]



class EditsDict(dict):
	def __init__(self, values):
		self = values

class EditsFromExcelSpreadsheet(EditsDict):
	def __init__(self):
		#Get values, pass to Super()

# No, edit logger being the thing that adjusts edit type... 
# So actually a thing that writes fields into the Editing thing?

# So the EditLogger should be a thing that operates on the letter[edits] thing and uses the 'merge' function as above?

# THIs SORT of balls is way too many args!
editDetails = {'dataFile': 'spreadsheets/Completed Letters to be proofed.xlsx', 
			'dataSheet': 'DRI LETTERS', 'matchColumn': 'NUMBER', 'type': 'OmekaProof', 'editor': 'PROOFED BY'}

editLogger = EditLogger('output/filtered.shelve', 'output/editInfoAdded.shelve', editDetails)
editLogger.process()

'''
newEditDetails = {'dataFile': 'spreadsheets/Completed Letters to be proofed.xlsx', 
			'dataSheet': 'OTHER', 'matchColumn': 'NUMBER', 'type': 'OmekaProof', 'editor': 'PROOFED BY'}
newEditLogger = EditLogger('output/editInfoAdded.shelve', 'output/editInfoAdded2.shelve', newEditDetails)
newEditLogger.process()
'''