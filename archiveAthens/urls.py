from django.conf.urls import url, include  
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^', include('apps.archive_app.urls')) # And now we use the include function to pull in our first_app.urls...
] 

# if settings.DEBUG: 
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', serve, { 
#             'document_root' : settings.MEDIA_ROOT,
#         }),
#     ]