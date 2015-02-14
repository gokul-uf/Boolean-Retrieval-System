''' Python script to implement the backend for the Boolean retrieval system'''

import inv_indexer
import sys
import os
import cPickle as pickle

def get_indexer(dir_name,flag= False): 

	os.chdir(dir_name)
	index_file = dir_name + ".index"
	
	if(os.path.isfile(index_file))
		index = pickle.load(open(index_file,"rb"))
		return index

	elif(flag):
		print "No index file found!, creating it now"
		inv_indexer.init(dir_name)

	else:
		print "Index file not found!, no new index file created. Exiting now!"
		exit(1)

def get_terms(search_query):
'''
	Note on query format
	--------------------
	* Looking for a query format using the !, &&, || operators for NOT AND and OR operations
	* Precedence Order: NOT > AND > OR
	* Example query: foo && bar || test && !best
'''
	sear

def get_indices(index, terms):
	
	indices = {}
	for term in terms:
		if index.has_key[term] == False:  
			indices.update({term,set([])})
		else:
			indices.update({term,index[term]})
	return indices
	
def init(search_query, search_dir,flag):

	index = get_indexer(search_dir,flag)
	terms = get_terms(search_query) #TODO
	indices = get_indices(index,terms)
#TODO: ok, now that we have the indices corresponding to each of the terms, how we gonna do the boolean operations on em?

	
if __name__ ='__main__':
	try:
		search_query = sys.argv[1]
		search_dir = sys.argv[2]
		flag = sys.argv[3]
	except IndexError:
		print ("Usage Error!!")
		print ("search.py <search_query> <search_dir> <Create index if file doesn't exist? (True/False)")
		sys.exit()
	
	init(search_query, search_dir,flag)
	
