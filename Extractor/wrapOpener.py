import re as re
from EditLogger import EditLogger
from Processor import Processor as Processor

'''
Class for wrapping opener/closer --- classed for namespace convenience
'''
class WrapperUtils:

	def __init__(self, temp_wrapper=False):
		re.purge()
		self.temp_wrapper = temp_wrapper
		
		

	def wrap_element_with_tags(self, text, elem_to_wrap, wrapping_element):
		regex = r'(<' + elem_to_wrap + r'>[\s\S]*?</' + elem_to_wrap + r'>)'
		pattern = re.compile(regex)
		result = pattern.findall(text)
		text = text
		for r in set(result):
			text = re.sub(r, r'<' + wrapping_element + r'>' + r + r'</' + wrapping_element + '>', text)

		return text

	def find_positions_of_matches(self, text, previous_end=0, pieces=[]):
		try:
			re.purge()
			self.find_temp_segments_regex = re.compile(r'[^(<p>)]<' + self.temp_wrapper + r'>[\s\S]*?</' + self.temp_wrapper + r'>[\s\n\t]??')
			re.purge()
			result = self.find_temp_segments_regex.search(text, previous_end)
			re.purge()
		except Exception as e:
			print('findpos_error')
			raise e
		try:
			rg = result.group()
			print(rg)
			rs = result.start()
			ren = result.end()
			pieces.append((rs,ren,rg))
			return self.find_positions_of_matches(text, previous_end=ren, pieces=pieces)
		except:
			print(pieces)
			return pieces

	def find_contiguous_pieces(self, pieces, threshold=100):
		try:
			cont_pieces = []
			start_pos = pieces[0][0]
			last_pos = pieces[0][1]
			pieces_count = 1
			for i, piece in enumerate(pieces):
				try:
					if piece[1] + threshold >= pieces[i+1][0]:
						pieces_count += 1
						last_pos = pieces[i+1][1]
					else:
						cont_pieces.append((start_pos, last_pos, pieces_count))
						start_pos = pieces[i+1][0]
						last_pos = pieces[i+1][1]
						pieces_count = 1
				except:
					cont_pieces.append((start_pos, piece[1], pieces_count))
					sorted_cont_pieces = sorted(cont_pieces, key=lambda piece: piece[0])
					#print(sorted_cont_pieces)
					return sorted_cont_pieces
		except IndexError:
			raise



	# Bunch of utility processing functions

	# Grabs the segment of text from its start and end positions
	def get_segment(self, text, s,e):
		try:
			regex = r'[\s\S]*'
			re.purge()
			pattern = re.compile(regex)
			print(pattern)
			
			try:
				segment = pattern.search(text,s,e).group()
				
				return segment
			except Exception as e:
				print('getseg regex err -', e)
				raise e
			
		except Exception as e:
			print('getseg error', e)
			raise e

	# Strips temp tags from some text (looks more complicated than just re.sub, but dunno why...)
	# Q. above: A. I think to remove internal TEMPS; Used by fix-opener and fix-closer -wraps()
	def strip_internal_temps(self, text):
		regex = r'</TEMP>(?=[\s\S]*?<\/TEMP\>)'
		text = re.sub(regex, '', text)
		regex = r'<TEMP>'[::-1] + r'(?=[\s\S]*?' + r'<TEMP>'[::-1] + r')'
		text = re.sub(regex,'',text[::-1])[::-1]
		return text

	# Do as they say on tin; don't know why they can't be one function though...
	def fix_opener_wraps(self, segment):
		segment = self.strip_internal_temps(segment)
		return re.sub(r'TEMP', 'opener', segment)

	def fix_closer_wraps(self, segment):
		segment = self.strip_internal_temps(segment)
		return re.sub(r'TEMP', 'closer', segment)



	def wrap_pieces_in_text(self, text, ordered_cont_pieces):
		text_length = len(text)
		text = text
		if text:
			print('wp text in ok')
		try: 
		
			try:
				re.purge()
				opener_segment = self.get_segment(text, ordered_cont_pieces[0][0], ordered_cont_pieces[0][1])
			except Exception as e:
				print('wp_openseg error')
				raise e
			try:
				re.purge()
				closer_segment = self.get_segment(text, ordered_cont_pieces[-1][0], ordered_cont_pieces[-1][1])
			except Exception as e:
				print('wp_closeg error')
				raise e
			# Maybe some more checking in case there's some shit at the top/bottom? -- i.e. check
			# by length or content?	
			
			try:
				if ordered_cont_pieces[-1][1] > text_length * 0.7 and '<salute>' in closer_segment:
					text = re.sub(closer_segment, self.fix_closer_wraps(closer_segment), text)
			except Exception as e:
				print('wp closersub failed')
				raise e

			try:
				text = re.sub(opener_segment, self.fix_opener_wraps(opener_segment), text)	
			except Exception as e:
				print('wp openersub failed')
				print(e)
		
			print('wp_ index error not triggered')
		except IndexError: # presumably from fail if there is only one segment identified
			print('wp_index error')
			opener_segment = self.get_segment(text, cont_pieces[0][0], cont_pieces[0][1])
			text = re.sub(opener_segment, self.fix_opener_wraps(opener_segment), text)
		except Exception as e:

			print('wp_general exception', e)
			raise e
		# Remove all remaining temps
		text = re.sub(r'<TEMP>','',text)
		text = re.sub(r'</TEMP>','',text)
		#print(text)
		return text




