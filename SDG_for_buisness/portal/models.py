from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

import secrets


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    mailing = models.BooleanField(default=False)


class SDGGoal(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.number} - {self.title}"

    class Meta:
        db_table = 'sdg_goal'


class SDGGoal(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.number} - {self.title}"

    class Meta:
        db_table = 'sdg_goal'


class GeneralQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.text

    class Meta:
        db_table = 'general_question'


class AnswerOption(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)

    question = models.ForeignKey(
        GeneralQuestion,
        on_delete=models.CASCADE,
        related_name="answer_options",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'answer_option'


class AnswerOptionTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    answer_option = models.ForeignKey(
        AnswerOption,
        on_delete=models.CASCADE,
        related_name='translations'
    )
    language = models.CharField(max_length=5)  # 'ru', 'en', 'kz'
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'answer_option_translation'
        unique_together = ('answer_option', 'language')



class SDGQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    active = models.BooleanField(default=True)

    sdg_goal = models.ForeignKey(
        SDGGoal,
        on_delete=models.CASCADE,
        related_name='questions'
    )


    def __str__(self):
        return self.text

    class Meta:
        db_table = 'sdg_question'


class SDGQuestionTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        SDGQuestion,
        on_delete=models.CASCADE,
        related_name='translations'
    )
    language = models.CharField(max_length=5)
    text = models.TextField()

    class Meta:
        db_table = 'sdg_question_translation'
        unique_together = ('question', 'language')


class GeneralQuestionTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        GeneralQuestion,
        on_delete=models.CASCADE,
        related_name='translations'
    )
    language = models.CharField(max_length=5)
    text = models.TextField()

    class Meta:
        db_table = 'general_question_translation'
        unique_together = ('question', 'language')

# -- адаптивность
class RelevanceRule(models.Model):
    answer_option = models.ForeignKey(
        AnswerOption,
        on_delete=models.CASCADE,
        related_name='relevance_rules'
    )

    sdg_goal = models.ForeignKey(
        SDGGoal,
        on_delete=models.CASCADE,
        related_name='relevance_rules'
    )

    weight = models.IntegerField()  # например: +2 или -3

    class Meta:
        db_table = 'relevance_rule'
        unique_together = ('answer_option', 'sdg_goal')


class QuestionnaireSubmission(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaire_submissions')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing'
    )

    submitted_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'questionnaire_submission'


class QuestionnaireAnswer(models.Model):
    submission = models.ForeignKey(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        'SDGQuestion',
        on_delete=models.CASCADE,
        related_name='questionnaire_answers'
    )

    weight = models.FloatField()

    answer_text = models.TextField()

    score = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'questionnaire_answer'


class QuestionnaireResult(models.Model):
    submission = models.ForeignKey(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='results'
    )

    # company_id = models.IntegerField()
    sdg_number = models.IntegerField()
    value = models.FloatField()

    class Meta:
        db_table = 'questionnaire_result'


class QuestionnaireNews(models.Model):
    submission = models.ForeignKey(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='news'
    )

    news_title = models.TextField()
    pestel_type = models.CharField(max_length=50)
    impact_type = models.CharField(max_length=50)
    impact_strength = models.FloatField()

    url = models.URLField()

    title_en = models.TextField()
    title_kz = models.TextField()

    sdg = models.JSONField()

    class Meta:
        db_table = 'questionnaire_news'


class QuestionnaireRecommendedSDG(models.Model):
    submission = models.ForeignKey(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='recommended_sdgs'
    )

    sdg_number = models.IntegerField()

    current_value = models.FloatField()
    recommended_value = models.FloatField()
    delta = models.FloatField()

    class Meta:
        db_table = 'questionnaire_recommended_sdg'


class QuestionnaireChart(models.Model):
    submission = models.OneToOneField(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='chart'
    )

    labels = models.JSONField()

    class Meta:
        db_table = 'questionnaire_chart'

class QuestionnaireChartSeries(models.Model):
    chart = models.ForeignKey(
        QuestionnaireChart,
        on_delete=models.CASCADE,
        related_name='series'
    )

    sdg_code = models.IntegerField()
    scenario = models.IntegerField()
    label = models.CharField(max_length=255)

    start_value = models.FloatField()

    class Meta:
        db_table = 'questionnaire_chart_series'


class QuestionnaireChartPoint(models.Model):
    series = models.ForeignKey(
        QuestionnaireChartSeries,
        on_delete=models.CASCADE,
        related_name='points'
    )

    value = models.FloatField()

    class Meta:
        db_table = 'questionnaire_chart_point'


class QuestionnaireAnswerResult(models.Model):
    submission = models.OneToOneField(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='answer'
    )

    text = models.TextField()

    class Meta:
        db_table = 'questionnaire_answer_result'


class QuestionnaireCategory(models.Model):
    submission = models.ForeignKey(
        QuestionnaireSubmission,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    category_name = models.CharField(
        max_length=128
    )

    value = models.FloatField()

    sdg_numbers = models.JSONField()

    class Meta:
        db_table = 'questionnaire_category'
