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
    # path("category/", name="category_show"),
    # path("category/<int:talks_id>", name="question_show")
]