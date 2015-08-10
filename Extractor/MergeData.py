from Processor import Processor
from Stream import Stream


'''
Am I really going to rewrite all of this in Decorator fashion??
'''


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
		# self.writeGenericToAll allows some generic thing to be written to all rows
		if str(row[self.dict_key]) + '.0' in self.data or self.writeGenericToAll:
			if self.dataField in row:
				if type(self.dataField) is list:
					row[self.dataField].append(self.get_merge_data(row, self.row_match_field))
					return row
				else:
					raise TypeError('Cannot append data to a non-list object.')
			else:
				row[self.dataField] = self.get_merge_data(row, self.row_match_field)
				print(row)
				return row
		else:
			return row
		

class EditLogger(MergeData):
	def __init__(self, inputFilePath, outputFilePath, editsDict, generic=False):
		self.row_match_field = 'Letter'
		self.data = editsDict.values
		self.editsDict = editsDict
		self.dataField = 'Edits'
		self.writeGenericToAll = generic

		if generic:
			self.get_merge_data = self.generic_data
		else:
			self.get_merge_data = self.merge_data


		super().__init__(inputFilePath, outputFilePath, 'Letter')
		
    
    #Implement choice here... match from dict... or Generic option??
	def merge_data(self, row, match_field):
		identifier = str(row[match_field]) + '.0'
		return [{"EditType": self.editsDict.editType, 
					"Editor": self.editsDict.values[identifier][self.editsDict.editorColumn]}]


	def generic_data(self, row, match_field):
		return ["Edit type": self.editsDict.editType]
		### CHECK THIS WORKS!!!


class EditsDict:
	def __init__(self, editType, editorColumn, values):
		self.editType = editType
		self.values = values
		self.editorColumn = editorColumn



class EditsFromExcelSpreadsheet(EditsDict):
	def __init__(self, dataFile, dataSheet, matchColumn, editorColumn, editType):
		# Gets data
		data = Stream(dataFile, matchColumn, sheet=dataSheet).as_dict()
		super().__init__(editType, editorColumn, data)



# No, edit logger being the thing that adjusts edit type... 
# So actually a thing that writes fields into the Editing thing?

# So the EditLogger should be a thing that operates on the letter[edits] thing and uses the 'merge' function as above?

# THIs SORT of balls is way too many args!
editDetails = EditsFromExcelSpreadsheet('spreadsheets/Completed Letters to be proofed.xlsx', 
			'DRI LETTERS', 'NUMBER', 'PROOFED BY', 'OmekaProof')
#print(editDetails.values)

editLogger = EditLogger('output/filtered.shelve', 'output/editInfoAdded.shelve', editDetails)
editLogger.process()

'''
newEditDetails = {'dataFile': 'spreadsheets/Completed Letters to be proofed.xlsx', 
			'dataSheet': 'OTHER', 'matchColumn': 'NUMBER', 'type': 'OmekaProof', 'editor': 'PROOFED BY'}
newEditLogger = EditLogger('output/editInfoAdded.shelve', 'output/editInfoAdded2.shelve', newEditDetails)
newEditLogger.process()
'''