from rest_framework import permissions


class IsServiceSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow service super admins to add/delete museums and add/delete museum super admins
    """

    def has_permission(self, request, view):
        print(request.user.groups.filter(name='service_super_admins').exists())
        return request.user.groups.filter(name='service_super_admins').exists()


class IsMuseumSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow museum super admins to add/delete museum admins
    """

    def has_permission(self, request, view):
        print(request.user.groups.filter(name='museum_super_admins').exists())
        return request.user.groups.filter(name='museum_super_admins').exists()


class IsMuseumAdmin(permissions.BasePermission):
    """
    Custom permission to only allow museum admins to edit museums
    """

    def has_permission(self, request, view):
        print(request.user.groups.filter(name='museum_admins').exists())
        return request.user.groups.filter(name='museum_admins').exists()


class IsMuseumCashier(permissions.BasePermission):
    """
    Custom permission to only allow museum cashiers to create new tickets
    """

    def has_permission(self, request, view):
        print(request.user.groups.filter(name='museum_cashiers').exists())
        return request.user.groups.filter(name='museum_cashiers').exists()
