import sys
import os

sys.path.append('/Users/mananaggarwal/miniconda3/lib/python3.6/site-packages')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report


# wraps a scikit-learn SVM classifier
class Classifier():

    # train classifier
    def __init__(self):
        data_dir = '../sentiment_analysis/review_polarity/txt_sentoken/'
        classes = ['pos', 'neg']

        # Read the data
        train_data = []
        train_labels = []
        for curr_class in classes:
            dirname = os.path.join(data_dir, curr_class)
            for fname in os.listdir(dirname):
                with open(os.path.join(dirname, fname), 'r') as f:
                    content = f.read()
                    if not fname.startswith('cv9'):
                        train_data.append(content)
                        train_labels.append(curr_class)

        # Create feature vectors
        self.vectorizer = TfidfVectorizer(min_df = 5,
                                     max_df = 0.8,
                                     sublinear_tf = True,
                                     use_idf = True)
        train_vectors = self.vectorizer.fit_transform(train_data)

        # Perform classification with SVM, linear kernel
        self.classifier_liblinear = svm.LinearSVC()
        self.classifier_liblinear.fit(train_vectors, train_labels)

    # takes a file in '<sender>: <message>' format
    # returns tuple of classifications for every message in input file
    def classify_from_file(self, data_file):
        you_data = []
        friend_data = []

        for l in data_file:
            s = l.split(':')
            if len(s) > 1:
                if s[0] == 'You':
                    you_data.append(s[1])
                else:
                    friend_data.append(s[1])

        return self.classify_from_lists(you_data, friend_data)

    def classify_from_lists(self, you_messages, friend_messages):
        you_vectors = self.vectorizer.transform(you_messages)
        friend_vectors = self.vectorizer.transform(friend_messages)

        you_prediction = self.classifier_liblinear.predict(you_vectors)
        friend_prediction = self.classifier_liblinear.predict(friend_vectors)

        return (you_prediction, friend_prediction)
