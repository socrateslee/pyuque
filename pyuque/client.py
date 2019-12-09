import requests

DEFAULT_API_BASE = "https://www.yuque.com/api/v2"


def _filter_none(d):
    return {k: v for k, v in d.items() if v is not None}


class MethodGetter(object):
    def __init__(self, inst, prefix):
        self.inst = inst
        self.prefix = prefix

    def __getattr__(self, name):
        return getattr(self.inst, '%s_%s' % (self.prefix, name))

    def __dir__(self):
        return [i[len(self.prefix) + 1:]\
                for i in dir(self.inst) if i.startswith("%s_" % self.prefix)]


class Yuque(object):
    def __init__(self, token, api_base=None):
        self.token = token
        self.api_base = api_base or DEFAULT_API_BASE
        self.user = MethodGetter(self, 'user')
        self.group = MethodGetter(self, 'group')
        self.repo = MethodGetter(self, 'repo')
        self.doc = MethodGetter(self, 'doc')
        self.search = MethodGetter(self, 'search')

    def send_request(self, method, path, headers=None, params=None, json=None, **kwargs):
        if headers is None:
            headers = {}
        if method in ['PUT', 'POST']:
            headers['Content-Type'] = 'application/json'
        if not headers.get('User-Agent'):
            headers['User-Agent'] = 'pyuque'
        headers['X-Auth-Token'] = self.token
        resp = requests.request(method, self.api_base + path,
                                headers=headers,
                                params=params,
                                json=json,
                                **kwargs)
        return resp.json()

    def user_get(self, login_or_id=None):
        if login_or_id:
            return self.send_request('GET', '/users/%s' % login_or_id)
        else:
            return self.send_request('GET', '/user')

    def user_list_groups(self, login_or_id):
        return self.send_request('GET', '/users/%s/groups' % login_or_id)

    def user_list_repos(self, login_or_id):
        return self.send_request('GET', '/users/%s/repos' % login_or_id)

    def user_create_repo(self, login_or_id, name, slug=None, description=None, public=0, type="Book"):
        params = {
            "name": name,
            "slug": slug,
            "description": description,
            "public": public,
            "type": type
        }
        params = _filter_none(params)
        return self.send_request('POST', "/users/%s/repos" % login_or_id, json=params)

    def group_list(self):
        return self.send_request('GET', '/groups')

    def group_create(self, name, login=None, description=None):
        params = {
            "name": name,
            "login": login,
            "description":  description
        }
        params = _filter_none(params)
        return self.send_request('POST', '/groups', json=params)

    def group_get(self, login_or_id):
        return self.send_request('GET', '/groups/%s' % login_or_id)

    def group_update(self, login_or_id, name=None, login=None, description=None):
        params = {
            "name": name,
            "login": login,
            "description":  description
        }
        params = _filter_none(params)
        return self.send_request('PUT', '/groups/%s' % login_or_id, json=params)

    def group_delete(self, login_or_id):
        return self.send_request('DELETE', '/groups/%s' % login_or_id)

    def group_users_list(self, login_or_id):
        return self.send_request('GET', '/groups/%s/users' % login_or_id)

    def group_users_add(self, group_login_or_id, user_login, role=1):
        return self.send_request('PUT',
                                 '/groups/%s/users/%s' % (group_login_or_id, user_login),
                                 params={'role': role})

    def group_users_delete(self, group_login_or_id, user_login):
        return self.send_request('DELETE',
                                 '/groups/%s/users/%s' % (group_login_or_id, user_login))

    def group_list_repos(self, login_or_id):
        return self.send_request('GET', '/groups/%s/repos' % login_or_id)

    def group_create_repo(self, login_or_id, name=None, slug=None, description=None, public=0, type="Book"):
        params = {
            "name": name,
            "slug": slug,
            "description": description,
            "public": public,
            "type": type
        }
        params = _filter_none(params)
        return self.send_request('POST', "/groups/%s/repos" % login_or_id, json=params)

    def repo_get(self, namespace_or_id):
        return self.send_request('GET', '/repos/%s' % namespace_or_id.strip('/'))

    def repo_update(self, namespace_or_id, name=None, slug=None, toc=None, description=None, public=None):
        params = {
            "name": name,
            "slug": slug,
            "toc": toc,
            "description": description,
            "public": public
        }
        params = _filter_none(params)
        return self.send_request('PUT', '/repos/%s' % namespace_or_id.strip('/'), json=params)

    def repo_delete(self, namespace_or_id):
        return self.send_request('DELETE', '/repos/%s' % namespace_or_id.strip('/'))

    def repo_toc(self, namespace_or_id):
        return self.send_request('GET', '/repos/%s/toc' % namespace_or_id.strip('/'))

    def repo_list_docs(self, namespace_or_id):
        return self.send_request('GET', '/repos/%s/docs' % namespace_or_id.strip('/'))

    def doc_get(self, namespace_or_id, slug_or_id, raw=1):
        return self.send_request('GET',
                                 '/repos/%s/docs/%s' % (namespace_or_id, slug_or_id),
                                 params={"raw": raw})

    def doc_create(self, namespace_or_id, title, slug=None, public=0, format='markdown', body=None):
        params = {
            "title": title,
            "slug": slug,
            "public": public,
            "format": format,
            "body": body
        }
        params = _filter_none(params)
        return self.send_request('POST',
                                 '/repos/%s/docs' % namespace_or_id.strip('/'),
                                 json=params)

    def doc_update(self, namespace_or_id, doc_id, title=None, slug=None, public=None, body=None):
        params = {
            "title": title,
            "slug": slug,
            "public": public,
            "body": body
        }
        params = _filter_none(params)
        return self.send_request('PUT',
                                 '/repos/%s/docs/%s' % (namespace_or_id.strip('/'), doc_id),
                                 json=params)

    def doc_delete(self, namespace_or_id, doc_id):
        return self.send_request('DELETE', '/repos/%s/docs/%s' % (namespace_or_id.strip('/'), doc_id))

    def search_repos(self, q, type=""):
        params = {"q": q, "type": type}
        return self.send_request('GET', '/search/repos', params=params)
