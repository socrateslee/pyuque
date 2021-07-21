'''
Utilities for operating names of yuque docs
'''

def split_fullpath(fullpath):
    fullpath = fullpath.strip('/')
    splitted = fullpath.split('/')
    namespace = '/'.join(splitted[:-1])
    slug = splitted[-1]
    return (namespace, slug)
