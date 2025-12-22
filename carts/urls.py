from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/', views.AddToCartView.as_view(), name='cart_add'),
    path('items/<int:pk>/update/', views.UpdateCartItemView.as_view(), name='cart_item_update'),
    path('items/<int:pk>/delete/', views.DeleteCartItemView.as_view(), name='cart_item_delete'),
    path('clear/', views.ClearCartView.as_view(), name='cart_clear'),
]