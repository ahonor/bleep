from django.core.management.base import BaseCommand, CommandError
from bleeps.models import Bleep, UserProfile
from services.BleepService import BleepService
import datetime

class Command(BaseCommand):
    args = '<>'
    help = 'Send the bleep digests to the subscribers'

    def handle(self, *args, **options):
        # get the list of bleeps
        digest_date = datetime.date.today()
        bleep_list = Bleep.objects.filter(bleep_pub_date__gte=digest_date)
        # get the subscribers
        subscribers = UserProfile.objects.filter(daily_digest_subscription=True)
        # get an email serivce
        service = BleepService.get_service('email')
        # process the subscribers
        for subscriber in subscribers:
            # Look up the user
            user = subscriber.user
            self.stdout.write('creating digest for user: %s\n' % user.username)
            # set up the context_data
            context_data = {'bleep_message':'Daily bleep digest',
                            'digest_date':digest_date,
                            'email_template_html':'email/digest.html',
                            'email_template_text':'email/digest.txt',
                            'email_recipients':subscriber.user.email,
                            'email_from':'bleep@example.com',
                            'bleeps':bleep_list}
            service.perform(context_data)
            
