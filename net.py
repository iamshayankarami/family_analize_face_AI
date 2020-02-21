import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import sqlite3
import matplotlib.pyplot as plt

use_cuda = False
pretrained_model = "/data/family1/george1.jpg"


class net(nn.Module):
    def __init__(self):
       super(net, self).__init__()
       self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
       self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
       self.conv2_drop = nn.Dropout2d()
       self.fc1 = nn.Linear(320, 50)
       self.fc2 = nn.Linear(50, 10)
    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


device = torch.device("cuda" if (use_cuda and torch.cuda.is_available()) else "cpu")
print(device)
model = net().to(device)
#model.load_state_dict(torch.load(pretrained_model, map_location='cpu'))
model.eval()

