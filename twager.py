#/usr/bin/env python
from pagerduty import Pagerduty
from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route('/twilio', methods=['GET', 'POST'])
def twilio_resp():
    pduty = Pagerduty('https://mrfriday.pagerduty.com/api/v1',
                      '9FzxEwftrpRz3bSwyNa3')
    oncall = pduty.find_oncall('PUIIRST')['entries'][0]['user']
    oncall_contact = pduty.find_user_contact(oncall['id'])['contact_method']

    phone = '+%s %s' % (oncall_contact['country_code'],
                       ''.join(map(lambda x: '%s ' % x, oncall_contact['phone_number'])))
    resp = twilio.twiml.Response()
    resp.say('On call is %s, number %s' % (oncall['name'], phone))
    return str(resp)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    
