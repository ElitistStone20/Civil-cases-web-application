# General imports
import csv
import re
import pandas as pd
import numpy as np
import seaborn as sns

# NLTK imports
import nltk
from nltk.stem import WordNetLemmatizer

# Sklearn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Graph settings
confusion_matrix = False
comparison_accuracy = True
plot_svm = False


def classify_case(dataset, categories):
    def SVM():
        clf = svm.SVC(kernel='linear', C=5, shrinking=False, probability=True)
        # Train the model
        clf.fit(train_cases , np.ravel(categories, order='C'))
        classification = clf.predict(case_to_classify)
        print(classification)
        return classification

    train_cases = dataset.iloc[:len(dataset)-2]
    case_to_classify = np.reshape(dataset.iloc[-1], (-1, 2))
    print(case_to_classify)
    return SVM()

# Bag of words extraction of features
def extract_features(documents):
    def bag_of_words():
        tfidf = TfidfVectorizer()
        features = tfidf.fit_transform(documents)
        return pd.DataFrame(
            features.todense(),
            columns=tfidf.get_feature_names()
        )
    return bag_of_words()


def encode_categories(categories):
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoded_categories = encoder.fit_transform(categories).toarray()
    return encoded_categories


def normalise_document(documents):
    def lemitize_corpus(text):
        lemitize = WordNetLemmatizer()
        return lemitize.lemmatize(text)

    def remove_special_characters(corpus):
        pattern = r'[?|$|&|*|%|@|(|)|~|,|.|/|“|’|;|:]'
        return re.sub('[\W\_]', ' ', ' '.join(corpus))

    def remove_stopwords(document):
        document = document.split(' ')
        stopword_list = nltk.corpus.stopwords.words('english')
        filtered_tokens = [token for token in document if token not in stopword_list]
        return filtered_tokens

    normalised_corpus = remove_stopwords(documents)
    normalised_corpus = remove_special_characters(normalised_corpus)
    normalised_corpus = lemitize_corpus(normalised_corpus)
    return normalised_corpus


def load_categories(data_set):
    categories = []
    for category in data_set['Category']:
        categories.append([category])
    return categories[:-1]


def classify(description):
    data_set = pd.read_csv('./Cases_Dataset.csv')
    corpus = []
    for i in data_set['Particulars of the Claim'].values.tolist():
        corpus.append(normalise_document(i.lower()))
    corpus.append(description.lower())
    categories = load_categories(data_set)
    extracted_corpus = extract_features(corpus)
    return classify_case(extracted_corpus, categories)
