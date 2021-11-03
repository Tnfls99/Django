from django.urls import path
from . import views

## 새로운 앱을 만들면 settings.py에 등록하는 것 잊지 말기 !!
urlpatterns = [
    ## FBV
    #path('<int:pk>/', views.single_post_page),
    #path('', views.index), # 서버 IP/blog

    ## CBV
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page), #서버IP/blog/category/slug
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]