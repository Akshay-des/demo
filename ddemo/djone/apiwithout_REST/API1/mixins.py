from django.http import HttpResponse
from django.core.serializers import serialize
import json
class HttpResponseMixin(object):
    def rendertohttpres(self,json_data,status=400):
        return HttpResponse(json_data,content_type='application/json',status=status)

class TextSerialize(object):
    def serialize(self,qs):
        json_data=serialize('json',qs,fields=('eno','ename','eaddr'))
        pdata=json.loads(json_data)
        finallist=[]
        for obj in pdata:
            emp=obj['fields']
            finallist.append(emp)

        json_data=json.dumps(finallist)
        return json_data