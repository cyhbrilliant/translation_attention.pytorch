import cv2
import numpy as np
import torch
from matplotlib import animation
from torch.autograd import Variable
import torch.nn.functional as F
import h5py
import os
import matplotlib.pyplot as mp

class Gru(torch.nn.Module):
    def __init__(self):
        super(Gru, self).__init__()
        self.gru = torch.nn.GRU(input_size=1, hidden_size=60, num_layers=1)
        self.Lo = torch.nn.Linear(60,1)

    def forward(self, x):
        x, Hidden_state = self.gru(x, self.Hidden_state)
        outs = []
        for i in range(x.size(0)):
            outs.append(self.Lo(x[i, :, :]))
        return torch.stack(outs, dim=0)

    def initHidden(self):
        self.Hidden_state = Variable(torch.zeros(1, 1, 60))

# Hidden = Variable(torch.zeros(1, 1, 60))
gru = Gru()
Loss_fn = torch.nn.MSELoss()
Optimizer = torch.optim.Adam(gru.parameters(),lr=0.001)
for iter in range(1000):
    start, end = iter * np.pi, (iter + 4) * np.pi  # time steps
    # sin 预测 cos
    steps = np.linspace(start, end, 600, dtype=np.float32)
    x_np = np.sin(steps)  # float32 for converting torch FloatTensor
    y_np = np.cos(steps)
    # print(x_np, y_np)
    gru.initHidden()
    out = gru(Variable(torch.from_numpy(x_np[:, np.newaxis, np.newaxis])))
    # print(out.data.numpy().shape)

    loss = Loss_fn(out, Variable(torch.from_numpy(y_np[:, np.newaxis, np.newaxis])))
    print(iter, loss.data.numpy())
    gru.zero_grad()
    loss.backward()
    Optimizer.step()
    if (iter + 1) % 100 == 0:
        mp.plot(steps, out.data.numpy()[:, 0, 0], steps, y_np)
        mp.show()







