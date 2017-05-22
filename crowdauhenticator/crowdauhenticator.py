import requests
import urllib.parse
import re
from jupyterhub.auth import Authenticator

from tornado import gen
from traitlets import Unicode, Int, Bool, Union, List


class CROWDAuthenticator(Authenticator):
    server_url = Unicode(
        config=True,
        help='URL of CROWD server to contact'
    )

    crowd_username = Unicode(
        config=True,
        help='Application name to contact CROWD server'
    )

    crowd_password = Unicode(
        config=True,
        help='Application password to contact CROWD server'
    )

    allowed_groups = List(
        config=True,
        help="List of CROWD Group whose members are allowed access"
    )

    valid_username_regex = Unicode(
        r'^.+$',
        config=True,
        help="""Regex to use to validate usernames before sending to CROWD

        Also acts as a security measure to prevent LDAP injection. If you
        are customizing this, be careful to ensure that attempts to do LDAP
        injection are rejected by your customization
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        username = data['username']
        password = data['password']

        # Protect against invalid usernames
        if not re.match(self.valid_username_regex, username):
            self.log.warn('Invalid username')
            return None

        # No empty passwords!
        if password is None or password.strip() == '':
            self.log.warn('Empty password')
            return None

        # call crowd endpoint
        query = urllib.parse.urlencode({'username': username})
        url = urllib.parse.urljoin(self.server_url, 'rest/usermanagement/latest/authentication?' + query)
        headers = {'Content-Type': 'application/xml',
                   'Accept': 'application/json',
                   'Referrer': self.server_url}
        data = '<password><value>%s</value></password>' % password
        resp = requests.post(url, data, headers=headers, auth=(self.crowd_username, self.crowd_password))

        if resp.status_code == 200:
            return username
        else:
            self.log.warn(resp.text)
            return None
