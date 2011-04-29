from django.core.management.base import BaseCommand, CommandError
from bleeps.models import Bleep
from services.BleepService import BleepService

class Command(BaseCommand):
    args = '<>'
    help = 'Dispatch all the queued bleeps'

    def handle(self, *args, **options):
        bleeps = Bleep.objects.filter( bleep_status='qued' )
        for bleep in bleeps:
            # Dispatch the bleep
            BleepService.dispatch(bleep)
            self.stdout.write('dispatched bleep %s to %s service\n' 
                              % (str(bleep.id), bleep.bleep_service))
