# from django.contrib import admin
# from django.urls import path, include

# # ✅ import these
# from django.conf import settings
# from django.conf.urls.static import static

# # ✅ FIRST define urlpatterns
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('users.urls')),
#     path('posts/', include('posts.urls')),
#     path('', include('posts.urls')),
#     path('', include('users.urls')),
#     path('posts/', include('posts.urls')),
    
# ]

# # ✅ THEN extend it
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 Landing + Auth
    path('', include('users.urls')),

    # 🔥 Dashboard + Posts
    path('posts/', include('posts.urls')),
]

# MEDIA FILES
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)