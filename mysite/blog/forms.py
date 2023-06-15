# Import forms module from Django
from django import forms 
from .models import Comment 

# Define the form for emailing a post
class EmailPostForm(forms.Form):
    # Form field for the sender's name, character limit of 25
    name = forms.CharField(max_length=25) 
    # Form field for the sender's email, must be valid email format
    email = forms.EmailField()
    # Form field for the recipient's email, must be valid email format
    to = forms.EmailField()
    # Form field for additional comments, not required, displayed as a textarea
    comments = forms.CharField(required=False, widget=forms.Textarea)


# This is a Django form for the Comment model
class CommentForm(forms.ModelForm):
    class Meta:
        # The model to use for this form is Comment
        model = Comment  
        # The fields from Comment model to include in the form
        fields =['name' , 'email' , 'body'] 
