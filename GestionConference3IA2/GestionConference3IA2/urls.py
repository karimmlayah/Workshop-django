from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root redirects to conferences list (by name)
    path("", RedirectView.as_view(pattern_name="liste_conferences", permanent=False)),
    path('conferences/', include('ConferenceApp.urls')),
    path('users/', include('UserApp.urls')),
    path('security/', include('securityConfigApp.urls')),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page=reverse_lazy('login')),
        name='logout'
    ),
    # Backward-compat: redirect /papers/... to /media/papers/...
    path(
        'papers/<path:subpath>',
        RedirectView.as_view(url='/media/papers/%(subpath)s', permanent=False),
        name='papers_compat_redirect',
    ),
    path('api/', include('SessionAppApi.urls')),
]

# Serve media files (e.g., uploaded PDFs) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
