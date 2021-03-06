import re
import json
import math
from string import ascii_lowercase
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import warnings



def main():
	source_file = "source/movie_review_data.json"
	points = make_points(source_file)
	clusters = make_clusters(points)



def make_points(source_file):

	print("Loading source file . . .")
	with open(source_file, 'r') as f:
		data = json.load(f)
	print("Source file loaded")

	print("Processing file data . . .")
	points = []
	re_pattern = re.compile(r"^[a-z]+$")
	for word in data:
		word = word.lower()
		if re.match(re_pattern,word):
			obj = {}
			obj['word'] = word
			obj['frequency'] = data[word]
			for c in word:
				if c in obj:
					obj[c] += 1
				else:
					obj[c] = 1
			points.append(obj)
	print("Points structure made")

	return points



def make_clusters(points):

	print("Processing letter frequency of words . . .")
	n_samples = len(points)
	X = np.zeros((n_samples,26) , dtype=np.int)
	for i in range(n_samples):
		j = 0
		for c in ascii_lowercase:
			if c in points[i]:
				X[i][j] = points[i][c]
			j += 1
	print("Letter frequency grid made")

	print("Clustering points . . .")
	n_samples_sqrt = int(math.floor(math.sqrt(n_samples)))
	batch_size = 2*n_samples_sqrt
	n_clusters = n_samples_sqrt*int(math.floor(math.sqrt(n_samples_sqrt)))
	mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size, n_init=10, max_no_improvement=10, verbose=0)
	print("Fitting data to mini batch clustering model . . .")
	warnings.filterwarnings("ignore")
	mbk.fit(X)
	mbk_means_labels = mbk.labels_
	mbk_means_cluster_centers = mbk.cluster_centers_
	print("Mini batch clustering completed")

	clusters = {}
	for i in range(n_clusters):
		clusters[i] = {}
		clusters[i]['label'] = i
		clusters[i]['center'] = mbk_means_cluster_centers[i].tolist()
		clusters[i]['points'] = []
	for i in range(n_samples):
		point = points[i]
		label = mbk_means_labels[i]
		obj = { 'word':point["word"] , 'frequency':point["frequency"] }
		clusters[label]['points'].append(obj)
	print("Clusters of points generated")

	print("Saving model . . .")
	with open('model/clusters.json', 'w') as outfile:
		json.dump(clusters,outfile)
	with open('model/clusters_indented.json', 'w') as outfile:
		json.dump(clusters,outfile,indent=2)
	print("Clusters data saved to file")



main()