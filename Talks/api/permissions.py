from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAuthenticatedOrReadOnlyAndIsOwnerOrAdminChange(BasePermission):
    """Ствараць пытанне мае права толькі зарэгістраваны карыстальнік.
    Уласнік пытання мае права толькі на рэдагаванне, адміністратар і на рэдагаванне і на выдаленне.

    Only a registered user has the right to create a question.
    The owner of the question has the right to edit only, the administrator both to edit and to delete"""

    def has_permission(self, request, view):
        if request.method == "POST" and request.user and request.user.is_authenticated:
            return True
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.user == request.user:
            return True

        if (
                request.method in ["PUT", "PATCH"]
                and (request.user.has_perm("Talks.change_talks")
                     and obj.user == request.user
                     or request.user.is_staff)
        ):
            return True

        if (
                request.method in ["DELETE"]
                and request.user.is_staff
        ):
            return True

        return False


class IsAuthOrReadOnlyAndOwnerOrAdminChange(BasePermission):
    """Ствараць паведамленне мае права толькі зарэгістраваны карыстальнік.
    Уласнік паведамлення і адміністратар маюць права на рэдагаванне і на выдаленне.

    Only a registered user has the right to create a message.
     The owner of the message and the administrator have the right to edit and delete."""
    def has_permission(self, request, view):
        if request.method == "POST" and request.user and request.user.is_authenticated:
            return True
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.user == request.user:
            return True

        if (
                request.method in ["PUT", "PATCH"]
                and (request.user.has_perm("Message.change_message")
                     and obj.user == request.user
                     or request.user.is_staff)
        ):
            return True

        if (
                request.method in ["DELETE"]
                and (request.user.has_perm("Message.delete_message")
                     and obj.user == request.user
                     or request.user.is_staff)

        ):
            return True

        return False

