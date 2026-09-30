from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Direct friendly category URL endpoints (singular and plural)
    path('racket/', views.home, {'category_slug': 'racquets'}, name='racket'),
    path('rackets/', views.home, {'category_slug': 'racquets'}, name='rackets'),
    path('racquet/', views.home, {'category_slug': 'racquets'}, name='racquet'),
    path('racquets/', views.home, {'category_slug': 'racquets'}, name='racquets'),

    path('footwear/', views.home, {'category_slug': 'footwear'}, name='footwear'),
    path('shoes/', views.home, {'category_slug': 'footwear'}, name='shoes'),
    path('shoe/', views.home, {'category_slug': 'footwear'}, name='shoe'),

    path('shuttlecocks/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttlecocks'),
    path('shuttlecock/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttlecock'),
    path('shuttles/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttles'),
    path('shuttle/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttle'),

    path('bags-gear/', views.home, {'category_slug': 'bags-gear'}, name='bags_gear'),
    path('bags/', views.home, {'category_slug': 'bags-gear'}, name='bags'),
    path('gear/', views.home, {'category_slug': 'bags-gear'}, name='gear'),
    path('bag/', views.home, {'category_slug': 'bags-gear'}, name='bag'),

    path('category/<slug:category_slug>/', views.home, name='category_filter'),

    # Auth & Checkout
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
]
