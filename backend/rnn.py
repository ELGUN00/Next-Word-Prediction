import torch
import torch.nn as nn
import torch.nn.functional as F


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class RNN(nn.Module):
    
    def __init__(self, vocab_size, output_size, embedding_dim, hidden_dim, n_layers, dropout=0.5):
        super(RNN, self).__init__()
      
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, dropout=dropout, batch_first=True)
        
        
        self.vocab_size = vocab_size
        self.output_size = output_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        
     
        self.fc = nn.Linear(hidden_dim, output_size)
    
    
    def forward(self, x, hidden):
        batch_size = x.size(0)
        x=x.long()
        
        embeds = self.embedding(x)
        lstm_out, hidden = self.lstm(embeds, hidden)
        
        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)
        
        out = self.fc(lstm_out)
        
        out = out.view(batch_size, -1, self.output_size)
        
        out = out[:, -1]

        return out, hidden
    
    
    def init_hidden(self, batch_size):
        weights = next(self.parameters()).data
        if(device=='cuda:0'):
            hidden = (weights.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda(), 
                     weights.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
            hidden = (weights.new(self.n_layers, batch_size, self.hidden_dim).zero_(),
                     weights.new(self.n_layers, batch_size, self.hidden_dim).zero_())
        
        return hidden