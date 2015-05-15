'''
 Mention object
'''

class Mention(object):
    '''
     Constructor - Default
    '''
    def __init__(self, docid='', senid='', mention='',
                 subtype='', maintype='', wiki=''):
        self.docid_ = docid             # Doc id
        self.senid_ = senid             # Sentence id
        self.beg_ = 0                   # Offset begin
        self.end_ = 0                   # Offset end
        self.mention_ = mention         # Mention
        self.subtype_ = subtype         # Sub-type
        self.maintype_ = maintype       # PER, ORG, GPE
        self.coreference_ = ''          # Coreference name
        self.neighbors_ = set()         # Neighbors
        self.coherence_ = set()         # Coherent named entities
        self.wiki_ = wiki               # Wikipedia title

    '''
     Constructor - AMR NamedEntity object
    '''
    def __init__(self, ne):
        self.docid_ = ne.senid_[:ne.senid_.rfind('.')] # Doc id
        self.senid_ = ne.senid_                        # Sentence id
        self.beg_ = 0                                  # Offset begin
        self.end_ = 0                                  # Offset end
        self.mention_ = ne.entity_name_                # Mention
        self.subtype_ = ne.subtype_                    # Sub-type
        self.maintype_ = ne.maintype_                  # PER, ORG, GPE
        self.coreference_ = ne.coreference_            # Coreference name
        self.neighbors_ = ne.neighbors_                # Neighbors
        self.coherence_ = ne.coherence_                # Coherent named entities
        self.wiki_ = ne.wiki_                          # Wikipedia title

    def name(self):
        if self.coreference_ != '':
            return self.coreference_
        else:
            return self.mention_
