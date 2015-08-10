from django.conf import settings


class CustomURLMiddleware():
    def process_request(self, request):
        if request.user.is_authenticated() and hasattr(request.user, 'member'):
            request.urlconf = settings.ROOT_URLCONF\
                .replace('.urls',
                         '.{}_urls'.format(request.user.member.type))
