import csv
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
import numpy as np
import matplotlib.pyplot as plt
import interesting_labels
import pandas


def get_data():
    header = ['status_id', 'tweet', 'label']
    data_set = pandas.read_csv('processed.txt', delimiter='\t', names=header)
    return data_set


def get_data_set():
    return global_data_set


if __name__ == '__main__':
    data_set = get_data()
    num_classes = {'Happy': 0, 'Sad': 0, 'Angry': 0, 'Surprised': 0, 'Disgusted': 0, 'Afraid': 0}
    for label in data_set['label']:
        if(label in interesting_labels.Happy):
            num_classes['Happy'] += 1
        elif(label in interesting_labels.Sad):
            num_classes['Sad'] += 1
        elif (label in interesting_labels.Angry):
            num_classes['Angry'] += 1
        elif (label in interesting_labels.Surprised):
            num_classes['Surprised'] += 1
        elif (label in interesting_labels.Disgusted):
            num_classes['Disgusted'] += 1
        elif (label in interesting_labels.Afraid):
            num_classes['Afraid'] += 1

    print(num_classes)