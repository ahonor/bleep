from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist

from bleeps.models import Bleep

class LatestEntries(Feed):
    title = "Latest Bleeps!"
    link = "/latest/"
    description = "The latest bleeps."

    def items(self):
        return Bleep.objects.order_by('-bleep_pub_date')[:5]

    def item_link(self):
        return "/bleeps/%s" 

class LatestComments(Feed):

    def get_object(self,bits):
        if len(bits) != 2:
            raise ObjectDoesNotExist
        if bits[0] != 'bleep':
            raise ObjectDoesNotExist
        bleep_id = bits[1]
        bleep = Bleep.objects.get(pk=bleep_id)
        return bleep

    def title(self,bleep):
        return "Bleep comments"

    def description(self,bleep):        
        return "Comments for Bleep[%s]: %s" % (bleep.id,bleep.bleep_message)

    def link(self,bleep):
        return "/comments/feeds/%s" % (bleep.id)
    
    def items(self,bleep):
        return bleep.comment_set.all()

    def item_link(self,comment):
        return "/bleeps/bleep/%s#comments_%s" % (comment.bleep.id, comment.id)
