from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView
# Create your views here.

## CBV ##
class PostList(ListView):
    model = Post
    ordering = '-pk'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

#    template_name = 'blog/post_list.html'
# post_list.html // post_list= model name

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
# post_detail.html // post = model name
## FBV ##
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html',
                  {
                      'post_list' : post_list, #post_list 클래스에서 사용하는 변수
                      'categories' : Category.objects.all(),
                      'no_category_post_count' : Post.objects.filter(category=None).count(),
                      'category': category
                  })
## FBV
#def index(request):
 #   posts = Post.objects.all().order_by('-pk')
#
 #   return render(
  #      request,
   #     'blog/post_list.html',
    #    {
     #       'posts' : posts
      #  }
    #)
#def single_post_page(request, pk):
#    post = Post.objects.get(pk=pk)
#
 #   return render(
  #      request,
   #     'blog/post_detail.html',
  #      {
   #         'post': post, 콤마 잊지 말고 작성하기 !
   #     }
   # )
