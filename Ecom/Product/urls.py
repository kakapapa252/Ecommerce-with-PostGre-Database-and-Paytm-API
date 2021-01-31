from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("category", views.category, name="category"),
    path("subCategory/<id>", views.subCategory, name="subCategory"),
    path("subCategoryProducts/<id>", views.subCategoryProducts, name="subCategoryProducts"),
    path("productPage/<id>", views.productPage, name="productPage"),

    path("createProduct", views.createProduct, name="createProduct"),

    path("addToCart/<id>", views.addToCart, name="addToCart"),
    path("removeFromCart/<id>", views.removeFromCart, name="removeFromCart"),
    path("cart/", views.cart, name="cart"),
    path("orderHistory/", views.orderHistory, name="orderHistory"),

    path("checkout/", views.checkout, name="checkout"),
    path("handleRequest/", views.handleRequest, name="handleRequest"),
    
    path("search", views.search, name="search"),
]