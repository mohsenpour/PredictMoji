import pandas
import interesting_labels
from nltk.corpus import wordnet as wn
import random

def get_data():
    header = ['tweet', 'label']
    data_set = pandas.read_csv('cleaned_data.txt', delimiter='\t', names=header)
    return data_set


def get_data_set():
    return global_data_set

def num_in_classes(data):
    num_classes = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for label in data_set['label']:
        num_classes[label] += 1
    return num_classes

def create_synonym_copy(tweet):
    new_tweets = []
    new_words = {}
    for i, word in enumerate(tweet.split()):
        syns = []
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                syns.append(l.name())
        if len(set(syns)) > 0:
            new_words[i] = set(syns).pop()

    for k in range(len(new_words)):
        if k in new_words:
            message = tweet.split()
            message[k] = new_words[k]
            new_tweets.append(message)

    return new_tweets

if __name__ == '__main__':
    import nltk
    data_set = get_data()
    num_classes = num_in_classes(data_set)
    add_lines = []
    with open('cleaned_data.txt', 'r', encoding="utf8") as clean_data_file:
        with open('augmented_data_new.txt', 'a', encoding="utf8") as augmented_data_file:
            for line in clean_data_file:
                sections = line.split('\t')
                if sections[-1] not in interesting_labels.Happy:
                    copies = create_synonym_copy(sections[0])
                    for t in range(len(copies)):
                        add_lines.append((copies[t], sections[-1]))
                    #add_lines.append((create_synonym_copy(sections[0]), sections[-1]))
                augmented_data_file.write(str(sections[0]) + '\t' + str(sections[-1]))
    with open('augmented_data.txt', 'a', encoding="utf8") as augmented_data_file:
        for i in range(len(add_lines)):
            augmented_data_file.write((" ".join(add_lines[i][0])) + '\t' + (" ".join(add_lines[i][-1])))

