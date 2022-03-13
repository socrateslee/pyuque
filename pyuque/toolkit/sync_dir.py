import os
import os.path
import argparse
import markdown
import bs4


MARKDOWN_EXTENSIONS = [
    '.md',
    '.mkd',
    '.mdown',
    '.mdwn',
    '.mdtxt',
    '.mkdn',
    '.mdtext'
    '.markdown'
]


def is_temp_file(file):
    if file.startswith('.#'):
        return True
    return False

def parse_markdown_info(markdown_content):
    html = markdown.markdown(markdown_content)
    soup = bs4.BeautifulSoup(html)
    ret = {
        'title': soup.h1.get_text() if soup.h1 else None
    }
    return ret


def sync_dir(client, path, repo):
    repo_info = client.repo.get(repo)
    public = repo_info['data']['public']
    files = os.listdir(path)
    for file in files:
        basename, extname = os.path.splitext(file)
        if extname not in MARKDOWN_EXTENSIONS:
            continue
        if is_temp_file(extname):
            continue
        filename = "%s/%s" % (path.rstrip('/'), file)
        content = open(filename).read()
        markdown_info = parse_markdown_info(content)
        slug = basename
        title = markdown_info.get('title') or basename
        doc = client.doc.get(repo, slug)
        print(slug, title)
        if doc.get('data') and doc['data'].get("id"):
            client.doc.delete(repo, doc['data']["id"])
            #print(client.doc.update(repo, doc['data']["id"],
            #                  title=title,
            #                  slug=slug,
            #                  public=public,
            #                  body=content,
            #                  _force_asl=1))

        client.doc.create(repo, title,
                          slug=slug,
                          public=public,
                          body=content)
    if os.path.exists("%s/.toc" % path.rstrip('/')):
        toc = open("%s/.toc" % path.rstrip('/')).read()
        client.repo.update(repo, toc=toc)


def handle_cli(action, cli_args, **kwargs):
    parser = argparse.ArgumentParser(prog=action)
    parser.add_argument('path')
    parser.add_argument('repo')
    args = vars(parser.parse_args(cli_args))
    if action == 'sync-dir':
        return sync_dir(kwargs['client'], args['path'], args['repo'])
    else:
        parser.print_help()
