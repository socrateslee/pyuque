'''
Utilities for generating markdown documents.
'''
import re


def get_markdown_table(data, cols=None, to_str=None):
    if to_str is None:
        to_str = str
    generate_line = lambda l: '| %s |' % (' | '.join(l))
    ret = []
    if not data:
        return ''
    if cols is None:
        cols = [''] * len(data[0])
    ret.append(generate_line(map(to_str, cols)))
    ret.append(generate_line(['---'] * len(data[0])))
    for line in data:
        if isinstance(line, dict):
            line = [line.get(k, '') for k in cols]
        ret.append(generate_line(map(to_str, line)))
    return '\n'.join(ret)


code_pattern = re.compile(r'```(.*?)\n(.*?)\n```', re.S)

def parse_code_block(body_markdown):
    '''
    Parse code block from markdown.
    '''
    code_block_list = []
    for language, code in code_pattern.findall(body_markdown):
        code_block_list.append({
            "language": language,
            "code": code
        })
    return code_block_list
