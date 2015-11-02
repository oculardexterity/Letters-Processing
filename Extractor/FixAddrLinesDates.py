from Processor import Processor
import HelperFunctions as HF
import WrapperUtils as WU


class FixAddrLineDate(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self._fix
		self.transform = self._fix
		self.dict_key = 'Letter'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath

		super().__init__()


	def _fix(self, row):
		new_row = row
		#print(row["Letter"])
		text = self._merged_pages(row['Pages'])
		if row:
			
			#print(text)
			print('--------')

			try:
				extracted_opener = HF.extractTagContents(text, 'opener')
				#print(extracted_opener[0])
				extracted_address = HF.extractTagContents(extracted_opener[0], 'address')
				#print('----')
				##print(extracted_address[0])
				try:
					wrapped = HF.wrapOnEmptyElementSplit(extracted_address[0],'lb','addrLine')
					#print(wrapped)
					#print('------')
					text = text.replace(extracted_address[0], wrapped)

					#print(text)
				except IndexError:
					print('No address')
			except Exception:
				print('nameError')

			print('-----')

			try:
				extracted_opener = HF.extractTagContents(text, 'opener')
				#print(extracted_opener[0])
				#print('-----')
				dateline_wrapped = WU.wrap_element_with_tags(extracted_opener[0], 'date', 'dateline')
				#print(dateline_wrapped)
				#print('-----')
				text = text.replace(extracted_opener[0], dateline_wrapped)
				#print(text)
			except:
				print('DATEERROR')

			try:
				extracted_opener = HF.extractTagContents(text, 'opener')
				#print(extracted_opener)
				lb_stripped = extracted_opener[0].replace("<lb/>","")
				#print(lb_stripped)
				text = text.replace(extracted_opener[0], lb_stripped)
				#print(text)
			except:
				print('DATEERROR')
		print(text)
		split = self._split_pages(text)
		new_row["Pages"] = self._build_new_page_row(row['Pages'], split)
		return new_row



	def _merged_pages(self, pages):
		
		def page_ok_to_include(k, v):
			if v["Translation"]:
				return True
			else:
				return False

		text = "§§\n".join([str(v["Translation"]) for k, v in sorted(pages.items()) if page_ok_to_include(k, v)])
		return text
			
	def _split_pages(self, pages_text):
		split = pages_text.split('§§\n')
		#print(len(split))
		return split

	def _build_new_page_row(self, pages, split):
		new_page_dict = pages
		for page_text, page_d in zip(split, sorted(pages.items())):
			new_page_dict[page_d[0]]["Translation"] = page_text
		return new_page_dict




if __name__ == '__main__':
	f = FixAddrLineDate('shelve_files/WrapOpenerAndCloser.shelve', 'shelve_files/AddrLineDatesFixed.shelve')
	f.process()