from minsearch import Index

# Simple test to understand the API
index = Index(['content', 'filename'])

docs = [
    {'content': 'hello world', 'filename': 'test1.md'},
    {'content': 'demo example', 'filename': 'test2.md'},
]

index.fit(docs)
results = index.search('demo', num_results=5)
print(results)

