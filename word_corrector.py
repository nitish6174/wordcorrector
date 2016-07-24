import json
import math
import numpy as np
from stringprocessing import *


def main():

	print("Enter word to correct :")
	input_word = raw_input()

	result_len = 5

	res = correct(input_word,result_len)
	print("\nTop matches:")
	show(res)
	


def correct(input_word,result_len,show_score=False):
	with open('process/model/clusters.json', 'r') as f:
		clusters = json.load(f)
	word_letter_freq = getDistribution(input_word)

	center_list = []
	for i in range(len(clusters)):
		obj = {}
		obj["cluster_label"] = i
		center_coords = clusters[str(i)]["center"]
		obj["vector_dist"] = np.linalg.norm(word_letter_freq-center_coords)
		center_list.append(obj)
	center_list.sort(key=lambda x: x['vector_dist'], reverse=False)
	center_list_len = len(center_list)
	clusters_to_check = intSqrt(center_list_len)

	words_to_check = []
	for i in range(clusters_to_check):
		cluster_label = center_list[i]["cluster_label"]
		for point in clusters[str(cluster_label)]["points"]:
			words_to_check.append(point)
	res = getBestMatch(input_word,words_to_check,result_len)
	if show_score==True:
		return res
	else:
		return [ x["word"] for x in res ]



def getBestMatch(input_word,words_to_check,result_len):
	match_threshold = 0
	result = []
	for lookup_word_object in words_to_check:
		lookup_word = lookup_word_object["word"]
		match_score = getMatchRelevanceScore(input_word,lookup_word_object)
		frequency_score = getFrequencyScore(lookup_word_object["frequency"])
		if match_score>=match_threshold:
			result.append({ 'word':lookup_word , 'match_score':match_score , 'frequency_score':frequency_score })
		if len(result)>2*result_len:
			result.sort(key=lambda x: x['match_score'], reverse=True)
			result = result[:result_len]
			match_threshold = result[result_len-1]["match_score"]
	result.sort(key=lambda x: x['match_score'], reverse=True)
	result = result[:result_len]

	for item in result:
		item["total_score"] = item["match_score"] + item["frequency_score"]
	result.sort(key=lambda x: x['total_score'], reverse=True)
	return result



def getMatchRelevanceScore(typed_word,lookup_word_obj):
	"""
	factors:
		0: constant
		1: frequency
		2: word distance score
		3: longest common prefix
		4: longest common suffix
	"""
	lookup_word = lookup_word_obj["word"]
	frequency = lookup_word_obj["frequency"]
	scores = np.zeros(5)
	score_factors = np.array([ 1.0 , 0.1 , 4.0 , 1.0 , 0.5 ])
	word_score = 0
	typed_word_len = len(typed_word)
	lookup_word_len = len(lookup_word)

	scores[1] = math.log(frequency+1,10)

	if typed_word_len>0 and lookup_word_len>0:
		scores[2] = dl_score_nuetral(typed_word,lookup_word)
		temp = lc_prefix(typed_word,lookup_word)
		if temp>1:
			scores[3] = scores[2]*math.log(temp+1,2)
		temp = lc_suffix(typed_word,lookup_word)
		if temp>1:
			scores[4] = scores[2]*math.log(temp+1,2)

	word_score = score_factors.transpose().dot(scores)
	return word_score



def getFrequencyScore(frequency):
	return math.log(frequency+1,10)


def getDistribution(word):
	word_letter_freq = np.zeros(26)
	for c in word:
		if c.isalpha():
			word_letter_freq[ord(c)-ord('a')] += 1
	return word_letter_freq


def intSqrt(n):
	return int(math.floor(math.sqrt(n)))


def show(obj):
	print(json.dumps(obj,indent=2))



main()