'''
THE MAIN PROCESSOR CLASS STARTS HERE
'''


class WrapOpenerAndCloser(Processor):
	def __init__(self, inputFilePath, outputFilePath):
		self.resolve = self.wrap_opener_and_closer
		self.transform = self.wrap_opener_and_closer
		self.dict_key = 'Letter'
		self.inputFilePath = inputFilePath
		self.outputFilePath = outputFilePath
		
		super().__init__()

	def wrap_opener_and_closer(self, row):
		new_row = row
		
		#
		l_list = [1038,1039,1040]
		if row["Type"] == 'Letter' and (row["Letter"] in l_list):
			print('--------')
			print(row["Letter"], row["Type"])
			text = self._merged_pages(row['Pages'])
			text = self._wrap_opener_and_closer_process(text)
			split = self._split_pages(text)
			new_row["Pages"] = self._build_new_page_row(row['Pages'], split)
		# Implicitly, else do nothing	
		
		return new_row
		

	def _merged_pages(self, pages):
		def page_ok_to_include(k, v):
			print(k, v["PageType"] )
			if v["Translation"] and v["PageType"] =='PageType':
				return True
			else:
				return False

		text = "§§\n".join([str(v["Translation"]) for k, v in sorted(pages.items()) if page_ok_to_include(k, v)])
		return(text)
			
	def _split_pages(self, pages_text):
		split = pages_text.split('§§\n')
		#print(len(split))
		return split

	def _build_new_page_row(self, pages, split):
		new_page_dict = pages
		for page_text, page_d in zip(split, sorted(pages.items())):
			new_page_dict[page_d[0]]["Translation"] = page_text
		return new_page_dict




	def _wrap_opener_and_closer_process(self, text):
		print(text)
		self.WU = WrapperUtils('TEMP')
		print(self.WU)
		
		# List of tags to consider
		tags_in_opener_and_closer =  ['salute', 'dateline', 'date', 'address', 'signed']
		self.letter_text = text
		for tag in tags_in_opener_and_closer:
			self.letter_text = self.WU.wrap_element_with_tags(self.letter_text, tag, 'TEMP')
		pieces = []
		pieces = self.WU.find_positions_of_matches(self.letter_text)
		if pieces:
			print('Pieces ok')
		try:
			contiguous_pieces = self.WU.find_contiguous_pieces(pieces)
			if contiguous_pieces:
				print('cont_pieces ok')
			opener_closer_fixed_text = self.WU.wrap_pieces_in_text(self.letter_text, contiguous_pieces)
			print('SUCCESS')
			#print(opener_closer_fixed_text)
			return opener_closer_fixed_text
		except Exception as e:
			#Maybe raise error and log higher up??)
			print('FAIL', e)
			return text		




if __name__ == '__main__':
	w = WrapOpenerAndCloser('shelve_files/pageTypesLogged.shelve', 'shelve_files/WrapOpenerAndCloser.shelve')
	w.process()