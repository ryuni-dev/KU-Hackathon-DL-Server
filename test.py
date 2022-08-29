import torch
import numpy as np
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
import gluonnlp as nlp
from dataset.dataset import BERTDataset


def predict(predict_sentence, model):
    device = 'cpu'

    batch_size = 64
    max_len = 64
    _, vocab = get_pytorch_kobert_model()
    tokenizer = get_tokenizer()
    tok=nlp.data.BERTSPTokenizer(tokenizer, vocab, lower = False)

    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
    
    model.eval()

    for _, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length= valid_length
        label = label.long().to(device)

        out = model(token_ids, valid_length, segment_ids)


        test_eval=[]
        for i in out:
            logits=i
            logits = logits.detach().cpu().numpy()

            #FEAR, SURPRISE, ANGER, SADNESS, NEUTRAL, HAPPINESS, DISGUST
            if np.argmax(logits) == 0:
                test_eval.append("FEAR")
            elif np.argmax(logits) == 1:
                test_eval.append("SURPRISE")
            elif np.argmax(logits) == 2:
                test_eval.append("ANGER")
            elif np.argmax(logits) == 3:
                test_eval.append("SADNESS")
            elif np.argmax(logits) == 4:
                test_eval.append("NEUTRAL")
            elif np.argmax(logits) == 5:
                test_eval.append("HAPPINESS")
            elif np.argmax(logits) == 6:
                test_eval.append("DISGUST")

    return test_eval[0]