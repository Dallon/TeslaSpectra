from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class BlockThirdPartyCookiesMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        accepted_cookies = request.COOKIES.get('accepted_cookies')
        if not accepted_cookies or accepted_cookies != "true":

            # Check the current URL to see if it's one of the pages with third-party cookies
            if request.path == '/onyoutube/' or request.path == '/onreddit/':
                # Redirect to the homepage if the user hasn't accepted the cookies
                response = self.get_response(request)
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response['Expires'] = '0'
                response['Pragma'] = 'no-cache'
                response.delete_cookie("_ga")
                response.delete_cookie("_gid")
                response.delete_cookie("_gat")
                return redirect('home')

        response = self.get_response(request)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Expires'] = '0'
        response['Pragma'] = 'no-cache'
        return response

    