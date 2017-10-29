"""
Description:
    tbd
"""


import sys
import abc
import json
import requests
import argparse


class ContactFormatter(object):
    """
    """
   
    @classmethod
    def rainloop(cls, contacts):
        new_contacts = []
        for ct in contacts:
            name = '{0} {1}'.format(ct.get('firstname', ''), 
                                    ct.get('lastname', ''))
            new_ct = [ct['email'], name.strip()]
            new_contacts.append(new_ct)

        return new_contacts


class BaseContactHandler(object):
    """
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, domain=''):
        """Initialization."""
        self._domain = domain or 'example.com'

    @abc.abstractmethod
    def get_users():
        pass
    
    @abc.abstractmethod
    def get_aliases():
        pass


class LdapContactHandler(BaseContactHandler):
    """
    """

    def __init__(self, token='', **base_kwargs):
        """Initialization."""
        super(LdapContactHandler, self).__init__(**base_kwargs)

        self._headers = {'x-api-key': token}
        self._base_url = 'https://console.jumpcloud.com'

    def _query(self, dir_path):
        """
        """
        url = '{0}{1}'.format(self._base_url, dir_path)
        data_holder = requests.get(url, headers=self._headers)
        if data_holder.status_code != 200:
            return None

        try:
            text = json.loads(data_holder.text)
        except ValueError:
            text = None

        return text

    def get_users(self):
        data = self._query('/api/systemusers')
        if data is None:
            return []
        
        user_data = []
        for elmt in data['results']:
            if not elmt['email'].endswith(self._domain):
                continue
            if not elmt['activated'] or elmt['ldap_binding_user']:
                continue
            user_data.append(elmt)

        return user_data

    def get_aliases(self):
        data = self._query('/api/v2/usergroups')
        if data is None:
            return []

        alias_data = []
        for elmt in data:
            alias_data.append(
                {'email': '{0}@{1}'.format(elmt['name'], self._domain)}
            )
      
        return alias_data   


def get_ldap_contacts(token, domain):
    """
    """
    handler = LdapContactHandler(token=token, domain=domain)
    
    contacts = []
    contacts.extend(handler.get_users())
    contacts.extend(handler.get_aliases())

    return contacts


def make_rainloop_contacts(contacts):
    """
    """
    return ContactFormatter.rainloop(contacts)


def get_argument_parser():
    """
    """
    argp = argparse.ArgumentParser()
    argp.add_argument(
        '-src', '--source', choices=['ldap'],  # TODO, choices should be queried from config data.
        help='' 
    )
    argp.add_argument(
        '-fmt', '--format', choices=['rainloop'],  # TODO, choices should be queried from config data.
        help=''
    )
    argp.add_argument(
        '-pt', '--pretty', action='store_true',
        help=''
    )
    argp.add_argument(
        '-tk', '--token', default='',
        help=''
    )
    argp.add_argument(
        '-dm', '--domain', default='',
        help=''
    )

    return argp


def main():
    """CLI entry point."""
    # TODO, should be queried from config data.
    source_mapping = {
        'ldap': get_ldap_contacts
    }
    format_mapping = {
        'rainloop': make_rainloop_contacts
    }

    argp = get_argument_parser()
    if not sys.argv[1:]:
        argp.print_help()
        return 0

    args = argp.parse_args()
    get_contacts = source_mapping[args.source]
    make_contacts = format_mapping[args.format]

    args_ = []
    kwargs = {}
    if args.source == 'ldap':
        args_ = [args.ldap_token, args.domain]
    contacts = make_contacts(get_contacts(*args_, **kwargs))
    
    kwargs = {'indent': 4} if args.pretty else {}
    print json.dumps(contacts, **kwargs)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
