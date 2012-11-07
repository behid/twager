#!/usr/bin/env python
from datetime import date

import requests

API_URL = 'https://mrfriday.pagerduty.com/api/v1'
API_KEY = '9FzxEwftrpRz3bSwyNa3'

class Pagerduty(object):
    def __init__(self, API_URL, API_KEY):
        self.API_URL = API_URL
        headers = {'Authorization': 'Token token=%s' % API_KEY}
        self.session = requests.session(headers=headers)

    def find_oncall(self, schedule_id):
        params = {'since': date.today().isoformat(),
                  'until': date.today().isoformat()
                  }
        return self.session.get('%s/schedules/%s/entries' % (self.API_URL, schedule_id),
                           params=params).json

    def find_user_contact(self, user_id):
        data = self.session.get('%s/users/%s/notification_rules' % (self.API_URL, user_id)).json
        data = filter(lambda x: x['contact_method']['type'] == 'phone',
                data['notification_rules'])
        data = reduce(lambda x, y: x if x['start_delay_in_minutes'] < y['start_delay_in_minutes'] else y,
                data)
        return data
    

