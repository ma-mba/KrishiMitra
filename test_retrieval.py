from services.retrieval import search
res = search('What fertilizer is used for rice?', 'rice', top_k=3)
print(res)
