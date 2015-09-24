import re

from Processor import Processor as Processor
from EditLogger import EditLogger


editLogger = EditLogger()

class FixAmpersands(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self._clean_tags
		self.transform = self._clean_tags
		self.dict_key = 'Letter'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		super().__init__()

	@editLogger('Clean tags', 'PythonScript_CleanersFixAmpersands')
	def _clean_tags(self, row):
		new_row = row
		reg = r'&(?!\S+[^;])'
		mod = '&amp;'

		for key, page in row["Pages"].items():
			if page["Translation"] is not None:
				new_row["Pages"][key]["Translation"] = self._tag_cleaner(page["Translation"])
		return new_row

	def _tag_cleaner(self, text):
		text = re.sub(r'&(?!\S+[^;][&])', '&amp;', text)
		text = re.sub(r'<<', '<', text)
		text = re.sub(r'>>', '>', text)
		text = re.sub(r'\<\s+\>', "", text)
		text = re.sub(r'\<\s+', "<", text)
		text = re.sub(r'\s+\>', ">", text)

		for empttag in ["lb", "pb", "gap"]:
			for sub in [r'\<\/' + empttag + r'\>', 
						r'\<\/' + empttag + r'(?!\>)',
						r'(?<!\<)\/' + empttag + r'\>?',
						r'\<' + empttag + r'\/(?!\>)',
						r'\<' + empttag + r'\>']:
				text = re.sub(sub, "<" + empttag + "/>", text)


		text = re.sub(r'\<pb\/\>', "<zz/>", text)
		text = re.sub(r'\<gap\/\>', "<gg/>", text)

		text = re.sub(r'hi rend="underline"', "qqq", text)
		text = re.sub(r'hi rend="superscript"', "yyy", text)


		#fix hi rends... (so don't clash with hi)
		tags = ["address", "date", "salute", "del", "note", "sic",  "foreign", "p", "unclear", "add", 'qqq', 'yyy',  "hi"]

		#split = text.split(tag)
		for tag in tags:
			split = [ch for ch in re.split( r'(?<=\<)(' + tag + r')|(?<=\/)(' + tag + r')|(' + tag + r')(?=\/{0,1}\>)', text) if ch is not None]
			split = [ch for ch in split if ch != tag]

			if tag == 'hi':
				print(split)

			new_list = []

			for i, chunk in enumerate(split):
				if len(split) == 1:
					new_list.append(chunk)

				# First chunk
				elif i == 0:
					new_chunk = chunk
					if not chunk.endswith("<"):
						if not chunk.endswith("</"):
							new_chunk = chunk + "<"
					new_list.append(new_chunk)

					print(new_list)

				# Last chunk
				elif i == len(split)-1:
					new_chunk = chunk
					if not (chunk.startswith(">")):
						if chunk.startswith("/"):
							new_chunk = chunk[1:]
							new_list[i-1] = new_list[i-1] + "/"

						else:
							new_chunk = ">" + new_chunk

					new_list.append(new_chunk)
					
					print(new_list)

				else:



					new_chunk = chunk
					if not (chunk.endswith("</") or chunk.endswith("<")):
						if chunk.endswith("/"):
							new_chunk = chunk[:-1] + "</"

						else:
							new_chunk += "<"
					if not chunk.startswith(">"):
						if chunk.startswith("/"):
							new_chunk = chunk[1:]
							new_list[i-1] = new_list[i-1] + "/"
						else:
							new_chunk = ">" + new_chunk

					new_list.append(new_chunk)

			#THIS ALSO NEEDS TO BE DONE WITH > FOR FIRST!
			if new_list[-1].endswith("<") or new_list[-1].endswith("/"):
				new_list.append(">")		
			

			text = tag.join(new_list)

			if tag == "address":
				text = re.sub(r'\<address\>', '<xx>', text)
				text = re.sub(r'\<\/address\>', '</xx>', text)


		text = re.sub(r'\<xx\>', '<address>', text)
		text = re.sub(r'\<\/xx\>', '</address>', text)
			
		text = re.sub(r'\<zz\/\>', "<pb/>", text)
		text = re.sub(r'\<gg\/\>', "<gap/>", text)
		text = re.sub(r'\<qqq\>', '<hi rend="underline">', text)
		text = re.sub(r'\<yyy\>', '<hi rend="superscript">', text)

		return text

		#END of fugly cleaner function

if __name__ == '__main__':
	fix_amps = FixAmpersands('shelve_files/MLP.shelve','shelve_files/testALL_tagsCleanedNoAmps.shelve')
	fix_amps.process()
