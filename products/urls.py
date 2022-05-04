from rest_framework.routers import DefaultRouter

from products.views import ProductApiViewSet

app_name = 'products'


router = DefaultRouter()
router.register(r'products', ProductApiViewSet, basename='products')
urlpatterns = router.urls
