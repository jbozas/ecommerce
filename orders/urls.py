from rest_framework.routers import DefaultRouter

from orders.views import OrderApiViewSet, CreateDestroyOrderApiViewSet

app_name = 'orders'


router = DefaultRouter()
router.register(r'orders', OrderApiViewSet, basename='orders')
router.register(r'transaction', CreateDestroyOrderApiViewSet,
                basename='transaction')
urlpatterns = router.urls
