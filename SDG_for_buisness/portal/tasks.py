import requests

from celery import shared_task
from django.conf import settings

from .serializers import RecommendationRootSerializer

from .models import QuestionnaireSubmission


@shared_task(
    bind=True,
    max_retries=3
)
def process_questionnaire(
    self,
    submission_id,
    payload,
    language
):
    submission = QuestionnaireSubmission.objects.get(
        id=submission_id
    )

    recommendation_url = (
        f'{settings.RECOMMENDATION_SERVICE_URL}'
        f'/api/Unity/GetResults'
    )

    try:
        response = requests.post(
            recommendation_url,
            params={
                'language': language
            },
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        data['news'] = [
            {
                'news_title': x.get('newsTitle'),
                'pestel_type': x.get('pestelType'),
                'impact_type': x.get('impactType'),
                'impact_strength': x.get('impactStrength'),
                'url': x.get('url'),
                'title_en': x.get('titleEn'),
                'title_kz': x.get('titleKz'),
                'sdg': x.get('sdg'),
            }
            for x in data['news']
        ]

        data['recommendedSdgs'] = [
            {
                'sdg_number': x.get('sdgNumber'),
                'current_value': x.get('currentValue'),
                'recommended_value': x.get('recommendedValue'),
                'delta': x.get('delta'),
            }
            for x in data['recommendedSdgs']
        ]

        data['chart']['series'] = [
            {
                'points': x.get('points'),
                'start_value': x.get('startValue'),
                'label': x.get('label'),
                'scenario': x.get('scenario'),
                'sdg_code': x.get('sdgCode'),
            }
            for x in data['chart']['series']
        ]

        serializer = RecommendationRootSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        submission.status = 'completed'

        submission.save(
            update_fields=['status']
        )

    except requests.RequestException as exc:

        if self.request.retries >= self.max_retries:

            submission.status = 'failed'

            submission.save(
                update_fields=['status']
            )

            raise exc

        raise self.retry(
            exc=exc,
            countdown=10
        )