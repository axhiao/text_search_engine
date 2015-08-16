#input = [file1, file2, ...]
#res = {filename: [world1, word2]}

import re
import math

class BuildIndex:

	def __init__(self, files):
		"""
		tf : term frequency
		df : document frequency: the number of docs some term shows up in
		idf : inverted document frequency
		regdex : regular index
		totalIndex : inverted index needed

		Note: totalIndex is very important because the order of entries in the converted vectors 
			  in terms of the query string and the documents is the same as that of the totalIndex.

			  tf-idf = tf * idf
		"""
		self.tf = {}
		self.df = {}
		self.filenames = files
		self.file_to_terms = self.process_files()
		self.regdex = self.regIndex()
		self.totalIndex = self.execute()

		self.vectors = self.vectorize()
		self.mags = self.magnitudes(self.filenames)
		#self.populateScores()
		self.idf = self.calc_idf()



	def process_files(self):
		"""
		Parse and tokenize the corpus of documents:
		    For every doc, firstly sanitize the doc,
		    then create a temporary hashtalbe that maps the filename to 
		    their list of tokens

		@input: filenames list 
		@return: a dict that maps the filename to their list of tokens
		"""
		file_to_terms = {}
		pattern = re.compile('[\W_]+')
		for filename in self.filenames:
			#stopwords = open('stopwords.txt').read().close()			
			with open(filename, 'r') as openfile:
				file_to_terms[filename] = pattern.sub(' ',openfile.read().lower()).strip().split(' ')
				#file_to_terms[file] = [w for w in file_to_terms[file] if w not in stopwords]
				#file_to_terms[file] = [stemmer.stem_word(w) for w in file_to_terms[file]]
		return file_to_terms


	def index_one_file(self, termlist):
		"""
		Create a dict that maps one word to a list of their position index in the file.
		The input data is from one file's words whose position index by its show-up is important

		input = [word1, word2, ...]
		output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
		"""
		fileIndex = {}
		for index, word in enumerate(termlist):
			if word in fileIndex.keys():
				fileIndex[word].append(index)
			else:
				fileIndex[word] = [index]
		return fileIndex


	def make_indices(self, termlists):
		"""
		regular index: a dict that maps the filename to their list of tokens including the show-up index
		inverted index: a dict that maps one token to the list of their filenames

		This method create the regular index from the dict - file_to_terms
		@return: regular index
		input = {filename: [word1, word2, ...], ...}
		res = { 
			filename: {word: [pos1, pos2, ...], word2: [posi,posj,...],....},
			 ...}
		"""
		total = {}
		for filename in termlists.keys():
			total[filename] = self.index_one_file(termlists[filename])
		return total




	def fullIndex(self):
		"""
		Create the inverted index that we WANTs
		Also generate the tf, df value when creating the inverted index

		@return: inverted index
		input = {filename: {word: [pos1, pos2, ...], ... }} from self.regdex
		res = {word: {filename: [pos1, pos2]}, ...}, ...}
		"""
		total_index = {}
		indie_indices = self.regdex

		for filename in indie_indices.keys():
			self.tf[filename] = {}
			for word in indie_indices[filename].keys():
				self.tf[filename][word] = len(indie_indices[filename][word]) * 1.0 / len(self.regdex[filename].keys())

				if word in self.df.keys():
					self.df[word] += 1
				else:
					self.df[word] = 1 

				if word in total_index.keys():
					if filename in total_index[word].keys():
						total_index[word][filename].append(indie_indices[filename][word][:])
					else:
						total_index[word][filename] = indie_indices[filename][word]
				else:
					total_index[word] = {filename: indie_indices[filename][word]}
		return total_index



	def vectorize(self):
		"""
		get the number of every term occurrance in every doc
		"""
		vectors = {}
		for filename in self.filenames:
			vectors[filename] = [len(self.regdex[filename][word]) for word in self.regdex[filename].keys()]
		return vectors


	def document_frequency(self, term):
		if term in self.totalIndex.keys():
			return len(self.totalIndex[term].keys()) 
		else:
			return 0



	def collection_size(self):
		"""
		return the size of corpus
		"""
		return len(self.filenames)

	def magnitudes(self, documents):
		mags = {}
		for document in documents:
			mags[document] = pow(sum(map(lambda x: x**2, self.vectors[document])),.5)
		return mags

	def term_frequency(self, term, document):
		return self.tf[document][term]/self.mags[document] if term in self.tf[document].keys() else 0



	# def populateScores(self): #pretty sure that this is wrong and makes little sense.
	# 	for filename in self.filenames:

	# 		for term in self.getUniques():
	# 			self.tf[filename][term] = self.term_frequency(term, filename)
	# 			if term in self.df.keys():
	# 				self.idf[term] = self.idf_func(self.collection_size(), self.df[term]) 
	# 			else:
	# 				self.idf[term] = 0
	# 	return self.df, self.tf, self.idf



	def calc_idf(self):
		idf = {}
		for term in self.getUniques():
			idf[term] = self.idf_func(self.collection_size(), self.df[term])
		return idf



	def cnt_showup(self, term):
		"""
		return the number of docs which contain the term
		"""
		cnt = 0;
		for filename in self.filenames:
			if self.conf_showup(term, filename):
				cnt += 1

		return cnt




	def conf_showup(self, term, filename):
		"""
		return true if term shows up in the filename
		"""
		if term in regdex[filename].keys():
			return True
		else:
			return False


	def idf_func(self, N, N_t):
		if N_t != 0:
			return math.log(N * 1.0 / N_t)
		else:
		 	return 0


	def generateScore(self, term, document):
		"""
		tf-idf value of some term in the query string = tf * idf
		"""
		if self.tf[document].has_key(term):
			return self.tf[document][term] * self.idf[term]
		else:
			return 0.0

	def execute(self):
		return self.fullIndex()

	def regIndex(self):
		return self.make_indices(self.file_to_terms)

	def getUniques(self):
		return self.totalIndex.keys()




# if __name__ == '__main__':
# 	b = BuildIndex(['corpus/pg11.txt', 'corpus/pg76.txt'])
# 	for term in b.getUniques():
# 		for filename in b.filenames:
# 			print b.generateScore(term, filename),

