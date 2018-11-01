from functools import wraps
from rest_framework.decorators import api_view as drf_api_view
from rest_framework.response import Response

from api.utils.logger import log


def api_view(http_method_schemas, form=None, serializer=None):
    def decorator(func):
        @wraps(func)
        @drf_api_view(http_method_schemas)
        def _func(request, *args, **kwargs):
            if form is not None:
                if request.method == 'GET':
                    data_form = form(request.query_params)
                else:
                    data_form = form(request.data)
                if not data_form.is_valid():
                    resp = Response({'success': False, 'errors': ['Invalid arguments']}, status=400)
                else:
                    data = data_form.cleaned_data
                    resp = func(request, data=data, *args, **kwargs)
            elif serializer is not None:
                if request.method == 'GET':
                    data_serializer = serializer(data=request.query_params)
                else:
                    data_serializer = serializer(data=request.data)
                if not data_serializer.is_valid():
                    errors = data_serializer.errors
                    # log.error('Error 400 %s path: %s, error: %s', str(request.data), request.path_info, str(errors))
                    resp = Response({'success': False, 'errors': ['Invalid arguments']}, status=400)
                else:
                    data = data_serializer.validated_data
                    resp = func(request, data=data, *args, **kwargs)
            else:
                resp = func(request, *args, **kwargs)
            return resp
        return _func
    return decorator
