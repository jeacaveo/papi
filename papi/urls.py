"""papi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import (
    include,
    path,
    re_path,
    )

from rest_framework import (
    permissions,
    routers,
    )
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from units import views as unit_views


SchemaView = get_schema_view(
    openapi.Info(
        title="Prismata API",
        default_version='v1',
        description="REST API for Prismata related data.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jv@venturasystems.net"),
        license=openapi.License(name="AGPLv3+ License"),
        ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    )


ROUTER = routers.DefaultRouter()
ROUTER.register(r'latest/units', unit_views.LatestUnitVersionViewSet)


urlpatterns = [  # pylint: disable=invalid-name
    re_path(
        r'^api/docs/swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0),
        name='schema-json'),
    re_path(
        r'^api/docs/swagger/$',
        SchemaView.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    re_path(
        r'^api/docs/redoc/$',
        SchemaView.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    path("api/auth/", include("rest_framework.urls")),
    path("api/", include(ROUTER.urls)),
    ]
