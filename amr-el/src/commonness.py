from __future__ import division
import pickle

'''
 Read pickle
'''
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

'''
 Return commonness ranking results
  n:     # of candidates
  score: whether return commonness score
'''
def query(commonness_table, query, n=0, score=True):
    results = list()
    if query in commonness_table:
        total = 0
        for title in commonness_table[query]:
            total += commonness_table[query][title]

        for title in sorted(commonness_table[query],
                            key=commonness_table[query].get, reverse=True)[:n]:
            commonness_score = float(commonness_table[query][title] / total)
            title = title.replace(' ', '_')
            if score:
                results.append((title, commonness_score))
            else:
                results.append(title)

    return results
