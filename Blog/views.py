from django.shortcuts import render
from .models import Blog


def view_blog(request):
    blog = Blog.objects.all().filter(status='published')
    return render(request, 'Blog/view-blog.html', {'blog': blog})
