#-*- coding: utf-8 -*-
'''
Modules for loading configs.
'''
import os
import configparser

CONFIG_LOCATIONS = [
    './pyuque.cfg',
    '~/.config/pyuque.cfg',
    '/etc/pyuque.cfg'
]

def format_location(location):
    if location\
            and location.startswith('~')\
            and os.environ.get('HOME'):
        return location.replace('~', os.environ['HOME'])
    else:
        return location


def _get_config(file_name='', profile_name=None):
    if not profile_name:
        profile_name = 'default'
    locations = [file_name, *CONFIG_LOCATIONS]
    for location in map(format_location, locations):
        if location and os.path.exists(location):
            cp = configparser.ConfigParser()
            cp.read_file(open(location))
            if profile_name in cp.sections():
                data = dict(cp.items(profile_name))
                return data
            break
    return {}


class GetConfig(object):
    def __init__(self):
        self._config = None

    def __call__(self, file_name='', profile_name=''):
        if self._config is None:
            self._config = _get_config(file_name=file_name,
                                       profile_name=profile_name)
        return self._config

get_config = GetConfig()


def get_credentials_from_config(args):
    client_id = ''
    client_secret = ''
    if args.get('client_id') in args.get('client_secret'):
        client_id = args['client_id']
        client_secret = args['client_secret']
    else:
        profile_name = args.get('profile') or None
        data = get_config(profile_name=profile_name)
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
    return (client_id, client_secret)


def get_access_token_from_config(args):
    access_token = ''
    if args.get('access_token'):
        access_token = args['access_token']
    else:
        profile_name = args.get('profile') or None
        data = get_config(profile_name=profile_name)
        access_token = data.get('access_token')
    return access_token
