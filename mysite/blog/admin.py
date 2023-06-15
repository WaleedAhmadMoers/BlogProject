from django.contrib import admin
from .models import Post , Comment




#Adding models to the administration site
@admin.register(Post)
#Customizing how models are displayed
#In this class, we can include information about how to display the model on the site and how to interact with it
class PostAdmin(admin.ModelAdmin):
    #The list_display attribute allows you to set the fields of your model that you want to display on the administration object list page
    list_display = ['title' , 'slug' , 'author', 'topic','publish', 'status']
    # filter the results by the fields included in the list_filter attribute
    list_filter = ['status', 'topic', 'created', 'publish', 'author']
    #searchable fields using the search_fields attribute
    search_fields = ['title', 'body']
    #navigation links to navigate through a date hierarchy
    date_hierarchy = 'publish'


@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']