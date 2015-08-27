import datetime


from Stream import Stream


class EditLogger:
	def __init__(self, editDict=None, logEdits=True):
		if editDict:
			self.editDict = editDict
		else:
			self.editDict = None

		if logEdits:
			self.edit_function = self._log_edit
		else:
			self.edit_function = self._not_log_edit

	def __call__(self, editType=None, editActor=None, editExtraInfo=None):
		return self.edit_function(editType, editActor, editExtraInfo)


	def _build_edit(self, row, editType, editActor, editExtraInfo):
		"""
		if self.editDict: builds an edit from an EditDict object passed on intialisation of EditLogger
		else: builds an edit from variables passed to self.edit_function (via __call__() method on object)
		"""
		if self.editDict:
			identifier = str(row['Letter'])
			#print(identifier)
			if identifier in self.editDict.data: 
				edit = {'editType': self.editDict.editType, 
						'editor': self.editDict.data[identifier][self.editDict.editorColumn],
						'datetime': str(self.editDict.data[identifier][self.editDict.editDateColumn])}
				return edit
			
		else:
			edit = {"editType": editType, "editor": editActor, 'datetime': str(datetime.datetime.now())}
			if editExtraInfo:
				edit = edit.update(editExtraInfo)
			return edit


	def _log_edit(self, editType=None, editActor=None, editExtraInfo=None):
		def edit_logger(func):
			def func_wrapper(*args, **kwargs):
				row = func(*args, **kwargs)
				edit = self._build_edit(row, editType, editActor, editExtraInfo)
				if edit:
					if "Edits" in row:
						row["Edits"].append(edit)
					else:
						row["Edits"] = [edit]
				return row
			return func_wrapper
		return edit_logger

	# Makes the editlogger decorator not do anything at all!
	def _not_log_edit(self, editType=None, editActor=None, editExtraInfo=None):
		def edit_logger(func):
			def func_wrapper(*args, **kwargs):
				row = func(*args, **kwargs)
				return row
			return func_wrapper
		return edit_logger

#@e.log_edit("Automated thing", "Python script")


class EditsDict:
	def __init__(self, editType, editorColumn, editDateColumn, data):
		self.editType = editType
		self.data = data
		self.editorColumn = editorColumn
		self.editDateColumn = editDateColumn



class EditsFromExcelSpreadsheet(EditsDict):
	def __init__(self, dataFile, dataSheet, matchColumn, editorColumn, editDateColumn, editType):
		# Gets data
		data = Stream(dataFile, matchColumn, sheet=dataSheet).as_dict()
		super().__init__(editType, editorColumn, editDateColumn, data)










if __name__ == '__main__':
	from Processor import Processor as Processor
	edits = EditsFromExcelSpreadsheet('spreadsheets/Completed Letters to be proofed.xlsx', 
				'ID NUMBERS', 'ID', 'PROOFED BY', 'DATE', 'OmekaProof')

	editLogger = EditLogger(editDict=edits)


	class LogEditProcess(Processor):
		def __init__(self, inputFilePath, outputFilePath):
			self.resolve = self._logEditProcess
			self.transform = self._logEditProcess
			self.dict_key = 'Letter'
			self.inputFilePath = inputFilePath
			self.outputFilePath = outputFilePath
			super().__init__()

		@editLogger()
		def _logEditProcess(self, field):
			return field

	lep = LogEditProcess('output/filtered.shelve', 'output/omekaProofEditsLogged.shelve')
	lep.process()



