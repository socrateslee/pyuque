#-*- coding: utf-8 -*-
'''
The command line client for pyuque.
'''
import os
import argparse
import configparser
from .config import get_access_token_from_config,\
                    get_credentials_from_config
from .oauth import gen_code, authorize, get_access_token
from .client import Yuque


def parse_args(parser):
    parser.add_argument("--client_id", default="",
                        help="The OAuth application client id.")
    parser.add_argument("--access_token", default="",
                        help="The access token.")
    parser.add_argument("--profile", default="",
                        help="The name of the config profile.")
    parser.add_argument("--scope", default="",
                        help="The authorization scope.")
    parser.add_argument("--redirect_uri", default="",
                        help="The redirect_uri for oauth web process.")
    parser.add_argument("options", default=[], nargs="*")
    return parser.parse_args()


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


def main():
    parser = argparse.ArgumentParser()
    args = vars(parse_args(parser))
    options = args['options']
    if options and options[0] == 'oauth-web':
        client_id, client_secret = get_credentials_from_config(args)
        oauth_process_web(args['client_id'], args['client_secret'], args['scope'], args['redirect_uri'])
    elif options and options[0] == 'oauth-nonweb':
        client_id, client_secret = get_credentials_from_config(args)
        oauth_process_nonweb(args['client_id'], args['client_secret'], args['scope'])
    elif options and options[0] == 'test':
        access_token = get_access_token_from_config(args)
        print(access_token)
    elif options and options[0] == 'get-code':
        access_token = get_access_token_from_config(args)
        client = Yuque(token=access_token)
        from .toolkit import extract
        index = int(options[2])\
                if len(options) > 2 and options[2].isdigit()\
                else 0
        print(extract.get_code_block(fullpath=options[1],
                                     index=index,
                                     client=client))
    elif options and options[0] == 'get-table':
        access_token = get_access_token_from_config(args)
        client = Yuque(token=access_token)
        from .toolkit import extract
        index = int(options[2])\
                if len(options) > 2 and options[2].isdigit()\
                else 0
        print(extract.get_table(fullpath=options[1],
                                index=index,
                                client=client))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
