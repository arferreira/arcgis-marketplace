from rest_framework.routers import SimpleRouter

from . import views


app_name = 'arcgis_marketplace.api.v1'
router = SimpleRouter(trailing_slash=False)

router.register(r'accounts', views.AccountViewSet)
router.register(r'products', views.ProductViewSet, base_name='product')
router.register(r'self', views.SelfViewSet, base_name='self')
router.register(r'me', views.MeViewSet, base_name='me')
router.register(r'me/products', views.ProductViewSet, base_name='me-products')
router.register(r'groups', views.GroupViewSet, base_name='group')
router.register(r'items', views.ItemViewSet, base_name='item')


urlpatterns = router.urls
