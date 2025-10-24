from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url="/conferences/liste/")),
    path('conferences/', include('ConferenceApp.urls')),
    path('users/', include('UserApp.urls'))
]
