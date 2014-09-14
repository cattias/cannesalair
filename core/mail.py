from django.core.mail import EmailMessage

class SpiffyEmailMessage(EmailMessage):
    def __init__(self, subject, body, from_email, to, cc, in_reply_to):
        EmailMessage.__init__(self, subject, body, from_email, to)
        self.cc = cc or []
        self.in_reply_to = in_reply_to
        self.message_id = None

    def message(self):
        msg = super(SpiffyEmailMessage, self).message()

        if self.cc:
            msg['Cc'] = ','.join(self.cc)

        if self.in_reply_to:
            msg['In-Reply-To'] = self.in_reply_to
            msg['References'] = self.in_reply_to

        self.message_id = msg['Message-ID']

        return msg

    def recipients(self):
        """
        Returns a list of all recipients of the e-mail.
        """
        return self.to + self.bcc + self.cc


def internal_sendmail(to_email, from_email, body, subject, fail_silently=True):
    """
    Send a simple mail
    """
    try:
        to_field = set(to_email.split(","))
        message = SpiffyEmailMessage(subject.strip(), body, from_email, list(to_field), None, None)
        message.content_subtype = "html"
        message.send()
    except Exception, ex:
        if fail_silently:
            print str(ex)
            pass
        else:
            raise ex

def add_to_maillist(maillist, user, auteur):
    if user not in maillist and user.email and not user == auteur:
        maillist.append(user)
