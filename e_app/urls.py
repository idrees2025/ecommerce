from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from e_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('keyboardpage/',views.keyboards_view.as_view(),name='keyboard'),
    path('graphic cards page/',views.graphiccards_view.as_view(),name='gpu'),
    path('ledspage/',views.leds_view.as_view(),name='led'),
    path('huddies/',views.huddies_view.as_view(),name='huddie'),
    path('register/',views.register.as_view(),name='register'),
    path('login/',views.login_view.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('detail/<int:pk>',views.detail_view.as_view(),name='detail'),
    path('shopingform/<int:item_id>',views.add_to_cart,name='addtocart'),
    path('cart/',views.cart,name='cart'),
    path('increase/<int:item_id>',views.increase_item,name='increase'),
    path('decrease/<int:item_id>',views.decrease_item,name='decrease'),
    path('remove/<int:item_id>',views.remove_item,name='remove'),
    path('checkout/',views.checkout,name='checkout'),
    path('success/',views.success_view,name='success'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
