#-*- coding: utf-8 -*-
'''
The command line client for pyuque.
'''
import argparse
from .oauth import gen_code, authorize, get_access_token

def parse_args(parser):
    parser.add_argument("--client_id", default="",
                        help="The OAuth application client id.")
    parser.add_argument("--client_secret", default="",
                        help="The OAuth application client secret.")
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
        oauth_process_web(args['client_id'], args['client_secret'], args['scope'], args['redirect_uri'])
    elif options and options[0] == 'oauth-nonweb':
        oauth_process_nonweb(args['client_id'], args['client_secret'], args['scope'])
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
