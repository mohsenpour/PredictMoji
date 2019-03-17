'''
script to do all the data processing on the processed.txt file

we do the following procesudures here:
1. remove the tweets with labels that are not in interesting_labels.wanted_list
2. remove the tweets with empty tweet text
3. map the tweet labels to classes
'''

import interesting_labels

def class_mappings():
    return {'Happy':0, 'Sad':1 ,'Angry':2, 'Surprised': 3, 'Disgusted':4, 'Afraid':5 }

def get_classes(label):
    '''
    given a label, this function returns a list of classes that the label belongs to
    '''
    mapping = class_mappings()
    classes = []
    if(label in interesting_labels.Happy):
        classes.append(mapping['Happy'])
    if (label in interesting_labels.Sad):
        classes.append(mapping['Sad'])
    if (label in interesting_labels.Angry):
        classes.append(mapping['Angry'])
    if (label in interesting_labels.Surprised):
        classes.append(mapping['Surprised'])
    if (label in interesting_labels.Disgusted):
        classes.append(mapping['Disgusted'])
    if (label in interesting_labels.Afraid):
        classes.append(mapping['Afraid'])
    return classes


def final_tweet_cleanup(tweet):
    tweet = tweet.replace(".", " . ") \
                 .replace(",", " , ") \
                 .replace(";", " ; ") \
                 .replace("?", " ? ") \
                 .replace("\'", "")
    return tweet.lower()

if __name__ == '__main__':
    with open('processed.txt','r') as raw_data_file:
        with open('cleaned_data.txt', 'a') as cleaned_data_file:
            for line in raw_data_file:
                whole_line = line.split(sep='\t')
                label = whole_line[-1].replace('\n', '')
                label = int(label)
                tweet = whole_line[1]
                tweet = final_tweet_cleanup(tweet)
                if(label not in interesting_labels.wanted_list or tweet==""):
                    continue
                for classes in get_classes(label):
                    cleaned_data_file.write(tweet + '\t' + str(classes) + "\n")
