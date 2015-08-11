import datetime


class EditLogger:
	def __init__(self, editDict=None, logEdits=True):
		if logEdits:
			self.edit_function = self._log_edit
		else:
			self.edit_function = self._not_log_edit

	def __call__(self, editType, editActor, editExtraInfo=None):
		return self.edit_function(editType, editActor, editExtraInfo)


	'''
	## Something here... GET
	def build_your_edit(self, row, match_field):
		identifier = str(row[match_field]) + '.0'
		return [{"EditType": self.editsDict.editType, 
					"Editor": self.editsDict.values[identifier][self.editsDict.editorColumn]}]
	'''

				# THESE THINGS PASSED IN --- also need to allow an EDITDICT
	def _log_edit(self, editType, editActor, editExtraInfo):
		def edit_logger(func):
			def func_wrapper(*args, **kwargs):
				row = func(*args, **kwargs)
				edit = {"editType": editType, "editor": editActor, 'datetime': str(datetime.datetime.now())}
				if editExtraInfo:
					edit = edit.update(editExtraInfo)
				if "Edits" in row:
					row["Edits"].append(edit)
				else:
					row["Edits"] = [edit]
				return row
			return func_wrapper
		return edit_logger

	# Makes the editlogger decorator not do anything at all!
	def _not_log_edit(self, editType, editActor, editExtraInfo):
		def edit_logger(func):
			def func_wrapper(*args, **kwargs):
				row = func(*args, **kwargs)
				return row
			return func_wrapper
		return edit_logger

#@e.log_edit("Automated thing", "Python script")


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
