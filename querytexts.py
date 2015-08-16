import buildindex
import re


class Query:
	"""
	Three main methods to do the search:
	1. one_word_query : just search one word
	2. free_text_query : no consideration about the order of input words
	3. phrase_query : ensure that input words stay with the original order
	"""

	def __init__(self, filenames):
		self.filenames = filenames
		self.index = buildindex.BuildIndex(self.filenames) #consuming time
		self.invertedIndex = self.index.totalIndex
		self.regularIndex = self.index.regdex
		self.pattern = re.compile('[\W_]+')# sanitize the input


	def one_word_query(self, word):

		word = self.pattern.sub(' ',word)
		if word in self.invertedIndex.keys():
			return self.rankResults([filename for filename in self.invertedIndex[word].keys()], word)
		else:
			return []

	def free_text_query(self, string):

		string = self.pattern.sub(' ',string)
		result = []
		for word in string.split(' '):
			result += self.one_word_query(word)
		return self.rankResults(list(set(result)), string)


	def phrase_query(self, string):

		#pattern = re.compile('[\W_]+')
		string = self.pattern.sub(' ',string)
		listOfLists, result = [],[]
		for word in string.split():
			listOfLists.append(self.one_word_query(word))
		setted = set(listOfLists[0]).intersection(*listOfLists)
		for filename in setted:
			temp = []
			for word in string.split():
				temp.append(self.invertedIndex[word][filename][:])
			for i in range(len(temp)):
				for ind in range(len(temp[i])):
					temp[i][ind] -= i
			if set(temp[0]).intersection(*temp):
				result.append(filename)
		return self.rankResults(result, string)


	def make_vectors(self, documents):
		"""
		decompose the docs into corresponding vectors

		return the vectors that consist of the values of tf-idf
		converted from the terms of docs in the corpus
		"""
		vecs = {}
		for doc in documents:
			docVec = [0]*len(self.index.getUniques())
			for ind, term in enumerate(self.index.getUniques()):
				docVec[ind] = self.index.generateScore(term, doc)
			vecs[doc] = docVec
		return vecs


	def query_vec(self, query):
		"""

		decompose the query string into one vector

		REMEMBER: ** treat the query as a document to decompose **

		the vector is sparse compared with the vector of doc

		Note: the order of entries in the vector is
		      the same as that of self.index.getUniques() = BuildIndex.totalIndex.keys()
		"""
		#pattern = re.compile('[\W_]+')
		query = self.pattern.sub(' ',query)
		queryls = query.split()
		queryVec = [0]*len(queryls)
		#index = 0
		for ind, word in enumerate(queryls):
			queryVec[ind] = self.queryFreq(word, query)
			#index += 1

		wordsidf = [self.index.idf[word] for word in self.index.getUniques()]


		magnitude = pow(sum(map(lambda x: x**2, queryVec)), .5)

		# every word in the self.index.getUniques() show-up times in the query
		freq = self.termfreq(self.index.getUniques(), query)


		#print('THIS IS THE FREQ')
		tf = [x/magnitude for x in freq]

		#print wordsidf

		final = [  tf[i]*wordsidf[i] for i in xrange(len(self.index.getUniques()))   ]
		#print(len([x for x in queryidf if x != 0]) - len(queryidf))

		return final



	def queryFreq(self, term, query):
		"""
		return the count for the term occurrence
		in the query string
		"""
		count = 0
		for word in query.split():
			if word == term:
				count += 1
		return count



	def termfreq(self, terms, query):
		temp = [0]*len(terms)
		for i,term in enumerate(terms):
			temp[i] = self.queryFreq(term, query)
			#print(self.queryFreq(term, query))
		return temp




	def dotProduct(self, doc1, doc2):
		if len(doc1) != len(doc2):
			return 0
		return sum([x*y for x,y in zip(doc1, doc2)])




	def rankResults(self, resultDocs, query):
		"""
		calc the similarity between two vectors with
		cosine similarity
		1. decompose the docs into vectors
		2. decompose the query string into vector
		3. compute the dotProduct between the vector of docs vectors
		   and the query vector, respectively
		"""
		## express docs with vectors
		vectors = self.make_vectors(resultDocs)
	
		## express the query string with vector
		queryVec = self.query_vec(query)
		#print(queryVec)

		## calc the similarity with cosine similarity
		## i.e., doc vector docproducts the query vector
		results = [[self.dotProduct(vectors[result], queryVec), result] for result in resultDocs]

		## sort the results in descending order by the dotProduct
		results.sort(key=lambda x: x[0], reverse = True)
		## get the final output list
		results = [x[1] for x in results]
		return results
