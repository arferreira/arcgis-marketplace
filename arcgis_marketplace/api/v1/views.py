from orders_flavor import models as orders_models
from orders_flavor.api import serializers as orders_serializers

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from ... import models
from ...tasks import add_item_to_account

from .. import mixins
from .. import permissions

from ..decorators import offset_pagination

from . import serializers


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_value_regex = '[0-9a-f]{32}'
    queryset = models.Account.objects.active()
    permission_classes = (
        permissions.IsStaffList,
        permissions.IsStaffOrSelf,
        permissions.Signed)

    serializer_class = serializers.AccountSerializer


class ProductViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[0-9a-f]{32}'
    permission_classes = (
        permissions.OwnItem,
        permissions.ReadOnlyOrSigned,
        permissions.MeProductsSigned)

    serializer_class = orders_serializers.ItemSerializer

    # filter_class = filters.ItemFilter
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'price', 'created')

    def get_queryset(self):
        if self.request.resolver_match.url_name.startswith('me'):
            qs = self.request.user.account.items.all()
        else:
            qs = orders_models.Item.objects.all()
        return qs

    def perform_create(self, serializer):
        if 'content_type' in self.request.query_params:
            kwargs = dict(owner=self.request.user.account)
        else:
            kwargs = {}

        serializer.save(**kwargs)

    @detail_route(
        methods=['post'],
        permission_classes=(
            permissions.Signed,
            permissions.OwnItemOrPaid)
    )
    def activate(self, request, *args, **kwargs):
        account = self.request.user.account
        obj = self.get_object()

        add_item_to_account.delay(account.id, obj.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeViewSet(mixins.ArcgisAPIMixin,
                mixins.ArcgisPaginationMixin,
                viewsets.ViewSet):

    permission_classes = (permissions.Signed,)
    serializer_class = serializers.AccountSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            self.serializer_class(self.account).data
        )

    @list_route(methods=['get'])
    def groups(self, request, *args, **kwargs):
        return Response(self.account.groups)

    @list_route(methods=['get'])
    @offset_pagination
    def items(self, request, *args, **kwargs):
        data = self.account.api.user_items(
            self.account.username,
            **request.pagination_params
        )
        return self.get_paginated_response(data, request)


class SelfViewSet(mixins.ArcgisAPIMixin,
                  mixins.ArcgisPaginationMixin,
                  viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    def list(self, request, *args, **kwargs):
        return Response(self.account.self())

    def get_self_response(self, resource, request, *args, **kwargs):
        data = getattr(self.account.api, "self_{}".format(resource))(
            **request.pagination_params
        )
        return self.get_paginated_response(data, request)

    @list_route(methods=['get'])
    @offset_pagination
    def roles(self, request, *args, **kwargs):
        return self.get_self_response('roles', request, *args, **kwargs)

    @list_route(methods=['get'])
    @offset_pagination
    def users(self, request, *args, **kwargs):
        return self.get_self_response('users', request, *args, **kwargs)


class GroupViewSet(mixins.ArcgisAPIMixin,
                   mixins.ArcgisPaginationMixin,
                   viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    @offset_pagination
    def list(self, request, *args, **kwargs):
        data = self.account.api.groups(**request.pagination_params)
        return self.get_paginated_response(data, request)

    def create(self, request, *args, **kwargs):
        return Response(
            self.account.api.create_group(**request.data),
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        return Response(self.account.api.group_detail(pk))

    def update(self, request, pk=None):
        return Response(self.account.api.update_group(pk, **request.data))

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.account.api.delete_group(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def add(self, request, pk=None):
        users = request.data.get('users')
        return Response(self.account.api.add_to_group(pk, users=users))

    @detail_route(methods=['post'])
    def invite(self, request, pk=None):
        return Response(self.account.api.invite_to_group(pk, **request.data))

    @detail_route(methods=['get'])
    @offset_pagination
    def items(self, request, pk=None):
        data = self.account.api.group_items(pk, **request.pagination_params)
        return self.get_paginated_response(data, request)

    @detail_route(methods=['post'])
    def configurable_apps(self, request, pk=None):
        return Response(self.account.set_group_for_apps(pk))


class ItemViewSet(mixins.ArcgisAPIMixin,
                  mixins.ArcgisPaginationMixin,
                  viewsets.ViewSet):

    permission_classes = (permissions.Signed,)

    def create(self, request, *args, **kwargs):
        return Response(
            self.account.api.add_item(
                self.account.username,
                **request.data
            ),
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        return Response(self.account.api.item_detail(pk))

    @detail_route(methods=['post'])
    def share(self, request, pk=None):
        groups = request.data.get('groups')
        return Response(self.account.api.share_item(pk, groups))
