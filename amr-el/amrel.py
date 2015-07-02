from __future__ import division
import sys
import re
import urllib
from src import Mention
from src import linkipedia
sys.path.append('../lib/amr-reader-master/amr-reader/src')
import amr
import output

def linking(amr_table):
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            named_entities = sen.named_entities_
            for i in named_entities:
                ne = named_entities[i]
                mention = Mention.Mention(ne) # NamedEntity -> Mention
                query = mention.name().lower()

                ### Entity type
                if ne.maintype_ == 'PER':
                    query = '%s(person)' % query
                if ne.maintype_ == 'ORG':
                    query = '%s(organization)' % query
                if ne.maintype_ == 'GPE':
                    query = '%s(place)' % query

                ### Coherent set
                for i in ne.coherence_:
                    query += ';%s' % i[2].entity_name_.lower()

                candidates = linkipedia.linking(query)
                gold = urllib.unquote(ne.wiki_)
                ne.wiki_ = candidates[0] # Top 1

def main(amr_input, filename, output_path):
    amr_table = amr.get_amr_table_str(amr_input)
    linking(amr_table)
    output.html(amr_table, filename, output_path)
