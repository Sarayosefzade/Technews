# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework.routers import DefaultRouter

# import everything from views
from .views import NewsViewSet

# define the router
router = DefaultRouter()

# define the router path and viewset to be used
router.register(r'news', NewsViewSet)

# specify URL Path for rest_framework
urlpatterns = [
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls'))
]
