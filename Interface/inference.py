import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
import numpy as np

int_to_emotion = {0:'Happy', 1:'Sad' , 2:'Angry', 3:'Surprised', 4:'Disgusted', 5:'Afraid'}

def pad_features(tweets_ints, seq_length):
    ''' Return features of review_ints, where each review is padded with 0's 
        or truncated to the input seq_length.
    '''
    
    # getting the correct rows x cols shape
    features = np.zeros((len(tweets_ints), seq_length), dtype=int)

    # for each review, I grab that review and 
    for i, row in enumerate(tweets_ints):
        features[i, -len(row):] = np.array(row)[:seq_length]
    
    return features

def inference_tweet_cleanup(tweet):
    tweet = tweet.replace(".", " . ") \
                 .replace(",", " , ") \
                 .replace(";", " ; ") \
                 .replace("?", " ? ") \
                 .replace("\'", "") \
                 .replace("\"", "")\
                 .replace("!", " ! ")\
                 .replace("#", " # ")

    return tweet.lower()

def tweet_to_glove_index(tweet, glove_dict):
    tweets_ints = []
    tweet = inference_tweet_cleanup(tweet)
    idxs = [glove_dict.stoi[w]        # lookup the index of word
            for w in tweet.split()
            if w in glove_dict.stoi] # keep words that has an embedding
    tweets_ints.append(idxs)
    return tweets_ints


def predict(model, test_tweet, glove, sequence_length, use_gpu):
    # tokenize tweet
    test_ints = tweet_to_glove_index(test_tweet, glove)
    
    # pad tokenized sequence
    seq_length=sequence_length
    features = pad_features(test_ints, seq_length)
    
    # convert to tensor to pass into your model
    if use_gpu:
      feature_tensor = torch.from_numpy(features).cuda()
    else:
      feature_tensor = torch.from_numpy(features)
    
    batch_size = feature_tensor.size(0)
    
    
    # get the output from the model
    output = model(feature_tensor)
    
    # convert output probabilities to predicted class (0 or 1)
    output_prob = nn.functional.softmax(output,dim=1)
    top_n_pred = output_prob.topk(3,dim=1) ## top 3 preds
    top_n_pred_prob, top_n_pred_index = top_n_pred[0].detach().cpu().numpy()[0], top_n_pred[1].detach().cpu().numpy()[0]
    print(test_tweet)
    print('Prediction:')
    predictions = []
    for prob,index in zip(top_n_pred_prob,top_n_pred_index):
    #   print(int_to_emotion[index] , 'with' , str(int(prob*100))+"%", 'confidence')
      pred = int_to_emotion[index] + ' with ' + str(int(prob*100))+"%" + ' confidence '
      print(pred)
      predictions.append(pred)



    return 'Prediction:', predictions[0], predictions[1], predictions[2]