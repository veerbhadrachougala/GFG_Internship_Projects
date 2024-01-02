from django.urls import path
from . import views
from .views import generate_pdf
urlpatterns = [
    path('', views.productList, name="Home"),
    path('add_to_cart/', views.addToCart, name='addToCart'),
    path('cart/', views.cart, name='cart'),
    path('cartTotalQuantity/', views.cartTotalQuantity, name='cartTotalQuantity'),  
    path('plusCart/<int:product_id>', views.plusCart, name="plusCart"),
    path('minusCart/<int:product_id>', views.minusCart, name="minusCart"),
    path('removeCart/<int:product_id>', views.removeCart,name='removecart'),
    path('productDetail/<int:pk>', views.ProductDetailsView.as_view(), name="productDetail"),
    path('search/', views.search_view, name="search_view"),
    path('myOrders/', views.orders, name="myOrders"),
    path('login', views.Login,name='login'),
    path('register', views.Register,name='register'),
    path('logout', views.Log_out,name='logout'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('checkout/', views.checkout, name="checkout"),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),

    path('generate-pdf/', generate_pdf, name='generate_pdf'),
]
