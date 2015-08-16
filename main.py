#encoding=utf-8

from querytexts import Query


if __name__ == '__main__':
	#q = Query(['corpus/pg11.txt', 'corpus/pg76.txt', 'corpus/pg5200.txt'])
	q = Query([
		'corpus_2/a foolish chicken.txt',
		'corpus_2/its my birthday today.txt',
		'corpus_2/we cannot pay for them.txt',
		'corpus_2/the boss is the largest.txt',
		'corpus_2/something is wrong with your cars.txt'
		])
	res = q.one_word_query('cock')
	#res = q.free_text_query('he hated everything')
	#res = q.phrase_query('he hated everything')
	print res
