import bs4


def parse_tables(body_html, value_field='text'):
    '''
    Parse table structures into list of list from body_html.
    '''
    doc = bs4.BeautifulSoup(body_html)
    table_list = []
    for table_elem in doc.findAll('table'):
        table = []
        for tr_elem in table_elem.findAll('tr'):
            tr = []
            for td_elem in tr_elem.findAll('td'):
                value = getattr(td_elem, value_field, '')
                tr.append(value)
            table.append(tr)
        table_list.append(table)
    return table_list


def table_to_dict(table, cols):
    ret = []
    for row in table:
        ret.append({k: v for k, v in zip(cols, row)})
    return ret
