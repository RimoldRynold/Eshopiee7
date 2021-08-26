from django.urls import path
from .views import Index,contact,contactsubmit,Signup,Login,logout,Cart,CheckOut,OrderView,ProfileUpdate


urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('contact',contact,name='contact'),
    path('contactsubmit',contactsubmit,name='contactsubmit'),

    path('signup',Signup.as_view(),name='signup'),
    path('login1',Login.as_view(),name='login1'),
    path('logout',logout,name='logout'),
    path('cart',Cart.as_view(),name='cart'),
    path('check-out',CheckOut.as_view(),name='checkout'),
    path('orders',OrderView.as_view(),name='orders'),

    path('<pk>/profile_update',ProfileUpdate.as_view(),name='profile_update'),
]
