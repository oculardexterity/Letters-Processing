import shelve
import os


with shelve.open('revision_dict.shelve') as r:
	for fname in [str(f)[:-4] for f in os.listdir('Letters 2015-12-08 0')]:
		r[fname] = {'revision': 'FLAG: abstract needs to be proofed!', 'when': '2015-12-10T15:40:20', 'who': '#RB'}