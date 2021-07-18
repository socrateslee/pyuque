'''
Toolkit for extracting content from yuque docs.
'''
from ..util import markdown


def get_code_block(fullpath=None, index=0, client=None):
    if not (fullpath and client):
        return ''
    splitted = fullpath.split('/')
    namespace = '/'.join(splitted[:-1])
    slug = splitted[-1]
    d = client.doc.get(namespace, slug)
    if d and d['data']:
        block_list = markdown.parse_code_block(d['data'].get('body') or '')
        if block_list and index < len(block_list):
            return block_list[index]['code']
    return ''
