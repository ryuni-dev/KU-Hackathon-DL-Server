from typing import Union
from fastapi import FastAPI

import torch
from kobert.pytorch_kobert import get_pytorch_kobert_model

from model.model import BERTClassifier
from test import predict

app = FastAPI()

device = torch.device("cpu")
bertmodel, _ = get_pytorch_kobert_model()

model = BERTClassifier(bertmodel, dr_rate = 0.5).to(device)
model.load_state_dict(torch.load('checkpoint.pth'))

@app.get("/sentiment")
def predict_sentiment(text: str):
    res = predict(text, model)
    return res