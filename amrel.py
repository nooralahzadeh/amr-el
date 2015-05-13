from __future__ import division
import sys
import re
import urllib
sys.path.append('./lib/')
from commonness import comread
sys.path.append('./lib/amr-reader-master/amr/')
from main import get_amr_table

'''
 README

 - This simple EL system only has commonness ranking now.
 - Loading whole commonness table will take 10 mins, so I use a subset that
   only contains mentions in AMR corpus
'''

def linking(amr_table):
    acc = dict()
    acc[1] = 0
    acc[5] = 0
    acc[10] = 0
    total = 0
    results = dict() # key: query, value: candidates

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            named_entities = sen.named_entities_
            for i in named_entities:
                ne = named_entities[i]

                ### PER ORG GPE only
                if ne.maintype_ not in ['PER', 'ORG', 'GPE']:
                    continue

                total += 1
                query = ne.name().lower()
                if query not in results:
                    results[query] = list()
                    results[query] = comread.query(commonness_table, query,
                                                   n=10, score=False)
                candidates = results[query]
                gold = urllib.unquote(ne.wiki_)

                ### NULL
                if len(candidates) == 0 and gold == 'NULL':
                    for k in [1, 5, 10]:
                        acc[k] += 1
                    continue

                ### non NULL
                for k in [1, 5, 10]:
                    kcandidates = candidates[0:k]
                    if gold in kcandidates:
                        acc[k] += 1
                    elif k == 10:
                        err.write('%s\t%s\t%s\t%s\n\n' % (senid, ne.name(),
                                                          gold, candidates))
    for k in sorted(acc):
        print '%d: %.2f' % (k, acc[k] / total * 100)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'USAGE: python amr_el.py <path of config file> ' \
            '<directory of AMR files>'
        sys.exit()
    else:
        config = open(sys.argv[1]).readlines()
        commonness_pickle_path = re.search('\<path of commonness table\>: (.+)',
                                           config[0].strip()).group(1)
        commonness_table = comread.read(commonness_pickle_path)
        amr_table = get_amr_table(sys.argv[2])
        err = open('error', 'w')
        linking(amr_table)
