from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from portal.models import GeneralQuestion, SDGQuestion
from .serializers import (
    AdminQuestionResponseSerializer,
    AdminQuestionUpdateSerializer,
    AdminUserSerializer,
)


class AdminUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.order_by("id")
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)


class AdminGeneralQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, question_id):
        question = get_object_or_404(
            GeneralQuestion.objects.prefetch_related(
                "translations",
                "answer_options",
            ),
            id=question_id,
        )
        serializer = AdminQuestionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.update_general_question(question)
        response = AdminQuestionResponseSerializer(question)
        return Response(response.data)


class AdminSDGQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, question_id):
        question = get_object_or_404(
            SDGQuestion.objects.select_related("sdg_goal").prefetch_related("translations"),
            id=question_id,
        )
        serializer = AdminQuestionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.update_sdg_question(question)
        response = AdminQuestionResponseSerializer(question)
        return Response(response.data)
