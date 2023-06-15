from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User
from django.urls import reverse



#Post model
class Post(models.Model):
    #allow us to manage the status of blog posts 
    class Status(models.TextChoices):
        #using Draft and Published statuses for posts.
        DRAFT = 'DF' , 'Draft'
        PUBLISHED = 'PB', 'Published'
    #This is the field for the post title. This is a CharField field that translates into a VARCHAR
    #column in the SQL database.
    title = models.CharField(max_length = 250)
    #This is the field for the post topic. This is a CharField field that translates into a VARCHAR
    #column in the SQL database.
    #we let users decide what topic is that 
    topic = models.CharField(max_length = 25 , default='topic')
    #This is a SlugField field that translates into a VARCHAR column in the SQL database
    #the slug field to build beautiful, SEO-friendly URLs
    slug = models.SlugField(max_length = 250 , unique_for_date='publish')
    # This field sets up a many-to-one relationship, linking each post to a user. A user can author many posts.
    # It creates a foreign key in the database, referencing the primary key of the user model. 
    # If the referenced user is deleted (on_delete=CASCADE), all related posts will also be deleted.
    author = models.ForeignKey(User , on_delete = models.CASCADE , related_name = 'blog_posts')

    #This is the field for storing the body of the post. 
    #This is a TextField field that translates into a TEXT column in the SQL database
    body = models.TextField()

    #image field  to allow users to upload pictures
    #You will need to set up media file handling for this to work properly
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)


    #to store the date and time when the post was published. 
    #We use Django’s timezone.now method as the default value for the field
    publish = models.DateTimeField(default = timezone.now)
    #to store the date and time when the post was created.
    #By using auto_now_add, the date will be saved automatically when creating an object
    created = models.DateTimeField(auto_now_add = True)
    #store the last date and time when the post was updated.
    #By using auto_now, the date will be updated automatically when saving an object
    updated = models.DateTimeField(auto_now = True)
    # The "Status" enumeration class provides two status options for a post: "DRAFT" and "PUBLISHED", 
    # represented by the values "DF" and "PB", respectively.
    status = models.CharField(max_length = 2 , choices=Status.choices , default = Status.DRAFT)

 

    #Defining a default sort order, This class defines metadata for the model
    class Meta:
        # We use the ordering attribute to tell Django that it should sort results by the publish field
        ordering = ['-publish']

        #Adding a database index This option allows you to define database
        #indexes for your model, which could comprise one or multiple fields, in ascending or descending order
        indexes = [models.Index(fields=['-publish']),]


    #the default Python method to return a string with the human-readable representation
    def __str__(self):
        return self.title

    # This method returns the canonical URL for a Post object.
    # It uses Django's 'reverse' function to generate a URL using URL configuration.
    # 'reverse' function takes a view name and optional arguments and returns the URL path string.
    # 'blog:post_detail' is the name of the URL pattern for the view that shows the details of a post (namespaced to the 'blog' application).
    # The 'args' parameter is a list of arguments to pass to the view.
    # In this case, it's a list containing 'self.id', which is the ID of the post. 
    # So, this function will return a string like '/blog/<id>/', where '<id>' is the ID of the post.
    def get_absolute_url(self):
        return reverse('blog:post_detail' , args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    # Each comment is related to a Post. When a Post is deleted, all comments related to it will be deleted as well.
    post = models.ForeignKey(Post , on_delete =models.CASCADE , related_name='comments')
    
    # Name of the person who made the comment.
    name = models.CharField(max_length = 80)
    
    # Email of the person who made the comment.
    email = models.EmailField()

    # The text of the comment.
    body = models.TextField()
    
    # The time when the comment was created, automatically set to the current time when the comment is created.
    created = models.DateTimeField(auto_now_add = True)

    # The time when the comment was last updated, automatically set to the current time whenever the comment is saved.
    updated = models.DateTimeField(auto_now = True)

    # Boolean to show if a comment is active or not. Default value is True.
    active = models.BooleanField(default=True)

    class Meta:
        # Comments are ordered by the time they were created.
        ordering = ['created']

        # Indexing the 'created' field for faster retrieval of comments based on the creation date.
        indexes = [ models.Index(fields=['created']),]

    # The string representation of a comment includes the commenter's name and the post that the comment belongs to.
    def __str__(self):
        return f'Comment by{self.name} on {self.post}' 
