# encoding:utf-8
from __future__ import unicode_literals

from django_expa import expaApi
from django_hatchbuck import hatchbuckApi

def load_expa_interaction(interaction):
    """
    Loads new EPs who have interacted yesterday with EXPA in a certain way. So far, only registered and contacted EPs are supported
    Params:
        interaction: The interaction kind. Only registered and contacted are supported.
    """
    ex_api = expaApi.ExpaApi()
    htb_api = hatchbuckApi.HatchbuckApi()
    eps = ex_api.get_past_interactions(interaction, 1, 1551, False)
    for ep in eps['eps']:
        try:
            location = ep['location'].split(', ')
        except AttributeError:
            print 'EP location: ' + str(ep['location'])
        city = 'None'
        country = 'None'
        state = 'None'
        try:
            city, country = location
        except ValueError:
            if len(location) == 3:
                city, state, country = location
                print "Agregado departamento"
            else:
                print ep['location']
                print location

        data = {
            'phones': [{
                'type':'Home',
                'number':ep['phone'],
                }],
            'firstName':ep['first_name'],
            'lastName':ep['last_name'],
            'addresses': [{
                'city':city,
                'country':country,
                'type':'Home',
                'state':state,
                'zip':'NA',
                'street':'NA',
                }],
        }
        print htb_api.add_interaction(ep['email'], interaction, data).json()
    print 'Added %d new contacts' % eps['total']
