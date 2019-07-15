from rest_framework import permissions

class SelfOrStaff(permissions.BasePermission):
    """
    Allow if user is calling self or user is a staff
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            print(request.user)
            return True
        elif request.user == obj:
            return True
        else:
            return False