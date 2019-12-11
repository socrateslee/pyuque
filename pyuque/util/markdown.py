'''
Utilities for generating markdown documents.
'''


def get_markdown_table(data, cols=None):
    generate_line = lambda l: '| %s |' % (' | '.join(l))
    ret = []
    if not data:
        return ''
    if cols is None:
        cols = [''] * len(data[0])
    ret.append(generate_line(cols))
    ret.append(generate_line(['---'] * len(data[0])))
    for line in data:
        if isinstance(line, dict):
            line = [line.get(k, '') for k in cols]
        ret.append(generate_line(line))
    return '\n'.join(ret)
