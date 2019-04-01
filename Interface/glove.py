import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
import numpy as np

class Glove():
    def __init__(self):
        self.emb = torchtext.vocab.GloVe(name="twitter.27B",dim=50)
        self.emb.vectors[0] = torch.tensor(np.zeros(50))

    def get_glove_emb(self):
        return self.emb