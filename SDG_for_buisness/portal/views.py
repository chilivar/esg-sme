from django.shortcuts import render, get_object_or_404
from SDG_for_buisness.settings import LIFETIME_ACCESS, LIFETIME_REFRESH
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from portal.tasks import process_questionnaire

from .adaptive_logic import calculate_sdg_scores, get_excluded_goal_ids, get_top_sdg_goals, get_questions_for_goals
from .models import GeneralQuestion, SDGQuestion, AnswerOption
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from portal.processors import UserQuerySet, OrganizationQuerySet

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import generics, status
from .models import SDGGoal, QuestionnaireSubmission
from .serializers import SDGGoalSerializer, GeneralQuestionSerializer, SDGQuestionSerializer, AnswerOptionSerializer, \
     AdaptiveSurveyRequestSerializer, QuestionnaireSubmissionSerializer, RecommendationResponseSerializer

from .utils.confirmation_email import send_confirmation_email
from .utils.exeptions import EmailSendingException, UserExistsException, InvalidTokenException
from .utils.normalize_payload import normalize_adaptive_payload
from .utils.reset_password import reset_password_request
from .utils.reset_password_confirm import reset_password_confirm

DEBUG = not settings.DEBUG


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    data = request.data
    try:
        user = UserQuerySet().post_data(data)
    except UserExistsException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        link = send_confirmation_email(request, user)
    except EmailSendingException:
        return Response(
            {
                "error": "Failed to send confirmation email"
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    response = Response(
        {"message": "Check your email to confirm account"},
        status=status.HTTP_201_CREATED
    )

    return response

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request):
    try:
        link = reset_password_request(
            request,
            request.data
        )

        return Response(
            {
                "message":
                "If account exists, email was sent"
            },
            status=status.HTTP_200_OK
        )

    except EmailSendingException as exc:
        return Response(
            {
                "error": str(exc)
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    except Exception as exc:
        return Response(
            {
                "error": str(exc)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm_view(request, uidb64, token):
    try:
        reset_password_confirm(request.data, uidb64, token)

        return Response(
            {
                "message":
                    "Password changed"
            }
        )

    except InvalidTokenException:
        return Response(
            {
                "error":
                    "Invalid or expired link"
            },
            status=400
        )

@api_view(['POST'])
@permission_classes([(IsAuthenticated)])
def new_password_view(request):
    try:
        user = UserQuerySet().patch_password(data=request.data, username= request.user.username)

        return Response(
            {
                "message":
                    "Password changed"
            }
        )

    except Exception as e:
        return Response(
            {
                "error": e
            },
            status=400
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)

    except Exception:
        return Response({"error": "Invalid link"}, status=400)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Email confirmed successfully"}, status=200)

    return Response({"error": "Invalid or expired token"}, status=400)

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.COOKIES.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        pass

    response = Response({"message": "Logged out"}, status=200)
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    return response


class LoginAPIView(APIView):

    permission_classes = []

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        print(username, password)

        user_obj = User.objects.filter(email=username).first()

        print(user_obj)

        if user_obj:
            user = authenticate(username=user_obj.username, password=password)
        else:
            user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "User not found", "user": user_obj.username, "mail": user_obj.email}, status=status.HTTP_400_BAD_REQUEST)


        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        response = Response({"message": "Success"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access',
            value=str(access),
            httponly=False,
            secure=DEBUG,
            samesite='Lax',
            max_age=LIFETIME_ACCESS
        )
        response.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            secure=DEBUG,
            samesite='Lax',
            max_age=LIFETIME_REFRESH
        )

        return response


class RefreshAPIView(APIView):

    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            return Response({'error': 'No refresh token'}, status=400)

        refresh = RefreshToken(refresh_token)
        access = refresh.access_token
        response = Response({"message": 'refreshed'})

        response.set_cookie(
            key='access',
            value=str(access),
            httponly=False,
            secure=DEBUG,
            samesite='Lax',
            max_age=LIFETIME_ACCESS
        )

        return response


class OrganizationAPIView(APIView):
    qs = OrganizationQuerySet()
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = self.qs.get_data(user=request.user)
            return Response(list(data), status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data

        try:
            update_data = self.qs.put_data(data, user=request.user)
        except Exception:
            return Response({'error': 'Invalid data'}, status=400)

        return Response({'message': f'success, {update_data}'}, status=200)


class SettingsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        settings = OrganizationQuerySet().get_settings_data(user=request.user)

        return Response(settings, status=200)

    def patch(self, request):
        data = request.data

        change_settings = OrganizationQuerySet().patch_data(data, user=request.user)

        return Response("Success", status=200)


class SDGGoalListAPIView(generics.ListAPIView):
    queryset = SDGGoal.objects.prefetch_related("questions__translations").all()
    serializer_class = SDGGoalSerializer


# Общие вопросы
class GeneralQuestionListAPIView(APIView):
    def get(self, request):
        questions = (
            GeneralQuestion.objects.filter(active=True)
            .prefetch_related("translations", "answer_options__translations")
            .order_by("id")
        )

        serializer = GeneralQuestionSerializer(
            questions,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class AnswerOptionListView(generics.ListAPIView):
    queryset = AnswerOption.objects.prefetch_related('translations').all()
    serializer_class = AnswerOptionSerializer


class SDGQuestionListView(generics.ListAPIView):
    queryset = (
        SDGQuestion.objects.filter(active=True)
        .select_related("sdg_goal")
        .prefetch_related("translations")
        .order_by("sdg_goal_id", "id")
    )
    serializer_class = SDGQuestionSerializer


class TestPostView(APIView):
    pass
    # def get(self, request):
    #     data = request.query_params
    #
    #     lang = request.query_params.get("lang", "ru")
    #
    #     result = GlobalQuestionQuerySet(lang).get_data()
    #     return Response(result, status=200)
    #
    # def post(self, request):
    #     # Просто тест — выводим, что пришло в запросе
    #     data = request.data
    #     print("Получено из Postman:", data)
    #     return Response({"status": "ok"}, status=status.HTTP_200_OK)


class AdaptiveSurveyAPIView(APIView):
    def post(self, request):
        normalized_payload = normalize_adaptive_payload(request)
        request_serializer = AdaptiveSurveyRequestSerializer(data=normalized_payload)
        request_serializer.is_valid(raise_exception=True)

        answer_ids = request_serializer.validated_data["answers"]

        scores = calculate_sdg_scores(answer_ids)
        excluded_goal_ids = get_excluded_goal_ids(answer_ids)
        scores = {
            goal_id: score
            for goal_id, score in scores.items()
            if goal_id not in excluded_goal_ids
        }
        goal_entries = get_top_sdg_goals(scores)
        questions_by_goal = get_questions_for_goals(goal_entries)

        response = []

        for entry in goal_entries:
            goal = entry["goal"]
            response.append(
                {
                    "goal_id": goal.id,
                    "goal_number": goal.number,
                    "goal_title": goal.title,
                    "score": entry["score"],
                    "questions": SDGQuestionSerializer(
                        questions_by_goal.get(goal.id, []),
                        many=True,
                        context={"request": request},
                    ).data,
                }
            )

        return Response(response)


class QuestionnaireSubmissionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestionnaireSubmissionSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        submission = serializer.save()

        payload = {
            **request.data,
            'questionnaire_id': submission.id
        }

        process_questionnaire.delay(
            submission.id,
            payload,
            request.data.get('language', 'ru')
        )

        return Response(
            {
                'submission_id': submission.id,
                'status': submission.status
            },
            status=status.HTTP_202_ACCEPTED
        )


class QuestionnaireStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id):
        submission = QuestionnaireSubmission.objects.get(
            id=submission_id,
            user=request.user
        )

        return Response({
            'submission_id': submission.id,
            'status': submission.status
        })


class QuestionnaireRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id):

        submission = get_object_or_404(
            QuestionnaireSubmission.objects.prefetch_related(
                'results',
                'categories',
                'news',
                'recommended_sdgs',
                'chart__series__points',
                'chart__series',
            ).select_related(
                'chart',
                'answer',
            ),
            id=submission_id,
            user=request.user
        )

        serializer = RecommendationResponseSerializer(submission)

        return Response(serializer.data)


class QuestionnaireAllResultsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        submissions = (
            QuestionnaireSubmission.objects
            .prefetch_related(
                'results',
                'categories',
                'news',
                'recommended_sdgs',
                'chart__series__points',
                'chart__series',
            )
            .select_related(
                'chart',
                'answer',
            )
            .filter(user=request.user)
            .order_by('-submitted_at')
        )

        serializer = RecommendationResponseSerializer(submissions, many=True)

        return Response(serializer.data)