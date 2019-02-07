
from __future__ import absolute_import
from simpleserver.celery import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from queue_task.models import Task
import requests


def get_response(url, task_id):
	#print("URL", url)
	r = requests.get("https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=uk")
	#print("response_status", r.status_code, type(r.status_code))
	if r.status_code == 404:
		Task.objects.filter(id=task_id).update(status=3, response_content=len(r.content),
			response_http_status=r.status_code, response_body=r.text)
	else:
		Task.objects.filter(id=task_id).update(status=2, response_content=len(r.content),
			response_http_status=r.status_code, response_body=r.text)
	return r


@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="server_task",
    ignore_result=True
)
def server_task():
	flag = True
	while flag:
		tasks = Task.objects.filter(status=0).order_by("id")[:4]
		# some databases do not support slices
		tasks_id = list(task.id for task in tasks)
		if len(tasks_id) < 1:
			return False
		tasks = Task.objects.filter(id__in=tasks_id)
		print(tasks.last().id)
		tasks.update(status=1)
		for task in tasks:
			response = get_response(task.url, task.id)
		flag = server_task()


