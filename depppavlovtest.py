'''
from deeppavlov import configs, train_model

para_model = train_model('paraphraser_rubert', download=True)


print(para_model)
'''
import torch
from transformers import AutoModelForSequenceClassification, BertTokenizer
model_name = 'cointegrated/rubert-base-cased-dp-paraphrase-detection'
model = AutoModelForSequenceClassification.from_pretrained(model_name).cuda()
tokenizer = BertTokenizer.from_pretrained(model_name)

def compare_texts(text1, text2):
    batch = tokenizer(text1, text2, return_tensors='pt').to(model.device)
    with torch.inference_mode():
        proba = torch.softmax(model(**batch).logits, -1).cpu().numpy()
    return proba[0] # p(non-paraphrase), p(paraphrase)


print(compare_texts('Алиса, что делает карта глубоководные','как работает карта глубоководные'))

print(compare_texts('Алиса, что делает карта с названием желуждь','как работает карта глубоководные'))




print(compare_texts('Отличная погодка сегодня выдалась','как работает карта глубоководные'))


