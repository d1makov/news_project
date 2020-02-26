from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import generic
from .models import Post
from .forms import CommentForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.decorators import login_required, permission_required

#
# @permission_required('polls.can_vote')
# def my_view(request):
#     ...


@login_required()
def create_post(request, ):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home')
        else:
            messages.error(request, 'Pleas change the slug or post name!')
    return render(request, 'create_post.html', {'form': form})


def posts_list(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'index.html',
                  {'page': page,
                   'post_list': post_list})


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
