from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def student_api(request):
    if request.method == "GET":
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get("id", None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type="application/json")

        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")

    if request.method == "POST":

        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Data created"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")
        else:
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type="application/json")

    if request.method == "PUT":

        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get("id")
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        # serializer = StudentSerializer(stu, data=pythondata, partial=True) # for complete update
        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Data updated"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")
        else:
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type="application/json")

    if request.method == "DELETE":

        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get("id")
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {"msg": "Data deleted"}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type="application/json")
