#/usr/bin/env python
from pagerduty import Pagerduty
from flask import Flask
import twilio.twiml

import settings

app = Flask(__name__)

@app.route('/twilio', methods=['GET', 'POST'])
def twilio_resp():
    pduty = Pagerduty(settings.PAGERDUTY_API_URL, settings.PAGERDUTY_API_KEY)
    oncall = pduty.find_oncall(settings.PAGERDUTY_SCHEDULE_ID)['entries'][0]['user']
    oncall_contact = pduty.find_user_contact(oncall['id'])['contact_method']

    phone = '+%s%s' % (oncall_contact['country_code'], 
                       oncall_contact['phone_number'])
    resp = twilio.twiml.Response()
    resp.dial(phone)
    return str(resp)

if __name__ == '__main__':
    app.debug = settings.DEBUG
    app.run(host='0.0.0.0')
    
