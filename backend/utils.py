from .rnn import LSTM

import torch
from torchtext.data import get_tokenizer

import string

torch.manual_seed(0)

class Utils:
    def __init__(self) -> None:

        self.vocab_obj = torch.load('./model/vocab_obj.pth')
        self.device = torch.device('cpu')
        self.tokenizer = get_tokenizer("basic_english")
        # Model parameters
        vocab_size = len(self.vocab_obj)
        embedding_dim = 128            
        hidden_dim = 128               
        num_layers = 3             
        dropout_rate = 0.15          
        tie_weights = True                  
        lr = 1e-3

        

        self.model = LSTM(vocab_size, embedding_dim, hidden_dim, num_layers, dropout_rate, tie_weights).to(self.device)
        self.model.load_state_dict(torch.load('./model/model.pth'))
        self.model.eval()


    def clean_text(self,txt):
        txt = "".join(t for t in txt if t not in string.punctuation).lower()
        txt = txt.encode("utf8").decode("ascii",'ignore')
        return txt
    
    def predict_next_word(self, str_original):
        str = self.tokenizer(self.clean_text(str_original))
        print(str)
        hidden = self.model.init_hidden(1, self.device)
        with torch.no_grad():  
            hidden = self.model.detach_hidden(hidden)
            src = torch.tensor([self.vocab_obj(str)]).to(torch.int32).to(self.device)
            prediction, hidden = self.model(src, hidden) 
            prediction  = prediction[:,-1,:]
            res = self.vocab_obj.lookup_tokens([torch.argmax(prediction,dim=1).item()])[0]            
            print(f'{str_original} --> {res}')
            return res

