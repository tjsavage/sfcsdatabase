from django.db import models
from django.forms import ModelForm
from django import forms

class Paper(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', blank=True, null=True)
    topic = models.ForeignKey('Topic', blank=True, null=True)
    abstract = models.TextField(blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    paper = models.FileField(upload_to='papers/')
    image = models.FileField(upload_to='images/paper_images/', blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    downloads = models.IntegerField(editable=False, default=0)
    
    
    def __unicode__(self):
        return self.title

class Author(models.Model):
    full_name = models.CharField(max_length=100, blank=True)
    image = models.FileField(upload_to="images/author_images/", blank=True, null=True)
    bio = models.TextField(blank=True)
    year = models.IntegerField(blank=True)
    email = models.EmailField(blank=True)
    featured = models.BooleanField()
    
    
    def __unicode__(self):
        return self.full_name


class Topic(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField(blank=True)
    image = models.FileField(upload_to="images/partner_images/", blank=True, null=True)
    date_added = models.DateField(auto_now_add=True, null=True)
    
    def __unicode__(self):
        return self.name
    
class Update(models.Model):
    date_added = models.DateField(auto_now=True)
    headline = models.CharField(max_length=100)
    body = models.TextField()
    keywords = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=100, blank=True)
    partner = models.ForeignKey('Partner', blank=True, null=True)
    
    
    def __unicode__(self):
        return str(self.date_added) + ": " + self.headline
        
    def short_body(self, length=100, suffix='...'):
        if len(self.body) <= length:
            return self.body
        else:
            return ' '.join(self.body[:length+1].split(' ')[0:-1]) + suffix
        
class Comment(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    paper = models.ForeignKey('Paper')
    title = models.CharField(max_length=50)
    body = models.TextField()
    rating = models.IntegerField()
    
    def __unicode__(self):
        return str(self.date_added) + ": " + self.paper.title
    
class PartialCommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('paper',)
    
    '''
    class Media:
        css = {
            'all': ('admin/css/forms.css',),
        }
    '''
class SubmitPaperForm(forms.Form):
    title = forms.CharField(max_length=100)
    abstract = forms.CharField(widget=forms.Textarea)
    author_first_name = forms.CharField(max_length=50)

class PartialPaperForm(ModelForm):
    
    class Meta:
        model = Paper
        exclude = ('featured', 'downloads', 'approved', 'author', 'date_published')
        
class PartialAuthorForm(ModelForm):
    
    class Meta:
        model = Author
        exclude = ('featured',)