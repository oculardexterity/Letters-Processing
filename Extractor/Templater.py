from Stream import Stream

s = Stream('output/filtered.shelve', 'Letter')
for k, v in s.stream():
	print(k, v)