import tweepy
import creds
if __name__ == '__main__':
    # authentication to connect to Twitter API
    auth = tweepy.OAuthHandler(creds.CONSUMER_KEY,creds.CONSUMER_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN,creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    # open the training data file
    with open('full_train_plaintext.txt','r') as training_file:
        with open('tweet_text_file.txt', 'a') as tweet_text_file:
            i =0
            for line in training_file:
                if i > 5:
                    exit(0)
                try:
                    status_id = line.split()[0]
                    labels = (line.split()[1]).split(',')
                    tweet = api.get_status(status_id)
                    tweet_text = tweet.text.replace('\n',' ')
                    print('id: ',status_id,' text: ',tweet_text,' labels: ',labels)
                    for label in labels:
                        tweet_text_file.write(status_id +','+ tweet_text +','+ label + "\n")
                    i+=1
                except BaseException as e:
                    print(e)