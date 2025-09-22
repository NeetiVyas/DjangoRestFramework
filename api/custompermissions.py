from rest_framework.permissions import BasePermission
from rest_framework import permissions


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return False
    

class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        #SAFE_METHODS includes ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user