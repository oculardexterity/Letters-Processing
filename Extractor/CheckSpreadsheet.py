import Stream

class Checker:
	def __init__(self, filePath):
		self.filePath = filePath
		self.req_fields = """revID
							Title
							Creator
							Letter
							Description
							Source
							DocCollection
							Recipient
							Recipient_location
							Sender_location
							DATE_created
							Authors_gender
							Year_of_death_of_author
							Collection
							Archive_Filename
							Translation_Timestamp
							Topic""".replace('\t', '').split('\n');


	def check(self):
		#print(self.req_fields)
		s = Stream.Stream(self.filePath, 'Page', 'Translation').stream()
		_, kvs = s.__next__()
		keys = [keys for keys, _ in kvs.items()]
		#print(keys)
		missing = [f for f in self.req_fields if f not in keys]
		
		if missing:
			raise ValueError('\n\nThe following fields are missing from the spreadsheet: \n\n'\
			 + '\n'.join(missing) + '\n\nThey may be spelled incorrectly.')
		
if __name__ == '__main__':
	c = Checker('spreadsheets/16122015_revisors.xlsx')
	c.check()
