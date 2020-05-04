from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.

#class based views
class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'templates/blog/post/list.html'

#function based views    
def post_list(request,  tag_slug=None):
    object_list = Post.objects.all() #you can also use 'Post.published.all' since yiu created a manager for it
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) #3 post for each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts' : posts,
        'page': page,
        'tag' : tag,
    }
    return render ( request, 'templates/blog/post/list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published', publish__year=year,publish__month=month,publish__day=day)
    #list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    #list of similar posts
    post_tags_id = post.tags.values_list('id', flat=True)

    #exclude current post
    similar_posts = Post.objects.filter(tags__in = post_tags_id).exclude(id=post.id)

    #publish most recent 4 posts
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    
    if request.method == 'POST':
        comment_form =  CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment but dont save to database yet
            new_comment = comment_form.save(commit=False)

            #assign current post to the comment
            new_comment.post = post
            
            #save comment to the database
            new_comment.save()
    else:
        comment_form =  CommentForm()
    context = {
        'post' : post,
        'comments' : comments,
        'new_comment' : new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,

    }
    return render (request, 'templates/blog/post/detail.html', context)


def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            print('yeah')
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f'{post.title}'
            message = f'read {post.title} at {post_url} \n' f"{cd['name']} comments: {cd['comments']}"
            send_mail(subject, message, 'jerrynelson78@yahoo.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
   
    return render(request, 'templates/blog/post/share.html', {'post':post, 'form':form, 'sent':sent,})

