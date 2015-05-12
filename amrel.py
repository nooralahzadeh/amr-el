from __future__ import division
import sys
import re
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
    results = dict() # key: query, value:candidates
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            named_entities = sen.named_entities_
            for i in named_entities:
                ne = named_entities[i]
                query = ne.name().lower()
                if query not in results:
                    results[query] = list()
                    results[query] = comread.query(commonness_table, query, 5)
                candidates = results[query]
                print '%s\t%s\t%s\n' % (senid, ne.name(), candidates)

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
        linking(amr_table)
