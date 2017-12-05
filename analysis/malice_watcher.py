import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB

class MaliceWatcher:

    def __init__(self):
        self.vectorizer = CountVectorizer(ngram_range=(1, 1), stop_words='english', decode_error='ignore')
        self.clf = BernoulliNB()
        data, labels = self.build_dataset()
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True)
        X_train = self.vectorizer.fit_transform(X_train.transpose()[0])
        self.clf.fit(X_train, y_train)

    def build_dataset(self):
        isis_df = pd.read_csv('analysis/isis_tweets.csv', sep=',')
        isis_df.drop(['name', 'username', 'location', 'followers', 'numberstatuses', 'time', 'description'], axis=1, inplace=True)
        isis_df.reset_index(drop=True, inplace=True)

        benign_df = pd.read_csv('analysis/benign_tweets_2.csv', sep=',', header=None, nrows=17000)
        benign_df.drop([0, 1, 2, 3, 4], axis=1, inplace=True)
        benign_df.reset_index(drop=True, inplace=True)

        data = np.concatenate((isis_df.as_matrix(), benign_df.as_matrix()))
        labels = np.hstack((np.ones(isis_df.shape[0]), np.zeros(benign_df.shape[0])))
        return data, labels

    # 0=not malicious; 1=malicious
    def predict(self, text):
        text = np.array([text])
        text = self.vectorizer.transform(text)
        return self.clf.predict(text)[0]

if __name__ == '__main__':
    mw = MaliceWatcher()
    print(mw.predict('ISIS'))
    print(mw.predict('Syria'))
    print(mw.predict('hamburger'))
    print(mw.predict('happy'))
