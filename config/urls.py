from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from chat_app.page_views import index_view, register_page_view, home_view, conversation_page_view

urlpatterns = [
    path("", index_view, name="index"),
    path("register/", register_page_view, name="register-page"),
    path("home/", home_view, name="home"),
    path("chat/<str:conversation_id>/", conversation_page_view, name="conversation-page"),

    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include("chat_app.urls")),
]