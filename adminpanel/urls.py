from django.urls import path
from adminpanel.views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',admin.as_view(),name='admin'),
    path('products',products.as_view(),name='products'),
    
    path('productadd',ProductAdd.as_view(),name='productadd'),
    path('listproduct',listproduct.as_view(),name='listproduct'),

    path('deleteproduct/(?P<pk>[0-9]+)/$',deleteproduct.as_view(),name='deleteproduct'),
    path('productdetail/(?P<pk>[0-9]+)/$',productdetail.as_view(),name='productdetail'),

    path('listfeedback/',listfeedback.as_view(),name='listfeedback'),

    path('<pk>/update',ProductUpdate.as_view(),name='update'),
    path('order',OrderDetails.as_view(),name='order'),
    path('<pk>/order_update',OrderUpdate.as_view(),name='order_update'),
    path('deleteorder/(?P<pk>[0-9]+)/$',deleteOrder.as_view(),name='deleteorder'),
    path('customer/',CustomerView.as_view(),name='customer'),
    path('<pk>/customer_update',CustomerUpdate.as_view(),name='customer_update'),
    path('delete_customer/(?P<pk>[0-9]+)/$',deleteCustomer.as_view(),name='delete_customer'),

    path('employee/',EmployeeView.as_view(),name='employee'),
    path('<pk>/employee_update',EmployeeUpdate.as_view(),name='employee_update'),
    path('delete_employee/(?P<pk>[0-9]+)/$',deleteEmployee.as_view(),name='delete_employee'),

    path('register/',CustomerRegister.as_view(),name='cust_reg'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),


    path('staffprofile/',StaffProfile.as_view(),name='staffprofile'),
]
