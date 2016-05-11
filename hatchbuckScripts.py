# encoding:utf-8
from __future__ import unicode_literals

from django_expa import expaApi
from django_hatchbuck import hatchbuckApi, settings

def load_expa_interaction(interaction):
    """
    Loads new EPs who have interacted yesterday with EXPA in a certain way. So far, only registered and contacted EPs are supported
    Params:
        interaction: The interaction kind. Only registered and contacted are supported.
    """
    inter_dict = {
        'registered':'person',
        'contacted':'person',
        'applied':'application',
        'accepted':'application',
        'an_signed':'application',
        'approved':'application',
        'realized':'application',
        }
    interaction_type = inter_dict[interaction]
    ex_api = expaApi.ExpaApi()
    htb_api = hatchbuckApi.HatchbuckApi()
    items = ex_api.get_past_interactions(interaction, 1, 1551, False)
    for ep in items['items']:
        if interaction_type == 'application':
            subtype = ep['opportunity']['programmes'][0]['short_name']
            ep = ep['person']
        city = 'None'
        country = 'None'
        state = 'None'
        ep_phone = 'None'
        if interaction_type == 'person':
            ep_phone = ep['phone']
            subtype = None
            try:
                location = ep['location'].split(', ')
            except AttributeError:
                print 'EP location: ' + str(ep['location'])
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
                'number':ep_phone,
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
            'customFields':[{
                'id':settings.CUSTOM_FIELD_TAGS['EXPA_ID'],
                'value':ep['id'],
            },{
                'id':settings.CUSTOM_FIELD_TAGS['LC'],
                'value':ep['home_lc']['name'],
            }],
        }
        print htb_api.add_interaction(ep['email'], interaction, data, subtype).json()
    print 'Added %d new contacts' % items['total']
