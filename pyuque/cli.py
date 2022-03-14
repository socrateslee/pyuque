#-*- coding: utf-8 -*-
'''
The command line client for pyuque.
'''
import os
import sys
import importlib
import argparse
import configparser
from .config import get_access_token_from_config,\
                    get_credentials_from_config
from .oauth import gen_code, authorize, get_access_token
from .client import Yuque

TOOLKIT_MAP = {
    'get-code': {
        'module': 'extract',
        'help': 'Get the code block from an article.'
    },
    'get-table': {
        'module': 'extract',
        'help': 'Get the table from an article.'
    },
    'sync-dir':  {
        'module': 'sync_dir',
        'help': 'Sync a local directory to a remote yuque repo.'
    },
}


def load_toolkit_module(action):
    if action in TOOLKIT_MAP:
        info = TOOLKIT_MAP[action]
        module_name = 'pyuque.toolkit.%s' % info['module']
        importlib.import_module(module_name)
        return sys.modules[module_name]
    return None


def parse_args(parser):
    parser.add_argument("--client_id", default="",
                        help="The OAuth application client id.")
    parser.add_argument("--client_secret", default="",
                        help="The OAuth application client secret.")
    parser.add_argument("--access_token", default="",
                        help="The access token.")
    parser.add_argument("--profile", default="",
                        help="The name of the config profile.")
    parser.add_argument("--scope", default="",
                        help="The authorization scope.")
    parser.add_argument("--redirect_uri", default="",
                        help="The redirect_uri for oauth web process.")
    parser.add_argument("command", default='', nargs="?")
    return parser.parse_known_args()


def oauth_process_web(client_id, client_secret, scope, redirect_uri):
    url = authorize(client_id,
                    scope=scope,
                    state="pyuque",
                    redirect_uri=redirect_uri,
                    mode="web")
    print("Please copy and access the url in your browser:\n%s\n" % url)
    code = input("Please input the code in your redirected url:")
    ret = get_access_token(client_id, code,
                           client_secret=client_secret,
                           grant_type='authorization_code')
    print(ret)
    return ret


def oauth_process_nonweb(client_id, client_secret, scope):
    code = gen_code()
    url = authorize(client_id,
                    scope=scope,
                    code=code,
                    client_secret=client_secret)
    print("Please copy and access the url in your browser:\n%s\n" % url)
    input("Press ENTER after you authorized to continue...")
    ret = get_access_token(client_id, code, grant_type='client_code')
    print(ret)
    return ret


def main():
    parser = argparse.ArgumentParser(add_help=False)
    args, rest = parse_args(parser)
    args = vars(args)
    command = args['command']
    token_info = None
    action = ''
    if command == 'oauth-web':
        client_id, client_secret = get_credentials_from_config(args)
        token_info = oauth_process_web(client_id, client_secret, args['scope'], args['redirect_uri'])
    elif command == 'oauth-nonweb':
        client_id, client_secret = get_credentials_from_config(args)
        token_info = oauth_process_nonweb(client_id, client_secret, args['scope'])
    elif command in TOOLKIT_MAP:
        action = command
    if not action and rest and rest[0] in TOOLKIT_MAP:
        action = rest[0]
        rest = rest[1:]

    # tooklit actions
    if action:
        module_action = load_toolkit_module(action)
        access_token = token_info.get('access_token')\
                if token_info and token_info.get('access_token')\
                else get_access_token_from_config(args)
        client = Yuque(token=access_token)
        module_action.handle_cli(action, rest, client=client)
    elif '-h' in rest or '--help' in rest:
        parser.print_help()


if __name__ == '__main__':
    main()
