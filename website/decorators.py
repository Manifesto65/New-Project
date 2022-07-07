from django.urls import reverse
from django.http import HttpResponseRedirect
from functools import wraps


def auth_decorator(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        return_url = request.META['PATH_INFO']
        if not request.session.get('user_id'):
            return HttpResponseRedirect(f'{reverse("website:login")}?return_url={return_url}')
        return view(request, *args, **kwargs)

    return wrapper
