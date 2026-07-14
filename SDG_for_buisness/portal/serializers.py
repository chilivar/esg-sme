# import transaction
from django.db import transaction
from rest_framework import serializers
from .models import *


class LocalizedTextMixin:
    def _get_requested_language(self):
        request = self.context.get("request")
        if not request:
            return None

        query_params = getattr(request, "query_params", request.GET)
        lang = query_params.get("lang")
        return lang.lower() if isinstance(lang, str) and lang.strip() else None

    def _get_localized_text(self, obj):
        lang = self._get_requested_language()
        if not lang:
            return obj.text

        for translation in obj.translations.all():
            if translation.language == lang:
                return translation.text

        return obj.text

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if self._get_requested_language():
            data.pop("translations", None)

        return data


class AnswerOptionTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptionTranslation
        fields = ['language', 'text']


class AnswerOptionSerializer(LocalizedTextMixin, serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    translations = AnswerOptionTranslationSerializer(many=True, read_only=True)

    def get_text(self, obj):
        return self._get_localized_text(obj)

    class Meta:
        model = AnswerOption
        fields = ["id", "text", "translations"]


class SDGQuestionTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDGQuestionTranslation
        fields = ['language', 'text']

class GeneralQuestionTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralQuestionTranslation
        fields = ['language', 'text']

class SDGQuestionSerializer(LocalizedTextMixin, serializers.ModelSerializer):
    QUESTION_WEIGHTS = [0.30, 0.25, 0.25, 0.20]

    text = serializers.SerializerMethodField()
    translations = SDGQuestionTranslationSerializer(many=True, read_only=True)
    sdg_number = serializers.IntegerField(source="sdg_goal.number", read_only=True)
    weight = serializers.SerializerMethodField()

    def get_text(self, obj):
        return self._get_localized_text(obj)

    def get_weight(self, obj):
        questions = list(obj.sdg_goal.questions.filter(active=True).order_by("id"))

        try:
            index = next(i for i, question in enumerate(questions) if question.id == obj.id)
        except StopIteration:
            return 0

        return self.QUESTION_WEIGHTS[index] if index < len(self.QUESTION_WEIGHTS) else 0

    class Meta:
        model = SDGQuestion
        fields = ["id", "text", "translations", "sdg_number", "weight"]

class GeneralQuestionSerializer(LocalizedTextMixin, serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    translations = GeneralQuestionTranslationSerializer(many=True, read_only=True)
    answers = AnswerOptionSerializer(source="answer_options", many=True, read_only=True)

    def get_text(self, obj):
        return self._get_localized_text(obj)

    class Meta:
        model = GeneralQuestion
        fields = ["id", "text", "translations", "active", "answers"]

class SDGGoalSerializer(serializers.ModelSerializer):
    questions = SDGQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = SDGGoal
        fields = ['id', 'number', 'title', 'questions']


# Дима это твое
class QuestionnaireResultsGetSerializer(serializers.Serializer):
    result_id = serializers.IntegerField(required=False)

class AnswerSerializer(serializers.Serializer):
    sdg_number = serializers.IntegerField()
    weight = serializers.FloatField()
    question_text = serializers.CharField()
    answer_text = serializers.CharField()
    score = serializers.IntegerField()


class SurveySubmitSerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
    submitted_at = serializers.DateTimeField()
    answers = AnswerSerializer(many=True)

class AdaptiveSurveyRequestSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )

    def validate_answers(self, value):
        # Preserve order but avoid double counting duplicate answer ids.
        return list(dict.fromkeys(value))


class QuestionnaireAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=SDGQuestion.objects.filter(active=True),
        source='question'
    )

    class Meta:
        model = QuestionnaireAnswer
        fields = (
            'question_id',
            'weight',
            'answer_text',
            'score',
        )


class QuestionnaireSubmissionSerializer(serializers.ModelSerializer):
    answers = QuestionnaireAnswerSerializer(many=True)

    language = serializers.CharField()

    class Meta:
        model = QuestionnaireSubmission
        fields = (
            'submitted_at',
            'language',
            'answers',
        )

    def create(self, validated_data):
        validated_data.pop('language')

        answers_data = validated_data.pop('answers')

        user = self.context['request'].user

        submission = QuestionnaireSubmission.objects.create(
            user=user,
            **validated_data
        )

        answers = [
            QuestionnaireAnswer(
                submission=submission,
                **answer_data
            )
            for answer_data in answers_data
        ]

        QuestionnaireAnswer.objects.bulk_create(answers)

        return submission


class QuestionnaireResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireResult
        fields = (
            # 'company_id',
            'sdg_number',
            'value',
        )

        def create(self, validated_data):
            # request = self.context['request']

            return QuestionnaireResult.objects.create(
                # company_id=request.user.id,
                **validated_data
            )


class QuestionnaireNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireNews
        fields = (
            'news_title',
            'pestel_type',
            'impact_type',
            'impact_strength',
            'url',
            'title_en',
            'title_kz',
            'sdg',
        )


class QuestionnaireRecommendedSDGSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireRecommendedSDG
        fields = (
            'sdg_number',
            'current_value',
            'recommended_value',
            'delta',
        )


class QuestionnaireChartSeriesSerializer(serializers.ModelSerializer):

    points = serializers.ListField(
        child=serializers.FloatField()
    )

    class Meta:
        model = QuestionnaireChartSeries
        fields = (
            'sdg_code',
            'scenario',
            'label',
            'start_value',
            'points',
        )

    def create(self, validated_data):
        points_data = validated_data.pop('points')

        series = QuestionnaireChartSeries.objects.create(
            **validated_data
        )

        QuestionnaireChartPoint.objects.bulk_create([
            QuestionnaireChartPoint(
                series=series,
                value=point
            )
            for point in points_data
        ])

        return series


class QuestionnaireChartSerializer(serializers.ModelSerializer):
    series = QuestionnaireChartSeriesSerializer(many=True)

    class Meta:
        model = QuestionnaireChart
        fields = (
            'labels',
            'series',
        )


class QuestionnaireAnswerResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireAnswerResult
        fields = ('text',)

class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = (
            'category_name',
            'value',
            'sdg_numbers',
        )


class RecommendationRootSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField()

    result = QuestionnaireResultSerializer(many=True)
    news = QuestionnaireNewsSerializer(many=True)
    recommendedSdgs = QuestionnaireRecommendedSDGSerializer(many=True)
    categories = QuestionnaireCategorySerializer(
        many=True
    )

    chart = QuestionnaireChartSerializer()

    answer = serializers.CharField()

    def create(self, validated_data):
        submission_id = validated_data['questionnaire_id']

        results_data = validated_data['result']
        news_data = validated_data['news']
        recommended_data = validated_data['recommendedSdgs']
        chart_data = validated_data['chart']
        answer_text = validated_data['answer']
        categories_data = validated_data['categories']

        from .models import QuestionnaireSubmission

        submission = QuestionnaireSubmission.objects.get(
            id=submission_id
        )

        with transaction.atomic():
            # RESULTS
            QuestionnaireResult.objects.bulk_create([
                QuestionnaireResult(
                    submission=submission,
                    **item
                )
                for item in results_data
            ])

            # NEWS
            QuestionnaireNews.objects.bulk_create([
                QuestionnaireNews(
                    submission=submission,
                    **item
                )
                for item in news_data
            ])

            # RECOMMENDED SDG
            QuestionnaireRecommendedSDG.objects.bulk_create([
                QuestionnaireRecommendedSDG(
                    submission=submission,
                    **item
                )
                for item in recommended_data
            ])

            # CHART
            chart = QuestionnaireChart.objects.create(
                submission=submission,
                labels=chart_data['labels']
            )

            # SERIES + POINTS
            for series in chart_data['series']:
                points_data = series.pop('points')

                s = QuestionnaireChartSeries.objects.create(
                    chart=chart,
                    **series
                )

                QuestionnaireChartPoint.objects.bulk_create([
                    QuestionnaireChartPoint(
                        series=s,
                        value=p
                    )
                    for p in points_data
                ])

            # ANSWER
            QuestionnaireAnswerResult.objects.create(
                submission=submission,
                text=answer_text
            )

            QuestionnaireCategory.objects.bulk_create([
                QuestionnaireCategory(
                    submission=submission,
                    **category
                )
                for category in categories_data
            ])

        return submission


class RecommendationResponseSerializer(
    serializers.ModelSerializer
):
    questionnaire_id = serializers.IntegerField(
        source='id'
    )

    status = models.CharField(
        max_length=20,
    )

    result = QuestionnaireResultSerializer(
        many=True,
        source='results'
    )

    categories = QuestionnaireCategorySerializer(
        many=True
    )

    news = QuestionnaireNewsSerializer(
        many=True
    )

    recommendedSdgs = (
        QuestionnaireRecommendedSDGSerializer(
            many=True,
            source='recommended_sdgs'
        )
    )

    chart = serializers.SerializerMethodField()

    answer = serializers.SerializerMethodField()

    class Meta:
        model = QuestionnaireSubmission

        fields = (
            'questionnaire_id',
            'status',
            'result',
            'categories',
            'news',
            'recommendedSdgs',
            'chart',
            'answer',
        )

    def get_chart(self, obj):

        if not hasattr(obj, 'chart'):
            return None

        chart = obj.chart

        return {
            'labels': chart.labels,
            'series': [
                {
                    'sdgCode': s.sdg_code,
                    'scenario': s.scenario,
                    'label': s.label,
                    'startValue': s.start_value,
                    'points': [
                        p.value
                        for p in s.points.all()
                    ]
                }
                for s in chart.series.all()
            ]
        }

    def get_answer(self, obj):
        if hasattr(obj, 'answer'):
            return obj.answer.text

        return None
