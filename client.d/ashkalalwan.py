'''
    ashkalalwan.py - pandora_client plugin

    custom parse_path for pandora_client to parse musereen archive paths in the form

    /SRC/Year/Project/Item Title/Author/Type/MVI_123.AVI


'''
import re
import ox

def example_path(client):
    return '\t' + '/SRC/Year/Project/Item Title/Author/Type/MVI_123.AVI'

def parse_path(client, path):
    '''
        args:
            client - Client instance
            path   - path without volume prefix 
        return:
            return None if file is ignored, dict with parsed item information otherwise
    '''
    m = re.compile('^(?P<src>.+?)/(?P<year>\d{4}(-\d{4})?|NA)/(?P<project>.+?)/(?P<workname>.+?)/(?P<by>.+?)/(?P<type>.+?)/[^/]*').match(path)
    if not m:
        return None
    info = m.groupdict()
    date = '%s' % (info['year'])
    for key in info:
        if info[key]:
            info[key] = info[key].replace('_', ' ')

    source= "%s"% (info['src'])
    by = "%s" % (info['by'])
    by = by.replace(u"\u061b",";").split(";")
    i = 0
    for key in by:
        flname = key.replace(u"\u060c",",").split(",")
        if len(flname) > 1:
            key = "%s %s" % (flname[1],flname[0])
        key = re.sub(" {2,}"," ",key)
        key = re.sub("^ ","",key)
        by[i] = key
        i = i + 1

    title = "%s (%s) by %s" % (info['workname'],
        info['type']," & ".join(by))
    r = {
        'source': source,
        'by': by,
        'project': info['project'],
        'date': date,
        'taxons': [info['type']],
        'title': title,
    }
    _info = ox.movie.parse_path(path)
    for key in ('extension', 'type'):
        r[key] = _info[key]
    return r


