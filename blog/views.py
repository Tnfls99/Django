from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
# Create your views here.

## CBV ##
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post

    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        # 로그인이 되어져 있으면서 스태프 인가
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str') # template의 input name과 일치해야한다.
            if tags_str:
                tags_str = tags_str.strip() # 공백제거
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t) # 태그 모델을 받아옴
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True) # 한글에 대한 태그 허용
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView): # 모델명_form 템플릿명으로 사용
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # update인 경우 별도의 이름 지정 필요
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs): # Get으로 접근했는지 Post로 접근했는지 구분해주는 함수 - 장고가 제공
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tag_str_default'] = '; '.join(tags_str_list)
        return context

    def form_valid(self, form):
        # 다시 user에 대한 권한 체크를 할 필요가 없다.
        response = super(PostUpdate, self).form_valid(form)
        # 기존에 있던 태그 지우기
        self.object.tags.clear() # 태그가 다시 만들어진다
        tags_str = self.request.POST.get('tags_str')  # template의 input name과 일치해야한다.
        if tags_str:
            tags_str = tags_str.strip()  # 공백제거
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 태그 모델을 받아옴
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)  # 한글에 대한 태그 허용
                    tag.save()
                self.object.tags.add(tag)
        return response

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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()  #Post.objects.filter(tags=tag) #다대다 관계에서 post를 가져오는 방식이 다르다!!

    return render(request, 'blog/post_list.html',
                  {
                      'post_list' : post_list, #post_list 클래스에서 사용하는 변수
                      'categories' : Category.objects.all(),
                      'no_category_post_count' : Post.objects.filter(category=None).count(),
                      'tag': tag
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
