from django.db import models

from api.utils.enum import BaseEnum


class CrisisStatus(BaseEnum):
	IN_PROGRESS = 1
	COMPLETED = 2


class Crisis(models.Model):
	location = models.TextField()
	detail = models.TextField()
	assigned_agency = models.TextField()
	status = models.IntegerField(choices=(
		(CrisisStatus.IN_PROGRESS, 'In progress'),
		(CrisisStatus.COMPLETED, 'Completed'),
	))
	lat = models.CharField(default='1.3509431', max_length=200)
	lng = models.CharField(default='103.6768071', max_length=200)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


class ActionUpdate(models.Model):
	crisis = models.ForeignKey('api.Crisis')
	description = models.TextField()
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


class Report(models.Model):
	code = models.CharField(max_length=20)
	description = models.TextField()
	date = models.DateField()
	file_url = models.TextField()
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
