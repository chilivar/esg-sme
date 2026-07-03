from django.urls import path

from .views import (
    AdminGeneralQuestionAPIView,
    AdminSDGQuestionAPIView,
    AdminUsersAPIView,
)

urlpatterns = [
    path("users/", AdminUsersAPIView.as_view(), name="admin-users"),
    path(
        "questions/general/<int:question_id>/",
        AdminGeneralQuestionAPIView.as_view(),
        name="admin-general-question",
    ),
    path(
        "questions/sdg/<int:question_id>/",
        AdminSDGQuestionAPIView.as_view(),
        name="admin-sdg-question",
    ),
]
