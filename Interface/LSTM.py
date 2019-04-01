import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
import numpy as np

class TweetLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, glove, use_gpu):
        super(TweetLSTM, self).__init__()
        self.use_gpu = use_gpu
        self.emb = nn.Embedding.from_pretrained(glove.vectors)
        self.hidden_size = hidden_size
        self.rnn = nn.LSTM(input_size, hidden_size, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(2 * hidden_size, num_classes) # 2 * hidden_size because LSTM is bidrectional 
    def forward(self, x):
        # Look up the embedding
        x = self.emb(x)
        # Set an initial hidden state and cell state
        
        if self.use_gpu:
          h0 = torch.zeros(2, x.size(0), self.hidden_size).cuda()
          c0 = torch.zeros(2, x.size(0), self.hidden_size).cuda()
        else:
          h0 = torch.zeros(2, x.size(0), self.hidden_size)
          c0 = torch.zeros(2, x.size(0), self.hidden_size)
        # Forward propagate the LSTM
        out, _ = self.rnn(x, (h0, c0))
        # Pass the output of the last time step to the classifier
        out = self.fc(out[:, -1, :])
        return out