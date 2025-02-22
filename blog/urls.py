from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, AboutPageView, upload_file, transaction_list,dashboard

urlpatterns = [
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
	path("", BlogListView.as_view(), name="home"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('upload/', upload_file, name='upload_file'),
    path('transaction/', transaction_list, name='product_detail'),
    path('dashboard/', dashboard, name='dashboard'),
]

