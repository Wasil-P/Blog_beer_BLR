from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

# talks/
"""categories_all: адлюстраванне усіх катэгорый для форума
    category_show_talks: адлюстраванне канкрэтнай катэгорыі з пытаннямі
    talk_show: адлюстраванне канкрэтнага пытаннямя з паведамленнямі
    
    categories_all: display all categories for the forum
    category_show_talks: display a specific category with questions
    talk_show: display specific questions with messages"""
urlpatterns = [
    path("", cache_page(60)(views.CategoryTalksList.as_view()), name="categories_all"),
    path("<int:category_id>", cache_page(60)(views.OneCategoryTalks.as_view()), name="category_show_talks"),
    path("<int:category_id>/create/", views.TalkCreate.as_view(), name="talk_create"),
    path("<int:category_id>/<int:talk_id>/edit/", views.TalkEdit.as_view(), name="talk_edit"),
    path("<int:category_id>/<int:talk_id>", views.OneTalkShow.as_view(), name="talk_show"),
    path("<int:category_id>/<int:talk_id>/create/", views.MessageCreate.as_view(), name="message_create")
]