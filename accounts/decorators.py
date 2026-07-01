from functools import wraps

from django.http import HttpRequest
from django.shortcuts import redirect


def redirect_authenticated_user(view_func):
    """
    Keeps already-logged-in users away from pages like login/register
    by bouncing them back to the home page.
    """

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper
