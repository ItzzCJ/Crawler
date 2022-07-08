# sentence_transformer: Python module using Sentence BERT 
# check documentation in source link for further details
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import pytorch_cos_sim # cosine silarity


model = SentenceTransformer('stsb-roberta-large')
sentences = list(['Worst Customer Support', 'dont like customer service', 'It lags a lot', 'facing lag issue']) 
embeddings = model.encode(sentences)




print(pytorch_cos_sim(embeddings[0], embeddings[1]).item())
# print(pytorch_cos_sim(embeddings[0], embeddings[2]))
# print(pytorch_cos_sim(embeddings[0], embeddings[3]))

# print(pytorch_cos_sim(embeddings[1], embeddings[2]))
# print(pytorch_cos_sim(embeddings[1], embeddings[3]))

# print(pytorch_cos_sim(embeddings[2], embeddings[3]))