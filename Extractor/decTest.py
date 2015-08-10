def log_edit(edit):
	def edit_logger(func):
		def func_wrapper(*args, **kwargs):
			row = func(*args, **kwargs)
			row["edit"] = edit
			return row
		return func_wrapper
	return edit_logger

@log_edit("new edit")
def do_a_thing_to_row(row):
	row["thing"] = 'newthing'
	return row


row = {'old': 'stuff'}

print(row)

print(do_a_thing_to_row(row))