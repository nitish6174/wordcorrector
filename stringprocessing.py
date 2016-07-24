import jellyfish as match
import regex as re
from math import log

def stringToWords(s,allow_numeric=False):
	# wordList = s.split()
	if allow_numeric==True:
		wordList = re.sub('[^a-zA-Z0-9]',' ',s)
	else:
		wordList = re.sub('[^a-zA-Z]',' ',s)
	wordList = wordList.split()
	wordList = filter(None, wordList)
	return wordList


def lc_subsequence(X,Y):
	m = len(X)
	n = len(Y)
	L = [[None]*(n+1) for i in xrange(m+1)]
	for i in range(m+1):
		for j in range(n+1):
			if i == 0 or j == 0 :
				L[i][j] = 0
			elif X[i-1] == Y[j-1]:
				L[i][j] = L[i-1][j-1]+1
			else:
				L[i][j] = max(L[i-1][j] , L[i][j-1])

	return L[m][n]


def lc_prefix(s,t):
	s_len = len(s)
	t_len = len(t)
	l = min(s_len,t_len)
	for i in range(l):
		if s[i]!=t[i]:
			return i
	return l


def lc_suffix(s,t):
	s_len = len(s)
	t_len = len(t)
	l = min(s_len,t_len)
	for i in range(l):
		if s[s_len-i-1]!=t[t_len-i-1]:
			return i
	return l


def dl_dist(s,t):
	d = match.damerau_levenshtein_distance(unicode(s),unicode(t))
	return d

def dl_score(s,t):
	d = dl_dist(s,t)
	score = 1.0 - (3.5*d) / (len(s)+len(t))
	if len(s)<=2 and len(t)<=2:
		score = score/2
		if len(s)<2 and len(t)<2:
			score = score/2
	if score<0:
		score = 0
	return score

def dl_score_nuetral(s,t):
	d = dl_dist(s,t)
	score = 1.0 - d / log(len(s)+1,2)
	if score<0:
		score = 0
	return score

"""
dl_score:
	1-2: 0
	3-4: 1
	5-6: 2
	7-8: 3
"""
