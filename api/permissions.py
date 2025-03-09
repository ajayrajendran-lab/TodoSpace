from rest_framework.permissions import BasePermission
from myapp.models import Todo
class IsOwnerPermissionRequired(BasePermission):

    def has_object_permission(self,request,view,obj):
        return request.user == obj.owner