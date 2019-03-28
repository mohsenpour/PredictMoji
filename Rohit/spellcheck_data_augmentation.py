import pandas
from symspellpy.symspellpy import SymSpell  # import the module
import os

def get_data():
    header = ['tweet', 'label']
    data_set = pandas.read_csv('cleaned_data.txt', delimiter='\t', names=header)
    return data_set

def num_in_classes(data):
    num_classes = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for label in data_set['label']:
        num_classes[label] += 1
    return num_classes

def correct_spelling( sentence ):
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 5
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return
    if "&amp ;" in sentence:
        sentence = sentence.replace("&amp ;", "and")
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(sentence, max_edit_distance_lookup)
    save = ""
    for suggestion in suggestions:
        save = suggestion.term
        #print("{}".format(save))
        break;


    #if "#" in save:
    #    save = sym_spell.word_segmentation(save)

    return save


if __name__ == '__main__':
    data_set = get_data()
    num_classes = num_in_classes(data_set)
    with open('cleaned_data.txt', 'r', encoding="utf8") as clean_data_file:
        with open('augmented_data_spelling.txt', 'a', encoding="utf8") as augmented_data_file:
            for line in clean_data_file:
                sections = line.split('\t')
                augmented_data_file.write(str(correct_spelling(sections[0])) + '\t' + str(sections[-1]))

