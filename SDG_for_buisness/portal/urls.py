from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import (
    LoginAPIView, signup_view, confirm_email,
    logout_view, RefreshAPIView, SDGGoalListAPIView,
    TestPostView, GeneralQuestionListAPIView,
    AnswerOptionListView, SDGQuestionListView, OrganizationAPIView,
    AdaptiveSurveyAPIView, QuestionnaireSubmissionAPIView, QuestionnaireStatusAPIView,
    QuestionnaireRecommendationAPIView, QuestionnaireAllResultsAPIView, SettingsAPIView, reset_password_view,
    reset_password_confirm_view, new_password_view)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', signup_view, name='signup'),
    path("confirm-email/<uidb64>/<token>/", confirm_email, name="confirm_email"),
    path("reset-password/", reset_password_view, name="reset_password_view"),
    path("reset-password/<uidb64>/<token>/", reset_password_confirm_view, name="reset_password_confirm_view"),
    path("new-password/", new_password_view, name="new_password"),
    path('logout/', logout_view, name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('organization/', OrganizationAPIView.as_view(), name='organization'),
    path('user-settings/', SettingsAPIView.as_view(), name='user-settings'),
    # path('mailing-users/', MailingListAPIView.as_view(), name='organization-settings'),
    path('sdg-goals/', SDGGoalListAPIView.as_view(), name='sdggoal-list'),
    path('test-post/', TestPostView.as_view(), name='test-post'),
    path('general-questions/', GeneralQuestionListAPIView.as_view(), name='general-question-list'),
    path('answer-options/', AnswerOptionListView.as_view()),
    path('sdg-questions/', SDGQuestionListView.as_view()),
    path("adaptive-survey/", AdaptiveSurveyAPIView.as_view()),
    path("questionnaire-result/", QuestionnaireSubmissionAPIView.as_view()),
    path(
        'questionnaire/<int:submission_id>/status/',
        QuestionnaireStatusAPIView.as_view(),
        name='questionnaire-status'
    ),
    path(
        'questionnaire/<int:submission_id>/recommendations/',
        QuestionnaireRecommendationAPIView.as_view(),
        name='questionnaire-recommendations'
    ),

    path('questionnaire/results/', QuestionnaireAllResultsAPIView.as_view()),
]
