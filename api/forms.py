from rest_framework import serializers


class BaseAPISerializer(serializers.Serializer):
	key = serializers.CharField(allow_blank=True, required=False)


class CreateCrisisSerializer(BaseAPISerializer):
	location = serializers.CharField(allow_blank=True)
	detail = serializers.CharField(allow_blank=True)
	assigned_agency = serializers.CharField(allow_blank=True)


class EditCrisisSerializer(BaseAPISerializer):
	location = serializers.CharField(allow_blank=True, required=False)
	detail = serializers.CharField(allow_blank=True, required=False)
	assigned_agency = serializers.CharField(allow_blank=True, required=False)


class CreateActionUpdateSerializer(BaseAPISerializer):
	description = serializers.CharField(allow_blank=True)


class UpdateCrisisStatusSerializer(BaseAPISerializer):
	status = serializers.IntegerField()
