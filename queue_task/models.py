from django.db import models

# Create your models here.
Status_choices = (
	(0, "New"),
	(1, "Pending"),
	(2, "Completed"),
	(3, "Error"),
)


class Task(models.Model):
	"""
	Task model for task_queue server
	"""
	id = models.AutoField(primary_key=True)
	url = models.URLField(max_length=200)
	status = models.SmallIntegerField("Status", choices=Status_choices, default=0)
	response_content = models.IntegerField(default=0)
	response_http_status = models.IntegerField(null=True, blank=True)
	response_body = models.CharField(max_length=500, blank=True)

	class Meta:
		"""
		Meta class
		"""
		verbose_name = "TASK"
		verbose_name = "TASKS"

	def send(self, request):
		pass

