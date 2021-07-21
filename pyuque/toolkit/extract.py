'''
Toolkit for extracting content from yuque docs.
'''
from ..util import markdown, html, names


def get_code_block(fullpath=None, index=0, client=None):
    if not (fullpath and client):
        return ''
    namespace, slug = names.split_fullpath(fullpath)
    doc = client.doc.get(namespace, slug)
    if doc and doc['data']:
        block_list = markdown.parse_code_block(doc['data'].get('body') or '')
        if block_list and index < len(block_list):
            return block_list[index]['code']
    return ''


def get_table(fullpath=None, index=0, client=None):
    if not (fullpath and client):
        return ''
    namespace, slug = names.split_fullpath(fullpath)
    doc = client.doc.get(namespace, slug)
    if doc and doc['data']:
        table_list = html.parse_tables(doc['data'].get('body_html') or '')
        if table_list and index < len(table_list):
            return html.table_to_csv(table_list[index])
    return ''
