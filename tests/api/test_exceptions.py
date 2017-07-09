import responses

from rest_framework import status

from .shortcuts import add_response
from .views import BaseViewTests


class ExceptionTests(BaseViewTests):

    @responses.activate
    def test_exception_arcgis_400_BAD_REQUEST(self):
        add_response(
            'GET',
            'content/users/test',
            json={'error': 'boom!'},
            status=status.HTTP_400_BAD_REQUEST
        )

        response = self.client.get(self.reverse('me-items'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
