from functools import wraps
from django.shortcuts import redirect

def is_auth():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator