import nltk
import re
import string
from pprint import pprint


class NLP(object):
    def __init__(self):
        self.CONTRACTION_MAP = {
            "isn't": "is not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "could've": "could have",
            "didn't": "did not",
            "doesn't": "does not",
            "you'll've": "you will have",
            "you're": "you are",
            "you've": "you have",
            "we're" : "we are",
            "haven't": "have not",
            "hasn't": "has not",
            "how'll": "how will",
            "i'd": "i had",
            "i'll": "i will",
        } 


    def normalise_corpus(self, corpus, tokenize=False):
        # Tokenize the text after processing is done
        def tokenize_text(text_to_process):
            sentences = nltk.sent_tokenize(text_to_process)
            word_tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
            return word_tokens

        # Removing special characters with no relevance to the text
        def remove_special_chars(sentence):
            sentence = sentence.strip()    
            PATTERN = r'[?|$|&|*|%|@|(|)|~]'
            filtered_sentence = re.sub(PATTERN, r'', sentence)
            return filtered_sentence
        

        def expand_contractions(sentence, contraction_map):
            contractions_pattern = re.compile('({0})'.format('|'.join(self.CONTRACTION_MAP.keys())), flags=re.IGNORECASE|re.DOTALL)

            def expand_match(contraction):
                match = contraction.group(0)
                first_car = match[0]
                expanded_contraction = self.CONTRACTION_MAP.get(match) \
                                       if self.CONTRACTION_MAP.get(match) \
                                       else self.CONTRACTION_MAP.get(match.lower())
                expanded_contraction = first_car + expanded_contraction[1:]
                return expanded_contraction
            
            expanded_sentence = contraction_map.sub(expand_match, sentence)
            return expanded_sentence
        
        def remove_stopwords(tokens):
            stopword_list = nltk.corpus.stopwords.words('english')
            filtered_tokens = [token for token in tokens if token not in stopword_list]
            return filtered_tokens


        def convert_case(sentence):
            return sentence.lower()
        

        normalised_corpus = []
        for text in corpus:
            text = convert_case(text)
            text = expand_contractions(text, self.CONTRACTION_MAP)
            text = remove_special_chars(text)
            text = remove_stopwords(text)
            if tokenize:
                text = tokenize_text(text)
            normalised_corpus.append(text)
        return normalised_corpus
    

    def classify_case(self, case):
        case_type = ""
        normalised_corpus = self.normalise_corpus(case, True)
        return case_type



