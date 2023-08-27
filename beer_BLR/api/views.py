from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TechnologySerializer, ExperienceSerializer, CategoryTalksSerializer, OneCategoryTalksSerializer, OneTalkSerializer
from ..models import Technology, Experience
from Talks.models import Talks, Category, Message
from users.models import User
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminUserOrReadOnly, IsAuthenticatedOrAdminUserOrReadOnly, IsAuthenticatedOrReadOnly
from datetime import datetime
from rest_framework.response import Response


class TechnologyListAPIView(generics.ListAPIView):
    """Прагляд усіх тэхналогій піваварэння

    Browse Brewing Technologies"""
    serializer_class = TechnologySerializer

    def get_queryset(self):
        return Technology.objects.all()\
            .order_by("name")


class OneTechnologyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Прагляд канкрэтнай тэхналогіі. Магчымасць рэдагаванне суперюзэрам

    View a specific technology. Possibility of superuser editing"""
    serializer_class = TechnologySerializer
    queryset = Technology.objects.all()
    lookup_url_kwarg = "technology_id"
    lookup_field = "id"
    permission_classes = [IsAdminOrReadOnly]


class ExperienceListAPIView(generics.ListAPIView):
    """Прагляд эксперыментальных варак юзэраў

    View experimental brews of users"""
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return Experience.objects.all()\
            .order_by("name")


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


class OneCategoryTalksListAPIView(generics.ListAPIView):
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
    """Прагляд адказаў па каанкрэтнаму пытанню. Магчымасць стварэння і рэдагавання адказаў зарэгістраванымі юзэрамі

    View answers for a specific question. Ability to create and edit responses by registered users"""
    serializer_class = OneTalkSerializer
    lookup_url_kwarg = "talks_id"
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrAdminUserOrReadOnly]

    def get_queryset(self):
        talks_id = self.kwargs.get(self.lookup_url_kwarg)
        return Message.objects.filter(talks__id=talks_id)

    def post(self, request, *args, **kwargs):
        talks_id = kwargs.get('talks_id')
        talks = Talks.objects.get(id=talks_id)
        message = Message.objects.create(talks=talks, user=request.user, description=request.data)
        serializer = self.get_serializer_class()(message)
        return Response(serializer.data)
