"""
For D-Link DIR_300NRUB5.
"""

import os, os.path
from os.path import join, expanduser
import json
from base64 import b64decode

import requests


ADDRESS = 'http://192.168.1.1'
CREDENTIALS_FILE = expanduser(r'~\.creds-router')


def get_credentials(creds_filename=CREDENTIALS_FILE):
    if os.path.isfile(creds_filename):
        with open(creds_filename) as f:
            for line in f:
                try:
                    pair = b64decode(line).decode('utf-8').split(':', 1)
                    if len(pair) == 2:
                        return tuple(pair)
                except:
                    continue











def main():
    address = ADDRESS + '/index.cgi'
    username, password = get_credentials()
    with requests.Session() as session:
        # Login
        cookies = dict(cookie_lang='rus', client_login=username, client_password=password)
        login_data=dict(v2='y', rs_type='html', auth='auth',
            A1=username, A2=password)
        login_req = requests.Request('POST', address, data=login_data, cookies=cookies)
        login_resp = session.send(request=session.prepare_request(login_req))
        print(f'{login_resp=}')
        print(f'{login_resp.text[:512]}\n  --- // ---\n')
        
        # Status
        status_resp_text = session.post(address, data=dict(
            v2='y', rq='y', res_json='true', res_config_action=1, res_config_id=104, res_struct_size=1)).text
        status_resp_residents = json.loads('{\n' + '\n'.join(x for x in status_resp_text.splitlines() if x.startswith(' ')) + '}')
        print(f'{status_resp_residents=}')

        # Logout
        logout_resp = requests.get(address, cookies=dict(cookie_lang='rus'))
        print(f'\n{logout_resp=}')
        print(f'logout_resp_text=\n{logout_resp.text}')












if __name__ == '__main__':
    main()
