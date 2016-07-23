import re
import json


def main():
	source_file = "source/movie_review_data.json"
	points = make_points(source_file)


def make_points(source_file):

	print("Loading source file . . .")
	with open(source_file, 'r') as f:
		data = json.load(f)
	print("Source file loaded")

	points = []
	re_pattern = re.compile(r"^[a-z]+$")
	for word in data:
		word = word.lower()
		if re.match(re_pattern,word):
			obj = {}
			obj['word'] = word
			obj['word_len'] = len(word)
			obj['word_score'] = data[word]
			for c in word:
				if c in obj:
					obj[c] += 1
				else:
					obj[c] = 1
			points.append(obj)
	print("Points structure made")

	with open('model/points.json', 'w') as f:
		json.dump(points,f)
	with open('model/points_indented.json', 'w') as f:
		json.dump(points,f,indent=4)
	print("Points saved to file")




main()