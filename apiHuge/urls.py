from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'recipes', views.RecipeViewSet)
router.register(r'plants', views.PlantViewSet)
router.register(r'retailers', views.RetailerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'openapi-schema', get_schema_view(
        title="Greg's Django Rest API",  # Title of your app
        description="General Use API <br> gregstull.fly.dev/recipes <br> gregstull.fly.dev/plants <br> gregstull.fly.dev/retailers",  # Description of your app
        version="1.0.0",
        public=True,
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui')
]