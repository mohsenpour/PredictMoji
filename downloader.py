import tweepy
import creds2
import emoji
import interesting_labels
import time

def remove_word_starting_with(character,text):
    '''
    removes all the words that starts with character from the text and returns it
    '''
    text = " ".join(filter(lambda word: word[0] != character, text.split()))
    return text

def remove_word(unwanted_word, text):
    '''
    removes all the occurances of the word in the text
    '''
    text = " ".join(filter(lambda word: word != unwanted_word, text.split()))
    return text

def remove_emoji(text):
    '''
    removes all the emojis from the text
    '''
    text = emoji.demojize(text)
    text = " ".join(filter(lambda word: (word[0] != ':' and word[-1] != ":"), text.split()))
    return text


def is_useful(tweet_text):
    '''tweet is only useful for training if it is long enough and does not contain a url address'''
    '''according to https://arxiv.org/pdf/1708.00524.pdf ,tweets containing urls 
    are noisy for emoji prediction'''
    return (tweet_text.find('https') == -1 and tweet_text.find('http') == -1)


def cleanup(tweet_text):
    '''cleans the tweet text by removing new lines
     emojis and mentions(any word starting with @) '''
    tweet_text = tweet_text.replace('\n', ' ')
    tweet_text = remove_word_starting_with('@',tweet_text)
    tweet_text = remove_emoji(tweet_text)
    tweet_text = remove_word('RT', tweet_text)
    return tweet_text

def tweeter_api(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
# authentication to connect to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def restore_index():
    index_file = open("index.txt", "r")
    index = int(index_file.read())
    index_file.close()
    return index

def save_index(index):
    index_file = open("index.txt", "w")
    index_file.write(str(index))
    index_file.close()

MAX_LINES_EACH_TIME = 10
if __name__ == '__main__':
    api = tweeter_api(creds2.CONSUMER_KEY,
                      creds2.CONSUMER_SECRET,
                      creds2.ACCESS_TOKEN,
                      creds2.ACCESS_TOKEN_SECRET)
    index = restore_index()


    # open the training data file
    with open('full_train_plaintext.txt','r') as training_file:
        with open('processed.txt', 'a') as tweet_text_file:
            i = 0
            for line_index,line in enumerate(training_file):
                if i >= MAX_LINES_EACH_TIME:
                    save_index(index)
                    exit()
                if line_index >= index:
                    try:
                        time.sleep(1)
                        # get the status id from the file
                        status_id = line.split()[0]
                        # get the emoji labels from the file
                        labels = (line.split()[1]).split(',')
                        # get the tweet using twitte api
                        tweet = api.get_status(status_id)
                        print('i: ', i)
                        i += 1
                        index += 1

                        # clean up the tweet
                        tweet_text = cleanup(tweet.text)
                        if is_useful(tweet_text):
                            for label in labels:
                                if(int(label) in interesting_labels.wanted_list):
                                    print('id: ', status_id, ' text: ', tweet_text, ' labels: ', labels)
                                    tweet_text_file.write(status_id +'\t'+ tweet_text +'\t'+ label + "\n")
                    except BaseException as e:
                        print(e)
                        print('i: ', i)
                        i+=1
                        index+=1
            save_index(index)
