from __future__ import division
import pickle

def read(path_pickle):
    f = open(path_pickle, 'rb')
    commonness_table = pickle.load(f)
    return commonness_table

def search(commonness_table):
    while True:
        query = raw_input('query: ')
        n = int(raw_input('n: '))
        if query in commonness_table:
            total = 0
            for title in commonness_table[query]:
                total += commonness_table[query][title]
            count = 0
            for title in sorted(commonness_table[query],
                                key=commonness_table[query].get, reverse=True):
                print title, commonness_table[query][title], \
                    float(commonness_table[query][title] / total)
                count += 1
                if count == n:
                    print '-----------------------'
                    print '\n\n'
                    break
        else:
            print 'null'

def query(commonness_table, query, n=0, score=True):
    results = list()
    if query in commonness_table:
        total = 0
        for title in commonness_table[query]:
            total += commonness_table[query][title]
        count = 0
        for title in sorted(commonness_table[query],
                            key=commonness_table[query].get, reverse=True):
            commonness_score = float(commonness_table[query][title] / total)
            title = title.replace(' ', '_')
            if score:
                results.append((title, score))
            else:
                results.append(title)
            count += 1
            if count == n:
                break
    return results
