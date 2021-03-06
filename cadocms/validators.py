from __future__ import unicode_literals

import smtplib

from django.utils.translation import ugettext_lazy as _
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.conf import settings

import dns.resolver

#http://www.djangotips.com/real-email-validation

class EmailValidator(EmailValidator):

    def __call__(self, value):
        super(EmailValidator, self).__call__(value)
        if (settings.HOST.CLASS == 'DEV'):
            return
        
        try:
            hostname = value.split('@')[-1]
        except KeyError:
            raise ValidationError(_('Enter a valid email address.'))

        try:
            for server in [ str(r.exchange).rstrip('.') \
                            for r \
                            in dns.resolver.query(hostname, 'MX') ]:
                try:
                    smtp = smtplib.SMTP()
                    smtp.connect(server)
                    status = smtp.helo()
                    if status[0] != 250:
                        continue
                    #smtp.mail('')
                    #status = smtp.rcpt(value)
                    #if status[0] != 250:
                    #    raise ValidationError(_('Invalid email address.'))
                    break
                except smtplib.SMTPServerDisconnected:
                    break
                except smtplib.SMTPConnectError:
                    continue
        except dns.resolver.NXDOMAIN:
            raise ValidationError(_('Nonexistent domain.'))
        except dns.resolver.NoAnswer:
            raise ValidationError(_('Nonexistent email address.'))
        except smtplib.SMTPException: # Didn't make an instance.
            raise ValidationError(_('SMTP Error'))
        except smtplib.socket.error:
            pass
            #raise ValidationError(_('Cant connect to server'))


validate_email = EmailValidator(
    _('Enter a valid email address.'),
    'invalid'
)