import json
import urllib2

'''
 Return a set of DBpedia types using SPARQL
 Parameters: title - DBpedia title
             raw   - Raw DBpedia property
'''
def get_dbpedia_type(title, raw=False):
    query = 'http%3A%2F%2Fdbpedia.org%2Fresource%2F' + title
    url = 'http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.o' \
    'rg&query=select+distinct+%3Ftype+where+%7B%3C' + query + '%3E+rdf%3Atype' \
    '+%3Ftype.%7D&format=application%2Fsparql-results%2Bjson&timeout=30000&de' \
    'bug=on'
    request = urllib2.Request(url)
    json_ = urllib2.urlopen(request).read()

    dbtypes = set()
    results = json.loads(json_)
    for i in results['results']['bindings']:
        value = i['type']['value'].encode("utf-8")
        if raw != True:
            value = value[value.rfind('/')+1:].rstrip("0123456789")
        dbtypes.add(value)

    return dbtypes

'''
 Return a set of selected DBpedia properties using SPARQL
 Parameters: title - DBpedia title
             label - Selected DBpedia property label
'''
def get_dbpedia_property(title, label='rdf:type'):
    query = 'http%3A%2F%2Fdbpedia.org%2Fresource%2F' + title
    url = 'http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.o' \
          'rg&query=select+distinct+%3Fproperty+where+%7B%3C' + query + '%3E+' \
          + label + '+%3Fproperty.%7D&format=application%2Fsparql-results%2Bj' \
          'son&timeout=30000&debug=on'
    request = urllib2.Request(url)
    json_ = urllib2.urlopen(request).read()

    properties = set()
    results = json.loads(json_)
    for i in results['results']['bindings']:
        value = i['property']['value'].encode("utf-8")
        properties.add(value)

    return properties

'''
 Return a set of all DBpedia properties using SPARQL
'''
def get_dbpedia_all(title):
    query = 'http%3A%2F%2Fdbpedia.org%2Fresource%2F' + title
    url = 'http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.o' \
          'rg&query=select+distinct+*+where+%7B%3C' + query + '%3E+%3Flabel+%' \
          '3Fproperty.%7D&format=application%2Fsparql-results%2Bjson&timeout=' \
          '30000&debug=on'

    request = urllib2.Request(url)
    json_ = urllib2.urlopen(request).read()

    properties = set()
    results = json.loads(json_)
    for i in results['results']['bindings']:
        label = i['label']['value'].encode("utf-8")
        property_ = i['property']['value'].encode("utf-8")
        properties.add((label, property_)) # (label, property_) tuple

    return properties

if __name__ == '__main__':
    # print get_dbpedia_type('China')
    # print get_dbpedia_property('China', 'rdf:type')
    print get_dbpedia_all('China')
