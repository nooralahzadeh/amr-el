from __future__ import division
import json
import pickle
import urllib2

'''
 Read pickle
'''
def read(path_pickle):
    f = open(path_pickle, 'rb')
    table = pickle.load(f)
    return table

'''
 Return a set of DBpedia types using SPARQL
'''
def query(query):
    url = 'http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.o' \
    'rg&query=select+distinct+%3Ftype+where+%7B%3Chttp%3A%2F%2Fdbpedia.org%2F' \
    'resource%2F'+ query + '%3E+rdf%3Atype+%3Ftype.%7D&format=application%2Fs' \
    'parql-results%2Bjson&timeout=30000&debug=on'
    request = urllib2.Request(url)
    json_ = urllib2.urlopen(request).read()

    dbtypes = set()
    results = json.loads(json_)
    for i in results['results']['bindings']:
        value = i['type']['value'].encode("utf-8")
        value = value[value.rfind('/')+1:].rstrip("0123456789")
        dbtypes.add(value)

    return dbtypes

'''
 Probability based named entity typing
'''
def typing(db2amr, dbtypes, n=10):
    skip = ['owl#Thing', 'Object', 'Abstraction', 'Whole',
            'Wikidata:Q', 'Q', '_Feature', 'YagoLegalActorGeo',
            'PhysicalEntity', 'YagoPermanentlyLocatedEntity', 'Place',
            'd0.owl#Location', 'YagoGeoEntity', 'PopulatedPlace',
            'Location', 'Region', 'YagoLegalActor', 'DUL.owl#Agent',
            'Agent']

    results = dict()
    for dbtype in dbtypes:
        if dbtype in db2amr and dbtype not in skip:
            for amrtype in db2amr[dbtype]:
                amrcount = db2amr[dbtype][amrtype]
                if amrtype not in results:
                    results[amrtype] = 0
                results[amrtype] += amrcount

    typing = list()
    for i in sorted(results, key=results.get, reverse=True)[:n+1]:
        if i == '#TOTAL#':
            continue
        typing.append((i, results[i] / results['#TOTAL#']))

    return typing

if __name__ == '__main__':
    print query('China')
