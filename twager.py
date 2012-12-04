#/usr/bin/env python
from pagerduty import Pagerduty
from flask import Flask
import twilio.twiml
from twilio.rest import TwilioRestClient

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

@app.route('/oncall-notif', methods=['GET'])
def oncall_notification():
    twilio = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)
    pduty = Pagerduty(settings.PAGERDUTY_API_URL, settings.PAGERDUTY_API_KEY)
    oncall = pduty.find_oncall(settings.PAGERDUTY_SCHEDULE_ID)['entries'][0]['user']

    new_oncall = True

    with open(settings.TMPFILE, 'r+') as f:
        try:
            if f.read() == oncall['id']:
                new_oncall = False
            else:
                f.seek(0)
                f.write(oncall['id'])
                f.truncate()
        except IOError:
            new_oncall = False
            f.write(oncall['id'])

    if new_oncall:
        oncall_contact = pduty.find_user_contact(oncall['id'])['contact_method']
        message = 'Hello %s, you are now OnCall.' % oncall['name']
        phone = '+%s%s' % (oncall_contact['country_code'],
                           oncall_contact['phone_number'])
        twilio.sms.messages.create(to=phone, 
                                   from_=settings.TWILIO_NUMBER,
                                   body=message)
        return "new oncall, sent sms"
    else:
        return "same oncall"

if __name__ == '__main__':
    app.debug = settings.DEBUG
    app.run(host='0.0.0.0')
    
