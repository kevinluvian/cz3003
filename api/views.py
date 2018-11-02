import random

from rest_framework.response import Response

from api.forms import BaseAPISerializer, UpdateCrisisStatusSerializer, CreateActionUpdateSerializer, EditCrisisSerializer, CreateCrisisSerializer, NotifyPublicSerializer
from api.models import Crisis, CrisisStatus, ActionUpdate, Report
from api.utils.api import api_view
from api.utils.calendar import from_timezone_to_timestamp, format_date_obj
from cz3003backend.settings import FIRE_KEY, CMC_KEY, PRIME_KEY


def serialize_action_update(action_update):
	return {
		'id': action_update.id,
		'description': action_update.description,
		'added': from_timezone_to_timestamp(action_update.added),
	}


def serialize_crisis(crisis):
	action_updates = crisis.actionupdate_set.all()
	return {
		'id': crisis.id,
		'location': crisis.location,
		'detail': crisis.detail,
		'assigned_agency': crisis.assigned_agency,
		'status': crisis.status,
		'lat': crisis.lat,
		'lng': crisis.lng,
		'action_updates': [serialize_action_update(x) for x in action_updates],
		'added': from_timezone_to_timestamp(crisis.added),
	}


def serialize_report(report):
	return {
		'id': report.id,
		'code': report.code,
		'description': report.description,
		'file_url': report.file_url,
		'date': format_date_obj(report.date)
	}


def only_cmc(func):
	def _func(request, data, *args, **kwargs):
		key = data.get('key', None)
		if key == CMC_KEY:
			return func(request=request, data=data, *args, **kwargs)
		else:
			return Response({'success': False, 'errors': ['Invalid API key']}, status=400)
	return _func


def only_fire_dept(func):
	def _func(request, data, *args, **kwargs):
		if data.get('key', None) == FIRE_KEY:
			return func(request=request, data=data, *args, **kwargs)
		else:
			return Response({'success': False, 'errors': ['Invalid API key']}, status=400)
	return _func


def only_prime(func):
	def _func(request, data, *args, **kwargs):
		if data.get('key', None) == PRIME_KEY:
			return func(request=request, data=data, *args, **kwargs)
		else:
			return Response({'success': False, 'errors': ['Invalid API key']}, status=400)
	return _func


def cmc_and_fire_dept(func):
	def _func(request, data, *args, **kwargs):
		key = data.get('key', None)
		if key == CMC_KEY or key == FIRE_KEY:
			return func(request=request, data=data, *args, **kwargs)
		else:
			return Response({'success': False, 'errors': ['Invalid API key']}, status=400)
	return _func


@api_view(['GET'], serializer=BaseAPISerializer)
def get_crisis_list(request, data):
	crisis_list = Crisis.objects.all().order_by('pk')
	return Response({'success': True, 'data': [serialize_crisis(x) for x in crisis_list]})


@api_view(['POST'], serializer=CreateCrisisSerializer)
@only_cmc
def create_crisis(request, data):
	location = data['location']
	detail = data['detail']
	assigned_agency = data['assigned_agency']

	crisis = Crisis.objects.create(
		location=location,
		detail=detail,
		lat=str(float(1.3509431) + (random.randint(0, 100) * 0.00001)),
		lng=str(float(103.6768071) + (random.randint(0, 100) * 0.00001)),
		assigned_agency=assigned_agency,
		status=CrisisStatus.IN_PROGRESS
	)
	return Response({'success': True, 'data': serialize_crisis(crisis)})


@api_view(['GET'], serializer=BaseAPISerializer)
def get_crisis_detail(request, crisis_id, data):
	crisis = Crisis.objects.filter(id=crisis_id).first()
	if crisis is None:
		return Response({'success': False, 'errors': ['Crisis does not exist']}, status=400)
	return Response({'success': True, 'data': serialize_crisis(crisis)})


@api_view(['POST'], serializer=EditCrisisSerializer)
@only_cmc
def edit_crisis(request, crisis_id, data):
	crisis = Crisis.objects.filter(id=crisis_id).first()
	if crisis is None:
		return Response({'success': False, 'errors': ['Crisis does not exist']}, status=400)
	location = data.get('location', crisis.location)
	detail = data.get('detail', crisis.detail)
	assigned_agency = data.get('assigned_agency', crisis.assigned_agency)
	crisis.location = location
	crisis.detail = detail
	crisis.assigned_agency = assigned_agency
	crisis.save()
	return Response({'success': True, 'data': serialize_crisis(crisis)})


@api_view(['POST'], serializer=CreateActionUpdateSerializer)
@cmc_and_fire_dept
def create_action_update(request, crisis_id, data):
	crisis = Crisis.objects.filter(id=crisis_id).first()
	if crisis is None:
		return Response({'success': False, 'errors': ['Crisis does not exist']}, status=400)
	description = data['description']

	ActionUpdate.objects.create(crisis=crisis, description=description)

	return Response({'success': True, 'data': serialize_crisis(crisis)})


@api_view(['POST'], serializer=UpdateCrisisStatusSerializer)
@only_cmc
def update_crisis_status(request, crisis_id, data):
	crisis = Crisis.objects.filter(id=crisis_id).first()
	if crisis is None:
		return Response({'success': False, 'errors': ['Crisis does not exist']}, status=400)
	status = data['status']
	if status not in CrisisStatus.values_list():
		return Response({'success': False, 'errors': ['Status is not valid']}, status=400)
	crisis.status = status
	crisis.save()
	return Response({'success': True, 'data': serialize_crisis(crisis)})


@api_view(['POST'], serializer=NotifyPublicSerializer)
@only_cmc
def notify_public(request, crisis_id, data):
	crisis = Crisis.objects.filter(id=crisis_id).first()
	if crisis is None:
		return Response({'success': False, 'errors': ['Crisis does not exist']}, status=400)

	description = data['description']
	# TODO: post to facebook
	return Response({'success': True, 'data': serialize_crisis(crisis)})


@api_view(['POST'], serializer=BaseAPISerializer)
@only_prime
def get_report_list(request, data):
	reports = Report.objects.all().order_by('-date')
	return Response({'success': True, 'data': [serialize_report(x) for x in reports]})


@api_view(['POST'], serializer=BaseAPISerializer)
@only_prime
def get_report_detail(request, report_id, data):
	report = Report.objects.filter(id=report_id).first()
	if report is None:
		return Response({'success': False, 'errors': ['Report does not exist']}, status=400)
	return Response({'success': True, 'data':serialize_report(report)})
