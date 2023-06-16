# Import the 'path' function from Django's URL handling module and the views module from the current package.
from django.urls import path
from . import views

# Specify the application namespace as 'blog'.
# This allows you to differentiate between URLs of different apps when referring to them using their names.
app_name = 'blog'

# Define the URL patterns for this application.
# Each URL pattern is associated with a view, which is called when the pattern is matched.
# The 'name' parameter is used to name the URL so that it can be referred to in other parts of the application.
urlpatterns = [
    # Define a URL pattern for the post list.
    # The pattern is an empty string, meaning the view will be called when the root URL of the application is visited.
    # The associated view is 'views.post_list', and the name of the URL pattern is 'post_list'.
    path('', views.post_list, name='post_list'),

    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # This is a URL pattern for the 'post_detail' view.
    # It will match URLs that are formatted like '/<year>/<month>/<day>/<slug>/'
    # The '<int:year>', '<int:month>', '<int:day>', and '<slug:post>' are path converters 
    # that capture the corresponding parts of the URL as named arguments. 
    # 'int' specifies that the argument must be an integer and 'slug' specifies that 
    # the argument must consist of ASCII letters or numbers, hyphens, or underscores.
    # The captured arguments will be passed to the 'post_detail' view.
    # 'views.post_detail' is the view function that will be invoked when this URL pattern is matched.
    # The 'name' of this URL pattern is 'post_detail', which can be used to reverse this URL pattern.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # This line creates a URL pattern for the post_share view in your Django application
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    
    # URL pattern for the 'post_comment' view. 
    # The pattern matches URLs that have the format: <base_url>/<post_id>/comment/.
    # The 'post_id' part is a dynamic part that will be passed to the 'post_comment' view as an argument.
    # The name 'post_comment' allows this URL pattern to be referred to unambiguously from elsewhere in the code, such as in 'reverse' function calls or template 'url' tags.
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),


]
