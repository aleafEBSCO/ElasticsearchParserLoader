from elasticsearch import Elasticsearch

es = Elasticsearch()

doc = {
    'author': 'andrew',
    'text': 'some text'
}

res = es.index(index="temp", doc_type="doc", id=1, body=doc)
print(res)