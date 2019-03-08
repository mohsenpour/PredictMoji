import tweepy
import creds
import emoji
import interesting_labels

def remove_word_starting_with(character,text):
    '''
    removes all the words that starts with character from the text and returns it
    '''
    text = " ".join(filter(lambda word: word[0] != character, text.split()))
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
    return (tweet_text.find('https') == -1)


def cleanup(tweet_text):
    '''cleans the tweet text by removing new lines
     emojis and mentions(any word starting with @) '''
    tweet_text = tweet_text.replace('\n', ' ').replace(',',' ')
    tweet_text = remove_word_starting_with('@',tweet_text)
    tweet_text = remove_emoji(tweet_text)
    return tweet_text

def tweeter_api(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
# authentication to connect to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

if __name__ == '__main__':
    api = tweeter_api(creds.CONSUMER_KEY,
                      creds.CONSUMER_SECRET,
                      creds.ACCESS_TOKEN,
                      creds.ACCESS_TOKEN_SECRET)
    # open the training data file
    with open('full_train_plaintext.txt','r') as training_file:
        with open('processed.txt', 'a') as tweet_text_file:
            i=0
            for line in training_file:
                if i>1000:
                    exit(0)
                try:
                    # get the status id from the file
                    status_id = line.split()[0]
                    # get the emoji labels from the file
                    labels = (line.split()[1]).split(',')

                    # get the tweet using twitte api
                    tweet = api.get_status(status_id)

                    # clean up the tweet
                    tweet_text = cleanup(tweet.text)
                    if is_useful(tweet_text):
                        for label in labels:
                            print('id: ', status_id, ' text: ', tweet_text, ' labels: ', labels)
                            tweet_text_file.write(status_id +','+ tweet_text +','+ label + "\n")
                            i+=1
                except BaseException as e:
                    print(e)
