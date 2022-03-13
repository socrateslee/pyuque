'''
Toolkit for extracting content from yuque docs.
'''
import argparse
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


def handle_cli(action, cli_args, **kwargs):
    parser = argparse.ArgumentParser(prog=action)
    parser.add_argument('fullpath')
    parser.add_argument('index', default=0, type=int)
    args = vars(parser.parse_args(cli_args))
    if action == 'get-code':
        print(get_code_block(args['fullpath'], index=args['index'], client=kwargs['client']))
    elif action == 'get-table':
        print(get_table(args['fullpath'], index=args['index'], client=kwargs['client']))
    else:
        parser.print_help()
