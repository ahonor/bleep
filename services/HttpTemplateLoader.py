from django.template import TemplateDoesNotExist
import urllib2
import time
class HttpTemplateDoesNotExist(TemplateDoesNotExist):
    """
    Error thrown by HttpTemplateLoader if HTTP request fails for template
    """

def load_template_source(template_name, template_dirs=None):
    # Check if template_name is an http url
    result = urllib2.urlparse.urlparse(template_name)
    if not result.scheme.startswith('http') or not result.netloc:
        raise HttpTemplateDoesNotExist, template_name
    try:
        req = urllib2.Request(template_name)
        begin = time.time()
        f = urllib2.urlopen(req)
        print 'debuggery: %s download in %s secs' % (template_name, str(time.time() - begin))
        source = f.read()
        return (source, template_name)
    except urllib2.HTTPError, e:
        print 'The server could not fulfill the request. error code: ', e.code
        raise HttpTemplateDoesNotExist, template_name
    except urllib2.URLError, e:
        print 'Failed to reach the server. Reason: ', e.reason
        raise HttpTemplateDoesNotExist, template_name
load_template_source.is_usable = True

