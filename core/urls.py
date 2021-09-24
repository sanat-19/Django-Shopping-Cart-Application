from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path('productlist/',views.productlist,name='productlist'),
    path('catprod/<slug>/',views.catprod,name='catprod'),
    path('search/',views.search,name='search'),
    path('product_detail/<slug>',views.product_detail,name='product_detail'),
    path('cart',views.cart,name='cart'),
    path('addtocart/<str:slug>', views.addtocart, name='addtocart'),
    path('decrease_quantity/<str:slug>', views.decrease_quantity, name='decrease_quantity'),
    path('clear',views.clear, name='clear'),
    path('remove_item/<slug>',views.remove_item, name='remove_item'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('placeorder/', views.placeorder, name='placeorder'),
]
