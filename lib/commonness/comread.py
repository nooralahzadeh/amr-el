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

def query(commonness_table, query, n=0):
    results = list()
    if query in commonness_table:
        total = 0
        for title in commonness_table[query]:
            total += commonness_table[query][title]
        count = 0
        for title in sorted(commonness_table[query],
                            key=commonness_table[query].get, reverse=True):
            score = float(commonness_table[query][title] / total)
            results.append((title, score))
            count += 1
            if count == n:
                break
    return results

# def subset():
#     f = open('./output/commonness_table.pickle', 'rb')
#     commonness_table = pickle.load(f)
#     subset = dict()
#     for line in open('./output/amr_mentions', 'r'):
#         query = line.strip().lower()
#         if query in commonness_table:
#             print query
#             subset[query] = dict()
#             subset[query] = commonness_table[query]
#     pickle.dump(subset, open('./output/commonness_table_subset.pickle', 'wb'))
