from rest_framework import generics
from rest_framework.response import Response

from ..models import Talks, Category, Message
from .serializers import CategoryTalksSerializer, OneCategoryTalksSerializer, OneTalkSerializer
from .permissions import IsAdminOrReadOnly, IsAuthOrReadOnlyAndOwnerOrAdminChange, \
    IsAuthenticatedOrReadOnlyAndIsOwnerOrAdminChange


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
    permission_classes = [IsAuthenticatedOrReadOnlyAndIsOwnerOrAdminChange]

    def get_queryset(self):
        return Talks.objects.all()\
            .order_by('category')

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = Category.objects.get(id=category_id)
        talks = Talks.objects.create(category=category, user=request.user, question=request.data)
        serializer = self.get_serializer_class()(talks)
        return Response(serializer.data)


class OneTalkListAPIView(generics.ListCreateAPIView):
    """Прагляд адказаў па каанкрэтнаму пытанню. Магчымасць стварэння і
    рэдагавання адказаў зарэгістраванымі юзэрамі

    View answers for a specific question. Ability to create and edit responses by registered users"""
    serializer_class = OneTalkSerializer
    lookup_url_kwarg = "talks_id"
    lookup_field = "id"
    permission_classes = [IsAuthOrReadOnlyAndOwnerOrAdminChange]

    def get_queryset(self):
        talks_id = self.kwargs.get(self.lookup_url_kwarg)
        category_id = Talks.objects.get(id=talks_id).category.id
        return Message.objects.filter(talks__category__id=category_id, talks__id=talks_id)

    def post(self, request, *args, **kwargs):
        talks_id = kwargs.get('talks_id')
        talks = Talks.objects.get(id=talks_id)
        message = Message.objects.create(talks=talks, user=request.user, description=request.data)
        serializer = self.get_serializer_class()(message)
        return Response(serializer.data)
