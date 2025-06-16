import json
from unittest.mock import MagicMock, PropertyMock, patch

from rest_framework.test import APIRequestFactory


def _mock_question(id, title, delete=False):
    mock = MagicMock()
    mock.id = id
    mock.title = title
    if delete:
        mock.delete.return_value = None
    return mock


def _mock_request(method, url, user_authenticated=True, data=None):
    factory = APIRequestFactory()
    req_method = getattr(factory, method.lower())
    if data is not None:
        request = req_method(
            url, data=json.dumps(data), content_type="application/json"
        )
    else:
        request = req_method(url)
    request.user = MagicMock(is_authenticated=user_authenticated)
    return request


def _mock_view_response(
    viewset_cls, action_map, request, pk=None, mock_obj=None, serializer_data=None
):
    view = viewset_cls.as_view(action_map)
    patches = []
    if mock_obj is not None:
        patches.append(patch.object(viewset_cls, "get_object", return_value=mock_obj))
    if serializer_data is not None:
        mock_serializer = MagicMock()
        type(mock_serializer).data = PropertyMock(return_value=serializer_data)
        mock_serializer.is_valid = MagicMock(return_value=True)
        mock_serializer.save = MagicMock(return_value=mock_obj)
        mock_serializer.errors = {}
        patches.append(
            patch.object(viewset_cls, "get_serializer", return_value=mock_serializer)
        )
    # Apply all patches
    with patches[0] if patches else patch("builtins.id", lambda x: x):
        with patches[1] if len(patches) > 1 else patch("builtins.id", lambda x: x):
            if pk is not None:
                return view(request, pk=pk)
            return view(request)
