from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check if the user is authenticated
        if request.user.is_authenticated:
            # list of paths to check (only add login/register pages here)
            path_to_redirect = [
                reverse('blog:login'),
                reverse('blog:register'),
            ]

            if request.path in path_to_redirect:
                return redirect(reverse('blog:index'))

        response = self.get_response(request)
        return response

class RestrictunauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check if the user is authenticated
        if not request.user.is_authenticated:
            # list of paths to check (only add login/register pages here)
            Restricted_path = [
                reverse('blog:dashboard'),
            ]

            if request.path in Restricted_path:
                return redirect(reverse('blog:index'))

        response = self.get_response(request)
        return response
