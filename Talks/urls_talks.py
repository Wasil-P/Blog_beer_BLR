from django.urls import path
from . import views

# talks/
"""all_categories: адлюстраванне усіх катэгорый для форума
    category_show: адлюстраванне канкрэтнай катэгорыі з пытаннямі
    question_show: адлюстраванне канкрэтнага пытаннямя з паведамленнямі
    
    all_categories: display all categories for the forum
    category_show: display a specific category with questions
    question_show: display specific questions with messages"""
urlpatterns = [
    path("", views.CategoryTalksList.as_view(), name="categories_all"),
    path("<int:category_id>", views.OneCategoryTalks.as_view(), name="category_show_talks"),
    path("<int:category_id>/create/", views.TalkCreate.as_view(), name="talk_create"),
    path("<int:category_id>/<int:talk_id>/edit/", views.TalkCreate.as_view(), name="talk_edit"),

    path("<int:category_id>/<int:talk_id>", views.OneTalkShow.as_view(), name="talk_show"),
    path("<int:category_id>/<int:talk_id>/create/", views.MessageCreate.as_view(), name="message_create")
]