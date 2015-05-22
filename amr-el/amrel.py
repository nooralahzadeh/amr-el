from __future__ import division
import sys
import re
import urllib
from src import commonness
from src import dbpedia
from src import dbtype
from src import Mention
sys.path.append('../lib/amr-reader-master/amr-reader/src')
import amr

'''
 README

 - This simple EL system only has commonness ranking now.

'''

def linking():
    acc = dict()
    acc[1] = 0
    acc[5] = 0
    acc[10] = 0
    total = 0
    results = dict() # key: query, value: candidates
                     # store results into memory

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            named_entities = sen.named_entities_
            for i in named_entities:
                ne = named_entities[i]
                mention = Mention.Mention(ne) # NamedEntity -> Mention

                ### PER ORG GPE only
                if mention.maintype_ not in ['PER', 'ORG', 'GPE']:
                    continue

                total += 1
                query = mention.name().lower()
                if query not in results:
                    results[query] = list()
                    results[query] = commonness.query(commonness_table, query,
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
                        err.write('%s\t%s\t%s\t%s\n\n' % (senid, query,
                                                          gold, candidates))
    for k in sorted(acc):
        print '%d: %.2f' % (k, acc[k] / total * 100)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'USAGE: python amrel.py <path of config file> ' \
            '<directory of AMR files>'
        sys.exit()
    else:
        err = open('el_error', 'w')
        config = open(sys.argv[1]).readlines()
        path_commonness_pickle = re.search('\<.+\>: (.+)',
                                           config[0].strip()).group(1)
        path_db2amr_pickle = re.search('\<.+\>: (.+)',
                                       config[1].strip()).group(1)
        print 'loading...'
        commonness_table = commonness.read(path_commonness_pickle)
        # db2amr = dbtype.read(path_db2amr_pickle)
        print 'done.'

        '''
         AMR Named Entity query setting:

         coref     - Adding name coreference
         coherence - Adding coherent set
         hor       - Adding have-org-rol-91
         hrr       - Adding have-rel-rol-91
         time      - Adding global time
         loc       - Adding global location
         sr        - Adding semantic role
         chain     - Adding coreferential chain

       '''
        amr_table = amr.get_amr_table(sys.argv[2])
        # amr_table = amr.get_amr_table(sys.argv[2], coref=True, coherence=True,
        #                           hor=True, hrr=True, time=True, loc=True,
        #                           sr=True, chain=True)
        linking()
