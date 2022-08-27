'''
Utilities for operating names of yuque docs
'''
import re

YUQUE_SPACE_PATTERN = 'https://%s.yuque.com'


def split_fullpath(fullpath):
    fullpath = fullpath.strip('/')
    splitted = fullpath.split('/')
    namespace = '/'.join(splitted[:-1])
    slug = splitted[-1]
    return (namespace, slug)


def get_space_domain(name_or_url):
    if re.match(r'^[0-9a-zA-Z-_~]+$', name_or_url):
        return YUQUE_SPACE_PATTERN % name_or_url
    elif re.match(r'^[0-9a-zA-Z-_~]+\.yuque\.com/?$', name_or_url):
        return ('https://%s' % name_or_url).rstrip('/')
    elif re.match(r'^https://[0-9a-zA-Z-_~]+\.yuque\.com/?$', name_or_url):
        return  name_or_url.rstrip('/')
    else:
        raise Exception("Incorrect yuque space name or url: %s" % name_or_url)
