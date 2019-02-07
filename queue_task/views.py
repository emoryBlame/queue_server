from django.shortcuts import render
from .models import Task
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

class TaskSerializer(serializers.ModelSerializer):
	"""
	Task serializer class
	"""

	class Meta:
		"""
		Task serializer meta class
		"""
		model = Task
		fields = ('id', 'url', 'status', 'response_content',\
			'response_http_status', 'response_body')


class TaskSerializerResult(serializers.ModelSerializer):
	"""
	Task id serializer
	"""

	class Meta:
		model = Task
		fields = ('id',)


@api_view(("POST",))
def send(request):
	if request.method == "POST":
		task = Task.objects.create(url=request.data.get("url"))
		return Response(TaskSerializerResult(task).data)
	else:
		return Response({"error": "Bad request."})


@api_view(("GET", ))
def result(request):
	if request.method == "GET":
		task_id = request.GET.get("id", False)
		if task_id:
			task = Task.objects.filter(id = task_id).first()
			print(task)
			if task:
				return Response(TaskSerializer(task).data)
			else:
				task = Task.objects.all().order_by('-id')[:10]
				print(task)
				return Response(TaskSerializer(task, many = True).data)
		else:
			return Response({"status": "Bad id"})
	else:
		return Response({"status": "Bad request"})


@api_view(("GET",))
def start_tasks(request):
	Task.objects.all().update(status=0)
	return Response({"status": "all task gets status New, and will updating every 2 min in case it's still new"})
