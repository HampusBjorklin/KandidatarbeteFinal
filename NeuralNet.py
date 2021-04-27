import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import matplotlib.pyplot as plt

# use GPU for computations if possible
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        # Weights
        self.W = Net.parameters(3,800)
        # offset
        self.b = Net.parameters(800)


    def forward(self, X):
        # Linear transformation
        Z = X.mm(self.W) + self.b
        # Apply softmax
        G = F.softmax(Z,dim=1)
        return G


def cross_entropy(G,Y):
    Y_onehot = torch.eye(800, device=device)[Y]
    return -(Y_onehot * G.log()).sum(dim=1).mean()


def accuracy(G,Y):
    return (G.argmax(dim=1) == Y).float().mean()
