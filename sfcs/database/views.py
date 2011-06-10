from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Author, Paper, Partner, Topic, Update, Comment, PartialCommentForm, SubmitPaperForm, PartialPaperForm, PartialAuthorForm
from django.db.models import Q
from django.core.servers.basehttp import FileWrapper
import os, tempfile
from django.forms.models import modelformset_factory


PAPERS_PER_PAGE = 2


def index(request):
    featured_papers = Paper.objects.filter(featured=True, approved=True)
    recent_papers = Paper.objects.filter(approved=True).order_by('-date_added')[:5]
    recent_updates = Update.objects.order_by('-date_added')[:5]
    recent_partners = Partner.objects.order_by('-date_added')[:5]
    return render_to_response('index.html', {'featured_papers' : featured_papers,
                                             'recent_papers' : recent_papers,
                                             'recent_updates' : recent_updates,
                                             'recent_partners' : recent_partners},
                                             context_instance=RequestContext(request))
def browse(request):
    papers = Paper.objects.filter(approved=True).order_by('-date_published')[:PAPERS_PER_PAGE]
    pages = (len(papers) + PAPERS_PER_PAGE - 1) /PAPERS_PER_PAGE
    if pages == 0:
        pages = 1
    topics = Topic.objects.order_by('name')
    return render_to_response('browse.html', {'papers' : papers, 'topics' : topics, 'pages' : pages, 'page' : 1}, context_instance=RequestContext(request))

def search(request):
    page = request.GET.get('page',1)
    search = request.GET.get('search', "")
    sort = request.GET.get('sort', "-date")
    topic = request.GET.get('topic', "")
    
    papers = Paper.objects.filter(approved=True)
    
        
    if search:
        papers = papers.filter(
            Q(title__icontains=search) | Q(abstract__icontains=search) | Q(keywords__icontains=search) | Q(author__first_name__icontains=search) | Q(author__last_name__icontains=search)
        )
    if topic:
        papers = papers.filter(topic__name__icontains=topic)
    
    pages = (len(papers) + PAPERS_PER_PAGE - 1) /PAPERS_PER_PAGE
    if pages == 0:
        pages = 1
        
    if page:
        papers = papers[(int(page) - 1)*PAPERS_PER_PAGE:PAPERS_PER_PAGE*(int(page))]
    else:
        page = 1
    
    
        
    return render_to_response('search.html', {'papers' : papers, 'pages' : pages, 'page' : int(page)}, context_instance=RequestContext(request))
    

def paper_detail(request, object_id):
    paper = Paper.objects.get(pk=object_id)
    if not paper.approved:
        return HttpResponse("That paper was not approved yet.")
        
    comments = Comment.objects.filter(paper=object_id)
    return render_to_response('paper_detail.html', {'paper' : paper, 'comments' : comments}, context_instance=RequestContext(request))

def paper_download(request, object_id):
    paper = Paper.objects.get(pk=object_id)
    paper.downloads = paper.downloads + 1
    paper.save()
    
    filename = paper.paper.path
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filename)
    
    return response

def paper_comment(request, object_id):
    if request.method == 'GET':
        form = PartialCommentForm()
    elif request.method == 'POST':
        form = PartialCommentForm(request.POST)
        if form.is_valid():
            comment = Comment(paper=Paper.objects.get(pk=object_id))
            form = PartialCommentForm(request.POST, instance=comment)
            form.save()
            return  HttpResponseRedirect('/database/papers/' + object_id + '/')
    
    return render_to_response('comment_form.html', {'form' : form, 'paper_id' : object_id}, context_instance=RequestContext(request))

def author_detail(request, object_id):
    author = Author.objects.get(pk=object_id)
    papers = Paper.objects.filter(author=author.id)
    
    return render_to_response('author_detail.html', {'author' : author, 'papers' : papers}, context_instance=RequestContext(request))

def updates(request):
    UPDATES_PER_PAGE = 10
    
    updates = Update.objects.order_by('-date_added')
    pages = (len(updates) + UPDATES_PER_PAGE - 1) / UPDATES_PER_PAGE
    page = request.GET.get('page', 1)
    
    previous_page = int(page) - 1
    next_page = int(page) + 1
    
    updates = updates[(int(page) - 1)*UPDATES_PER_PAGE:UPDATES_PER_PAGE*int(page)]
    
    recent_comments = Comment.objects.order_by('-date_added')[:5]
    
    return render_to_response('updates.html', {
        'updates' : updates,
        'pages' : pages,
        'page' : int(page),
        'next_page' : next_page,
        'previous_page' : previous_page,
        'recent_comments' : recent_comments,
    }, context_instance=RequestContext(request))
    

    
def update_detail(request, object_id):
    update = Update.objects.get(pk=object_id)
    recent_updates = Update.objects.order_by('-date_added')[:5]
    
    return render_to_response('update_detail.html', {'update' : update, 'recent_updates' : recent_updates}, context_instance=RequestContext(request))

def submit(request):
    return render_to_response('submit_static.html', context_instance=RequestContext(request))
    '''
    if request.method == 'GET':
        paper_form = PartialPaperForm(prefix='paper_')
        author_form = PartialAuthorForm(prefix='author_')
    elif request.method == 'POST':   
        author = Author(featured=False)
        author_form = PartialAuthorForm(request.POST, prefix='author_', instance=author)
        if author_form.is_valid():
            new_author = author_form.save()
        else:
            return HttpResponse("Failed author")
        
        paper = Paper(featured=False, approved=False, downloads=0, author=Author.objects.get(pk=5))
        paper_form = PartialPaperForm(request.POST, prefix='paper_', instance=paper)
        if paper_form.is_valid():
            paper_form.save()
        else:
            return HttpResponse("Failed paper")
        
        return render_to_response('submitted.html', context_instance=RequestContext(request))
    
    return render_to_response('submit_form.html', {'paper_form' : paper_form, 'author_form' : author_form}, context_instance=RequestContext(request))
    '''
    
def partners(request):
    partners = Partner.objects.all()
    updates = Update.objects.filter(partner__isnull=False).order_by('-date_added')
    
    return render_to_response('partners.html', {'partners' : partners, 'partner_updates' : updates}, context_instance=RequestContext(request))


    