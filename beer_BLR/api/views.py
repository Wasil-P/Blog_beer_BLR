from rest_framework import generics
from rest_framework.response import Response

from ..models import Technology, Experience
from Talks.models import Talks, Category, Message
from .serializers import TechnologySerializer, ExperienceSerializer, CategoryTalksSerializer, \
    OneCategoryTalksSerializer, OneTalkSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminUserOrReadOnly, \
    IsOwnerOrAdminUserHasDeleteOrReadOnly, IsAuthenticatedOrReadOnly


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


class CategoryTalksListAPIView(generics.ListAPIView):
    """Прагляд усіх катэгорый для форума

    View all categories for the forum"""
    serializer_class = CategoryTalksSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Category.objects.all().order_by("name")


class OneCategoryTalksListAPIView(generics.ListCreateAPIView):
    """Прагляд усіх пытанняў ад карыстальнікаў па канкрэтнай катэгорыі.
    Магчымасць ствараць новыя пытанні па канкрэтнай катэгорыі зарэгістраваным юзэрам

    View all questions from users in a specific category.
    Ability to create new questions for a specific category by registered users"""
    serializer_class = OneCategoryTalksSerializer
    lookup_url_kwarg = "category_id"
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Talks.objects.all()\
            .order_by('category')

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = Category.objects.get(id=category_id)
        talks = Talks.objects.create(category=category, user=request.user, question=request.data)
        serializer = self.get_serializer_class()(talks)
        return Response(serializer.data)


class OneTalkListAPIView(generics.ListAPIView):
    """Прагляд адказаў па каанкрэтнаму пытанню. Магчымасць стварэння і
    рэдагавання адказаў зарэгістраванымі юзэрамі

    View answers for a specific question. Ability to create and edit responses by registered users"""
    serializer_class = OneTalkSerializer
    lookup_url_kwarg = "talks_id"
    lookup_field = "id"
    permission_classes = [IsOwnerOrAdminUserHasDeleteOrReadOnly]

    def get_queryset(self):
        talks_id = self.kwargs.get(self.lookup_url_kwarg)
        return Message.objects.filter(talks__id=talks_id)

    def post(self, request, *args, **kwargs):
        talks_id = kwargs.get('talks_id')
        talks = Talks.objects.get(id=talks_id)
        message = Message.objects.create(talks=talks, user=request.user, description=request.data)
        serializer = self.get_serializer_class()(message)
        return Response(serializer.data)
