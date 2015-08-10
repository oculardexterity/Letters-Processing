import datetime


class EditLogger:
	def __init__(self, thing):
		self.thing = thing

	def log_edit(self, editType, editActor):
		def edit_logger(func):
			def func_wrapper(*args, **kwargs):
				row = func(*args, **kwargs)
				edit = {"editType": self.thing, "editor": editActor, "datetime": str(datetime.datetime.now())}
				if "Edits" in row:
					row["Edits"].append(edit)
				else:
					row["Edits"] = [edit]
				return row
			return func_wrapper
		return edit_logger


#@e.log_edit("Automated thing", "Python script")



class myPseudoProcessor:
	row  = {'old': 'oldstuffstuff', 'Edits': [{"one": "edit1"}]}

	def __init__(self):
		pass

	@e.log_edit('automatedEdit', 'PythonScript')
	def do_a_thing_to_row(self):
		self.row["thing"] = 'newthing'
		return self.row


#mp = myPseudoProcessor()
#print(mp.do_a_thing_to_row())