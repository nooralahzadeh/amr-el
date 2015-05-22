from __future__ import division
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
 Probability based named entity typing
'''
def typing(db2amr, dbtype_freq, dbtypes, n=5):
    skip = ['owl#Thing', 'Object', 'Abstraction', 'Whole',
            'Wikidata:Q', 'Q', '_Feature']

    results = dict()
    for dbtype in dbtypes:
        if dbtype in db2amr and dbtype not in skip:
            for amrtype in db2amr[dbtype]:
                amrcount = db2amr[dbtype][amrtype]
                if amrtype not in results:
                    results[amrtype] = 0
                idf = dbtype_freq['#TOTAL#'] / dbtype_freq[dbtype]
                results[amrtype] += amrcount * idf

    typing = list()
    for i in sorted(results, key=results.get, reverse=True)[:n+1]:
        if i == '#TOTAL#':
            continue
        typing.append((i, results[i] / results['#TOTAL#']))

    return typing
