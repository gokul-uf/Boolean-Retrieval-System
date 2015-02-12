'''

python script to take in a directory which has a list of files and 
create a .index file which has the inverted index of all files

List of common stop words, sourced from : http://www.textfixer.com/resources/common-english-words.txt

NOTE (can be fixed in future)
-----------------------------
	
	* Need to specify directory explicitly SOLN: can provide the default as current directory
	* Need to do exception checking in several places SOLN: do it =)
	* Currently works on a single level directly, not recursively SOLN: os.walk() comes to rescue
	* Recreates the complete index every time it is called SOLN: maybe use cPickle with wb+ 
	* Uses '/' as the separator for file directories, works only on *NIX SOLN: have an adaptor class for the separator
	* Does not index numbers 
	* case insensitive
	* Indexes hypenated words separately;ex co-op is indexed as co and op
	* Stemming not done (assume and assumed are different) SOLN: Implement porter's algorithm
	* Doesn't store where in document token was found
	* Doesn't store the number of times the token appears in a document;could use that for ranking SOLN: change the indexing data structure slightly
	* Doesn't have the size of the posting list; assuming python set's intersection operation takes care of things SOLN: same as above


'''


import sys
import os
import datetime
import re
import cPickle as pickle

stop_words = set(["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"])

#Creates the token list for filename
def indexer (filename):

	print("creating index for "+filename)
	
	source = open(filename,"r")
	tokens = set([])

	# read in a file, one line at a time and remove stop words
	for line in source: 
		line = re.sub("[^a-zA-Z]"," ",line) 
		token_list = (line.lower().split())
		
		for tk in token_list:
			if tk not in stop_words:
				tokens.add(tk)
			
	source.close()
	print("creating file: "+filename+".index")
	pickle.dump(tokens,open(filename+".index","wb"))
	print("index for "+filename+" created successfully!")




#Takes a directory listing, opens up the individual file's index and reduces them into an inverted index	
def reducer (dir_list,dir_name):
	
	index = dict() 
	
	for filename in dir_list:

		file_tokens = pickle.load(open(filename+".index","rb"))	
		
		for token in file_tokens:
			if index.has_key(token): #the token has been encountered previously
				index[token].add(filename)

			else: #add token to the index
				index.update({token:set([filename])})
				
			
		print ("Index of "+filename+" successfully incorporated into main index!")
		print("ALERT: Removing index of "+filename)
		os.remove("./"+filename+".index")

	pickle.dump(index,open(dir_name+".index","wb"))

	
def init():

	try:
		dir_name = sys.argv[1]
	
	except IndexError:
		print("Error!! Usage: inv_indexer.py <dir_name>")
		sys.exit()
	
	try:
		os.chdir(dir_name)
	
	except WindowsError, OSError:
		print("Error opening directory, exitting")
		sys.exit()
	print("Index creation started at "+str(datetime.datetime.now()))	
	dir_name = os.getcwd() 
	dir_list = os.listdir(dir_name)
	dir_list = [filename for filename in dir_list if os.path.isfile('./'+filename)] #assuming a flat file structure
	if "inv_indexer.py" in dir_list:
		dir_list.remove("inv_indexer.py") #no need to index the script :p

	dir_name = (dir_name.split('/'))[-1] # We'll get just the curdir name	

	for filename in dir_list:
		indexer(filename)
	
	reducer(dir_list,dir_name)
	print("Index successfully created at "+str(datetime.datetime.now()))

if __name__ == '__main__':
	init()
