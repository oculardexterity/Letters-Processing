text = """
And then the man said something <addressand then he carried on and it was great<address/> and somethign something
"""
print(text)
tags = "address".split()

split = text.split(tags[0])

print(split)

new_list = []

for i, chunk in enumerate(split):

	if i == 0:
		new_chunk = chunk
		if not chunk.endswith("<"):
			new_chunk = chunk + "<"
		new_list.append(new_chunk)

	elif i == (2):
		new_chunk = chunk
		if not (chunk.startswith(">")):
			if chunk.startswith("/"):
				new_chunk = chunk.replace("/","")
				new_list[i-1] = new_list[i-1] + "/"

			else:
				new_chunk = ">" + new_chunk
		new_list.append(new_chunk)
	
	else:
		new_chunk = chunk
		if not (chunk.endswith("</") or chunk.endswith("<")):
			if chunk.endswith("/"):
				new_chunk = chunk[:-1] + "</"

			else:
				new_chunk += "<"
		if not (chunk.startswith(">") or chunk.startswith("/")):
			if chunk.startswith("/"):
				new_chunk = chunk.replace("/","")
				new_list[i-1] = new_list[i-1] + "/"
			else:
				new_chunk = ">" + new_chunk

		new_list.append(new_chunk)

print(new_list)

print(tags[0].join(new_list))
