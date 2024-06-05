import torch.nn as nn
import torch 
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
from utils import get_model_path

activate_functions = [nn.LeakyReLU(), nn.LeakyReLU()]

class MultiObjectiveModel(nn.Module):
    def __init__(self, n_dim, n_obj, args, hidden_size):
        super(MultiObjectiveModel, self).__init__()
        self.n_dim = n_dim
        self.n_obj = n_obj
        self.args = args
        self.env_name = args.env_name 
        self.save_path = get_model_path(args=args, model_type='multi', name=f'{args.train_model_seed}')

        layers = []
        layers.append(nn.Linear(n_dim, hidden_size[0]))
        for i in range(len(hidden_size)-1):
            layers.append(nn.Linear(hidden_size[i], hidden_size[i+1]))
        layers.append(nn.Linear(hidden_size[len(hidden_size)-1], n_obj))

        self.layers = nn.Sequential(*layers)
        self.hidden_size = hidden_size
    
    def forward(self, x):

        x = x.to(torch.float32)
        for i in range(len(self.hidden_size)):
            x = self.layers[i](x)
            x = activate_functions[i](x)
        
        x = self.layers[len(self.hidden_size)](x)
        out = x

        return out.to(torch.float32)
    

            
        
    
