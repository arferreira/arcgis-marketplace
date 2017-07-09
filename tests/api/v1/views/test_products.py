from urllib.parse import urlencode
from rest_framework import status

from .... import factories as test_factories
from ...views import BaseViewTests


class ProductViewTests(BaseViewTests):

    def test_product_list_200_OK(self):
        response = self.client.get(self.reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_201_CREATED(self):
        product = test_factories.WebMapingAppZipFactory.build()
        response = self.client.post(
            self.reverse('product-list'), {
                'name': product.name,
                'price': int(product.price),
                'tax_rate': int(product.tax_rate)
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], product.name)

    def test_product_web_mapping_app_create_201_CREATED(self):
        product = test_factories.WebMapingAppZipFactory.build()
        path = test_factories.WebMapingAppZipFactory.file__from_path
        url = '{url}?{params}'.format(
            url=self.reverse('product-list'),
            params=urlencode(
                dict(content_type=product.content_type)
            )
        )

        with open(path, 'rb') as zip_file:
            response = self.client.post(url, {
                'name': product.name,
                'price': int(product.price),
                'tax_rate': int(product.tax_rate),
                'purpose': product.purpose,
                'api': product.api,
                'file': zip_file
            }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], product.name)

    def test_product_create_400_BAD_REQUEST(self):
        product = test_factories.WebMapingAppZipFactory.build()
        response = self.client.post(
            self.reverse('product-list'), {
                'name': product.name,
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_detail_200_OK(self):
        product = test_factories.WebMapingAppZipFactory(owner=self.account)
        response = self.client.get(product.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], product.id.hex)

    def test_product_update_200_OK(self):
        product = test_factories.WebMapingAppZipFactory(owner=self.account)
        response = self.client.patch(
            product.get_absolute_url(), {
                'name': 'updated'
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated')

    def test_product_delete_204_NO_CONTENT(self):
        product = test_factories.WebMapingAppZipFactory(owner=self.account)
        response = self.client.delete(product.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_me_products_200_OK(self):
        response = self.client.get(self.reverse('me-products-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_activate_204_NO_CONTENT(self):
        product = test_factories.WebMapingAppZipFactory(owner=self.account)

        response = self.client.post(
            self.reverse('product-activate', args=(product.id.hex,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
