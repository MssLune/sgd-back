from rest_framework.permissions import BasePermission

ALLOW_ANY = '_ALLOW_ANY'
IS_AUTHENTICATED = '_IS_AUTHENTICATED'


class HasGroupPermission(BasePermission):
    """
    A class for setting permissions based on roles (Groups) per action in
    viewsets.

    DRF actions:
    ['list', 'create', 'retrieve', 'update', 'partial_update', 'delete']\n
    @usage: \n
    ```
    class AnyModelViewSet(ModelViewSet): \n
        ...
        permission_classes = [HasGroupPermission] \n
        permission_groups = {
          'create': ['Admin'], # Admin users can POST
          'partial_update': ['Admin', 'Management'], # Admin and Management can PATCH
          # list returns None and permission is denied. Be careful with missing actions
        }
    # You can use the ALLOW_ANY and IS_AUTHENTICATED constans for manage
    # public and only authenticated views.
        permission_groups = {
          'retrieve': [ALLOW_ANY], # Not need credentials
          'update': [IS_AUTHENTICATED], # Only authenticated users can PUT
        }
    # Another option is give permission for all actions to a Group list.\n
        permission_groups = {
            'all': [1] # Only users with a relation with group_id 1 can access
                       # to this viewset
        }
    # By default groups are searched by `pk` but you can change this by
    # defining a `group_lookup` property\
    in the viewset.\n
        group_lookup = 'name'
        permission_groups = {
            'list': ['Admin', 'Client']
        }
    ```
    If user does not have a relation with the group, group does not exists or
    its trying to check groups on an AnonymousUser, `has_permission` returns
    `False`.
    """

    def has_permission(self, request, view):
        if view.permission_groups.get('all'):  # For all viewset actions
            required_groups = view.permission_groups.get('all')
        else:
            required_groups = view.permission_groups.get(view.action)
            if required_groups is None:
                return False

        if IS_AUTHENTICATED in required_groups:
            return not request.user.is_anonymous
        elif ALLOW_ANY in required_groups:
            return True

        if request.user.is_anonymous:  # prevent check groups on AnonymousUser
            return False

        if hasattr(view, 'group_lookup'):
            group_filter = {'{}__in'.format(view.group_lookup): required_groups}
        else:
            group_filter = {'pk__in': required_groups}
        return request.user.groups.all().filter(**group_filter).exists()
