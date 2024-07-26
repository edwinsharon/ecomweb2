from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index,name="index"),
    path('seller/',views.sellerlogin,name="sellerlogin"),
    path('sellercreate/',views.createseller,name="createseller"),
    path('sellerindex/',views.sellerindex,name="sellerindex"),
    path('logout/',views.logoutseller,name="logout"),
    path('user/',views.userlogin,name="userlogin"),
    path('usersignup/',views.usersignup,name="usersignup"),
    path('logoutuser/',views.logoutuser,name="logoutuser"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('verification/',views.verification,name='verification'),
    path('getemail/',views.getemail,name="getemail"),
    path('addproduct/',views.addproduct,name="addproduct"),
    path('delete_g/<int:pk>',views.delete_g,name="delete"),
    path('edit_g/<int:pk>',views.edit_g,name="edit"),  
    path('productsdispaly/<int:pk>',views.productsdisplay,name="productsdisplay"),
    path('addcategory/',views.addcategory,name="addcategory"),
    path('filtercategory/',views.filtercategory,name="filtercategory"),
    path('deletecat/<int:pk>', views.deletecat, name='deletecat'),
    path('searchpro/',views.searchpro,name="searchpro"),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.view_cart, name='view_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart')

    
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
