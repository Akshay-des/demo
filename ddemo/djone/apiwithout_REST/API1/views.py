from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.generic import View
from API1.mixins import HttpResponseMixin,TextSerialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.serializers import serialize
from API1.models import Employee
from API1.forms import EmployeeForm
from API1.utils import is_json

# Create your views here.
def emp_data(requests):
    empdata={

        'eno':100,
        'ename':'akshay',
        'esal':1000
    }
    resp='Employee id:{}, Name {} and salary{}'.format(empdata['eno'],empdata['ename'],empdata['esal'])
    return HttpResponse(resp)

def emp_datajson(requests):
    empdata={
        'eno': 100,
        'ename': 'akshay',
        'esal': 2000

    }
    #resp='Employee id:{}, Name {} and salary{}'.format(empdata['eno'],empdata['ename'],empdata['esal'])
    jresp=json.dumps(empdata)

    return HttpResponse(jresp, content_type='application/json')
def jsonrespdata(requests):
    empdata = {
        'eno': 100,
        'ename': 'akshay',
        'esal': 3000

    }
    return JsonResponse(empdata)

class Cbvemp(View,HttpResponseMixin):
    def post(self,requests,*args,**kwargs):
        json_data=json.dumps({'msg':"this response is from post method"})
        return self.rendertohttpres(json_data)
    def get(self,requests,*args,**kwargs):
        json_data=json.dumps({'key':'this response is from get method'})
        return self.rendertohttpres(json_data)
    def put(self,requests,*args,**kwargs):
        json_data=json.dumps({'msg':'this response is from put method'})
        return self.rendertohttpres(json_data)
    def delete(self,requests,*args,**kwargs):
        json_data=json.dumps({'key':'this response is from delete method'})
        return self.rendertohttpres(json_data)
@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCBV(TextSerialize,View,HttpResponseMixin):
    def get_employee_by_id(self,id):
        try:
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None
        return emp

    def get(self,request,*args,**kwargs):
            data=request.body

            valid_json=is_json(data)
            if not valid_json:
                json_data=json.dumps({'msg':'Provide valid input'})
                return self.rendertohttpres(json_data)

            pdata=json.loads(data)
            id=pdata.get('id',None)
            if id is not None:
                emp=self.get_employee_by_id(id)
                if emp is not None:
                    json_data = self.serialize([emp,])
                    return self.rendertohttpres(json_data,status=200)
            response={'msg':'test of github'}
            response={'msg':'given id employee does not found'}
            json_data=json.dumps(response)
            return self.rendertohttpres(json_data)
            emp=Employee.objects.all()
            json_data=self.serialize([emp,])
            return self.rendertohttpres(json_data)

    def put(self,request,id,*args,**kwargs):
        try:
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            json_data=json.dumps({'msg':'Employee does not exists'})
            return self.rendertohttpres(json_data)
        if emp is None:
            json_data=json.dumps({'msg':'requested data not found'})
            return self.rendertohttpres()

        new_data = request.body
        Validjson_data=is_json(new_data)
        if not Validjson_data:
            json_data= json.dumps({'msg':'Enter valid input'})
            return self.rendertohttpres(json_data)
        original_data={
            'eno':emp.eno,
            'ename':emp.ename,
            'esal':emp.esal,
            'eaddr':emp.eaddr
        }

        pdata=json.loads(new_data)
        original_data.update(pdata)
        form=EmployeeForm(original_data,instance=emp)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'msg':'Record updated successfully'})
            return self.rendertohttpres(json_data,status=200)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.rendertohttpres(json_data)

    def delete(self,request,id,*args,**kwargs):
        try:
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            json_data=json.dumps({'msg':'Requested id employee does not exists'})
            return self.rendertohttpres(json_data)
        status,employee=emp.delete()
        if status==1:
            json_data=json.dumps({'msg':'employee deleted successfully'})
            return self.rendertohttpres(json_data)
        json_data=json.dumps({'msg':'there is some error, unable to delete record'})
        return self.rendertohttpres(json_data)
        #serialize does the similar job as below commented code
        '''        emp_data={
            'Employee no':emp.eno,
            'Employee Name':emp.ename,
            'Employee salary':emp.esal,
            'Employee Address':emp.eaddr,
        }

        json_data=json.dumps(emp_data)
        '''

#        return HttpResponse(json_data,content_type='Application\json')

@method_decorator(csrf_exempt,name='dispatch')
class EmployeeLCBV(TextSerialize,View,HttpResponseMixin):
    def get(self,requests,*args,**kwargs):
        empqs=Employee.objects.all()
        json_data=self.serialize(empqs)
        '''json_data=serialize('json',empqs,fields=('eno','ename','eaddr'))
        pdata=json.loads(json_data)
        finallist=[]
        for obj in pdata:
            emp=obj['fields']
            finallist.append(emp)

        json_data=json.dumps(finallist)'''
        return HttpResponse(json_data,content_type='Application/json')

    def post(self,request,*args,**kwargs):
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            json_data=json.dumps({'msg':'Please enter valid input'})
            return self.rendertohttpres(json_data)
        json_data=json.dumps({'msg':'you provided valid jason data only'})
        empdata=json.loads(data)
        form=EmployeeForm(empdata)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'msg':'record inserted successfully'})
            return self.rendertohttpres(json_data,status=200)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.rendertohttpres(json_data,status=404)
