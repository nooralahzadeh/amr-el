'Linkipedia system'
import json
import urllib
import urllib2
import re

def find_json(query):
    url = 'http://blender02.cs.rpi.edu:3301/linking?query=%s'
    url = url % urllib.quote_plus(query)
    request = urllib2.Request(url)
    result = urllib2.urlopen(request).read()
    return result

def find_candidates(json_input):
    candidates = list()
    result = json.loads(json_input)
    for i in result['results']:
        for j in i['annotations']:
            if j['url'] != 'NIL':
                candidate = re.search("/(.+)>", j['url']).group(1)
                candidate = candidate[candidate.rfind('/')+1:]
                candidates.append(candidate.encode("utf-8"))
            else:
                candidates.append('-')
    return candidates

def linking(query):
    candidates = find_candidates(find_json(query))
    return candidates
