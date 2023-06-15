# Import necessary modules from Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define URL patterns for the entire project
urlpatterns = [
    # The URL for the admin site. Typically, this is at '/admin/'
    path('admin/', admin.site.urls),

    # Include the URL patterns from the 'blog' application.
    # The 'include' function takes the module (or application) to import URL patterns from and an optional 'namespace'.
    # The 'namespace' allows us to uniquely reverse named URL patterns even if different applications use the same URL names.
    # The 'blog' app's URLs will be included at the root URL ('/').
    path('', include('blog.urls', namespace='blog')),
]

# If the project is in debug mode, add URL patterns for serving media files.
# This is not recommended for production use.
# In production, these files are typically served by the web server.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
