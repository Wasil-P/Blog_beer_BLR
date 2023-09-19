from rest_framework import generics
from rest_framework.response import Response

from ..models import Technology, Experience
from .serializers import TechnologySerializer, ExperienceSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminUserOrReadOnly, IsAuthenticatedOrReadOnly


class TechnologyListAPIView(generics.ListCreateAPIView):
    """Прагляд усіх тэхналогій піваварэння. Магчымасць стварэння тэхналогіі адмінам

    Browse Brewing Technologies. Possibility to create technology by administrator"""
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Technology.objects.all()\
            .order_by("name")

    def post(self, request, *args, **kwargs):
        technology = Technology.objects.create(name=request.data, description=request.data)
        serializer = self.get_serializer_class()(technology)
        return Response(serializer.data)


class OneTechnologyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Прагляд канкрэтнай тэхналогіі. Магчымасць рэдагавання адмінам

    View a specific technology. Possibility of admin editing"""
    serializer_class = TechnologySerializer
    queryset = Technology.objects.all()
    lookup_url_kwarg = "technology_id"
    lookup_field = "id"
    permission_classes = [IsAdminOrReadOnly]


class ExperienceListAPIView(generics.ListCreateAPIView):
    """Прагляд эксперыментальных варак юзэраў. Магчымасць ствараць новыя варкі
    зарэгістраванымі юзэрамі.

    View experimental brews of users. Ability to create new brews
     registered users."""
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Experience.objects.all()\
            .order_by("name")

    def post(self, request, *args, **kwargs):
        experience = Experience.objects.create(name=request.data, user=request.user, description=request.data)
        serializer = self.get_serializer_class()(experience)
        return Response(serializer.data)


class OneExperienceAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Прагляд канкрэтнага вопыту. Магчымасць рэдагаванне паста уласнікам, ці суперюзэрам

    View a specific experience. The possibility of editing the post by the owner or superuser"""
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    lookup_url_kwarg = "experience_id"
    lookup_field = "id"
    permission_classes = [IsOwnerOrAdminUserOrReadOnly]

