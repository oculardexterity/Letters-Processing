import re
from Processor import Processor as Processor

'''
Class for wrapping opener/closer --- classed for namespace convenience
'''
class WrapperUtils:

	def __init__(self, temp_wrapper=False):
		self.temp_wrapper = temp_wrapper
		if self.temp_wrapper:
			self.find_temp_segments_regex = re.compile(r'[^(<p>)]<' + self.temp_wrapper + r'>[\s\S]*?</' + self.temp_wrapper + r'>[\s\n\t]??')

	def wrap_element_with_tags(self, text, elem_to_wrap, wrapping_element):
		regex = r'(<' + elem_to_wrap + r'>[\s\S]*?</' + elem_to_wrap + r'>)'
		pattern = re.compile(regex)
		result = pattern.findall(text)
		#print(result)
		for r in set(result):
			text = re.sub(r, r'<' + wrapping_element + r'>' + r + r'</' + wrapping_element + '>', text)
		return text

	def find_positions_of_matches(self, pattern_as_regex, text, previous_end=0, pieces=[]):
		result = pattern_as_regex.search(text, previous_end)
		try:
			rg = result.group()
			rs = result.start()
			re = result.end()
			pieces.append((rs,re,rg))
			return self.find_positions_of_matches(pattern_as_regex, text, previous_end=re, pieces=pieces)
		except:
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
		regex = r'[\s\S]*'
		pattern = re.compile(regex)
		segment = pattern.search(text,s,e).group()
		
		return segment

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

		try: 
		

			opener_segment = self.get_segment(text, ordered_cont_pieces[0][0], ordered_cont_pieces[0][1])
			closer_segment = self.get_segment(text, ordered_cont_pieces[-1][0], ordered_cont_pieces[-1][1])
			# Maybe some more checking in case there's some shit at the top/bottom? -- i.e. check
			# by length or content?	
			

			if ordered_cont_pieces[-1][1] > text_length * 0.7 and '<salute>' in closer_segment:
				text = re.sub(closer_segment, self.fix_closer_wraps(closer_segment), text)

			text = re.sub(opener_segment, self.fix_opener_wraps(opener_segment), text)	
			
		

		except IndexError: # presumably from fail if there is only one segment identified
			opener_segment = self.get_segment(text, cont_pieces[0][0], cont_pieces[0][1])
			text = re.sub(opener_segment, self.fix_opener_wraps(opener_segment), text)
		
		# Remove all remaining temps
		text = re.sub(r'<TEMP>','',text)
		text = re.sub(r'</TEMP>','',text)
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
		text = self._merged_pages(row['Pages'])
		print(text)

		print('-----------------------------------------------')

		text = self._wrap_opener_and_closer_process(text)

		print(text)

		print('===============================================')
		split = self._split_pages(text)
		new_row["Pages"] = self._build_new_page_row(row['Pages'], split)
		return new_row
		

	def _merged_pages(self, pages):
		text = "§§\n".join([str(v["Translation"]) for k, v in sorted(pages.items()) if v["Translation"]])
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
		
		def wrap_element_with_tags(text,elems_to_wrap,wrapping_element):
			for elem_to_wrap in elems_to_wrap:

				regex = r'(<' + elem_to_wrap + r'>[\s\S]*?</' + elem_to_wrap + r'>)'
				#regex = r'(<address>[\s\S]*?</address>)'
				pattern = re.compile(regex)
				result = pattern.findall(text)
				for r in result:
					text = re.sub(r, r'<' + wrapping_element + r'>' + r + r'</' + wrapping_element + '>', text)
				print("(E", elem_to_wrap,text[:200], ')\n\n')
			return text

		

		def iter_search(pattern, text, previous_end=0, pieces=[]):
			result = pattern.search(text, previous_end)
			try:
				rg = result.group()
				rs = result.start()
				re = result.end()
				print('----- \nRG, RS, RE', rg, rs, re, '\n-------')
				pieces.append((rs,re,rg))
				return iter_search(pattern,text, previous_end=re, pieces=pieces)
			except:
				return pieces

		text = '<text>\n' + re.sub('\n\n<date>15.7.16 9.30PM', '12 January', text) + '\n</text>'
		text = wrap_element_with_tags(text, ['address', 'salute', 'date'], 'TEMP')	
		regex = r'[^(<p>)]<TEMP>[\s\S]*?</TEMP>[\s\n\t]??'
		pattern = re.compile(regex)
		pieces = iter_search(pattern,text)
		print(pieces)

		def find_contiguous_pieces(pieces,threshold=400):
			cont_pieces = []
			start_pos = pieces[0][0]
			last_pos = 0
			pieces_count = 1
			for i, piece in enumerate(pieces):
				try:
					#print piece
					if piece[1] + threshold >= pieces[i+1][0]:
						pieces_count += 1
						last_pos = pieces[i+1][1]
						#print 'thistrue', start_pos, last_pos, pieces_count
					else:
						#print '-----------'
						cont_pieces.append((start_pos, last_pos, pieces_count))
						start_pos = pieces[i+1][0]
						last_pos = pieces[i+1][1]
						pieces_count = 1
				except:
					cont_pieces.append((start_pos, piece[1], pieces_count))
					return cont_pieces


		cont_pieces = find_contiguous_pieces(pieces)

		sorted_cont_pieces = sorted(cont_pieces, key=lambda piece: piece[2], reverse=True)
		print(sorted_cont_pieces)

		def strip_temps(text):
			#print text
			regex = r'</TEMP>(?=[\s\S]*?<\/TEMP\>)'
			text = re.sub(regex, '', text)
			regex = r'<TEMP>'[::-1] + r'(?=[\s\S]*?' + r'<TEMP>'[::-1] + r')'
			text = re.sub(regex,'',text[::-1])[::-1]
			return text

		def fix_opener_wraps(segment):
			segment = strip_temps(segment)
			return re.sub(r'TEMP', 'opener', segment)

		def fix_closer_wraps(segment):
			segment = strip_temps(segment)
			return re.sub(r'TEMP', 'closer', segment)

		def get_segment(s,e):
			regex = r'[\s\S]*'
			pattern = re.compile(regex)
			try:
				segment = pattern.search(text,s,e).group()
			return segment

		def fix_pieces(text,cont_pieces):
			text_length = len(text)

			try: # will fail if cont_pieces has only one thing...
				# move these out to is_opener function...
				if cont_pieces[0][0] < cont_pieces[1][0] and cont_pieces[0][0] < len(text)*0.5: # First is the opener
					opener_segment = get_segment(cont_pieces[0][0], cont_pieces[0][1])
					
					#closer segment is at the end... OR... contains Salute?
					closer_segment = get_segment(cont_pieces[1][0], cont_pieces[1][1])
					
					if '<salute>' in closer_segment:
						text = re.sub(closer_segment,fix_closer_wraps(closer_segment),text)
					text = re.sub(opener_segment,fix_opener_wraps(opener_segment),text)

				
				elif cont_pieces[1][0] < cont_pieces[0][0] and cont_pieces[1][0] < len(text)*0.5:
					opener_segment = get_segment(cont_pieces[1][0], cont_pieces[1][1])			
					closer_segment = get_segment(cont_pieces[0][0], cont_pieces[0][1])

					if '<salute>' in closer_segment:
						text = re.sub(closer_segment,fix_closer_wraps(closer_segment),text)

					text = re.sub(opener_segment,fix_opener_wraps(opener_segment),text)
			
			except IndexError: # presumably from fail if there is only one segment identified
				opener_segment = get_segment(cont_pieces[0][0], cont_pieces[0][1])
				text = re.sub(opener_segment,fix_opener_wraps(opener_segment),text)
				
			text = re.sub(r'<TEMP>','',text)
			text = re.sub(r'</TEMP>','',text)
			return text


		return fix_pieces(text,sorted_cont_pieces)








if __name__ == '__main__':
	w = WrapOpenerAndCloser('shelve_files/tagsCleaned.shelve', 'shelve_files/WrapOpenerAndCloser.shelve')
	w.process()