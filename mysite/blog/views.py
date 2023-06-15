from django.shortcuts import render, get_object_or_404
from .models import Post, Comment 
from .forms import EmailPostForm , CommentForm
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

#The post_list view takes the request object as the only parameter.
def post_list(request):
    #We retrieve all the posts with the PUBLISHED status using the default manager.
    post_list = Post.objects.filter(status='PB')
    #Pagination with 3 posts per page
    # Create a Paginator object with 3 posts per page
    paginator = Paginator(post_list, 3)
    # Get the current page number from the query string, default to 1 if not present
    page_number = request.GET.get('page', 1)
    try:
        # Get posts for the current page
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    #render the list of posts with the given template
    return render(request,
                 'blog/post/list.html',
                 {'posts': posts})

# This view is responsible for displaying the details of a specific post along with its active comments and a form for new comments.
def post_detail(request, year, month, day, post):
    # It fetches the Post object based on the passed year, month, day, and slug parameters and ensures it has a status of 'PUBLISHED'. 
    # If no such post is found, a 404 error is raised.
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day)
    # It then fetches the list of active comments associated with this post.
    comments = post.comments.filter(active=True)
    # A CommentForm instance is created to be used for posting new comments to this post.
    form = CommentForm()
    # Finally, the post, active comments, and form are passed to the 'blog/post/detail.html' template for rendering.
    return render(request, 'blog/post/detail.html', {'post': post ,'comments': comments,'form': form})



def post_share(request, post_id):
    # Using the provided post_id, retrieve the post from the database with status as PUBLISHED.
    # If a post with such attributes does not exist, Django will automatically raise a 404 error.
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    # Initialize a boolean flag 'sent' as False. This flag will be used to track whether the email was successfully sent.
    sent = False 

    if request.method == 'POST': 
        # If the request method is POST, it means the form has been submitted.
        # In this case, we need to validate the submitted data.
        # Create an instance of EmailPostForm with the submitted data which is contained in request.POST
        form = EmailPostForm(request.POST) 

        if form.is_valid(): 
            # If all form fields pass the validation, we proceed with processing the form data.
            # Form data is validated against the field types defined in the form.
            # For example, 'email' and 'to' are checked to be valid email addresses.
            # Cleaned data is then available in form.cleaned_data dictionary.

            # Get cleaned/validated data from form
            cd = form.cleaned_data

            # Generate the absolute URL of the post to be shared
            post_url = request.build_absolute_uri(post.get_absolute_url())

            # Create subject of the email using the name field from the form and post's title
            subject = f"{cd['name']} recommends you read {post.title}"

            # Construct the email message body
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"

            # Send the email using Django's send_mail function. 'giftskiddo@gmail.com' is the sender's email.
            # The recipient's email address is taken from the form data.
            send_mail(subject, message, 'giftskiddo@gmail.com', [cd['to']])

            # After the email is successfully sent, set the 'sent' flag to True
            sent = True 

    else:
        # If the request method is not POST (it's a GET request), then just display an empty form
        form = EmailPostForm()

    # Render the 'share' page. If the email was sent successfully, 'sent' context variable will be True.
    # Depending on its value, a success message can be displayed on the page.
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

# Django view to handle POST requests for posting a comment
@require_POST 
def post_comment(request, post_id):
    # Get the post with provided id and PUBLISHED status or raise 404 error if not found
    post = get_object_or_404(Post, id=post_id , status = Post.Status.PUBLISHED)
    # This variable will be used to store the comment object when it gets created
    comment = None 
    # Create a CommentForm with the data from the POST request
    form = CommentForm(data=request.POST)

    # Validate the form data
    if form.is_valid():
        # If the form data is valid, create a new Comment object but don't save to DB yet
        # commit = False : the model instance is created but not saved to the database. 
        # This allows us to modify the object before finally saving it
        comment = form.save(commit = False)

        # Assign the post to the comment
        comment.post = post 

        # Save the comment to the DB
        comment.save()

    # Render the comment template with the post, form, and comment
    return render(request, 'blog/post/comment.html',{'post': post, 'form': form,'comment': comment})
