import jinja2
import os

from Stream import Stream





templateFile = open("Jinja_templateProof.xml").read() 
env = jinja2.Environment()
env.globals.update(sorted=sorted)

template = env.from_string(templateFile)


s = Stream('output/fixAmperands.shelve', 'Letter')
for key, item in s.stream():
	templatedText = template.render(item)
	f = open('xmlfiles/'+key+".xml", 'w')
	f.write(templatedText)
	f.close()