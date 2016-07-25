# Wordcorrector
**Python module to find closest matching words to a given input based on a dictionary of words.** 

**Note** : Currently used dictionary was generated from movie reviews data.  
  
### Features
- Model can be generated to correct using any list of words (english words, names, places, products, you name it)
- Fast, simple and clean
- Uses fuzzy matching method
- Takes into consideration the relative frequency of usage of words
- Number of suggestions can be varied

### Usage
1. Install the dependencies (given below)
2. Run word_corrector.py
3. Input a word when prompted. The program will return and display a list of top matches.

### Building a new dataset
1. Currently, the dictionary of words has been built using NLTK's movie review data.
2. To use another list of words, make a JSON file in ```process/source/``` folder in the following format:

  ```json
    {
      "word1" : 1,
      "word2" : 2
    }
  ```
  i.e. list of key-value pair where word will be key and its frequency/importance will be the value. Order does not matter.
  See the ```movie_review_data.json``` file for reference.
3. Open ```process/make_model.py```, specify the name of above made source file in ```main``` function and run the file.
4. The word_corrector program will now use the new dataset.

### Dependencies
- Both python 2 and python 3 are supported.
- **numpy** : http://docs.scipy.org/doc/numpy-1.10.1/user/install.html  
- **sklearn** : Not required to run the program. Needed only if you want to generate new dataset model.  
http://scikit-learn.org/stable/install.html