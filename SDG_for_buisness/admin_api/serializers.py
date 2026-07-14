from django.contrib.auth.models import User
from rest_framework import serializers

from portal.models import (
    AnswerOption,
    AnswerOptionTranslation,
    GeneralQuestion,
    GeneralQuestionTranslation,
    SDGQuestion,
    SDGQuestionTranslation,
)


SUPPORTED_LANGS = ("ru", "en", "kz")


class AdminUserSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source="is_active", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "active",
            "is_staff",
            "is_superuser",
            "date_joined",
        )


class AdminQuestionUpdateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True)
    texts = serializers.DictField(
        child=serializers.CharField(allow_blank=True),
        required=False,
    )
    translations = serializers.ListField(
        child=serializers.DictField(),
        required=False,
    )
    options = serializers.ListField(
        child=serializers.DictField(),
        required=False,
    )

    def _normalize_texts(self):
        texts = self.validated_data.get("texts") or {}

        for item in self.validated_data.get("translations") or []:
            lang = item.get("language")
            if lang in SUPPORTED_LANGS:
                texts[lang] = item.get("text", "")

        return {
            lang: str(texts.get(lang, "")).strip()
            for lang in SUPPORTED_LANGS
        }

    def _update_question_translations(self, question, translation_model, relation_field):
        texts = self._normalize_texts()
        fallback_text = (
            str(self.validated_data.get("text", "")).strip()
            or texts.get("ru")
            or texts.get("en")
            or texts.get("kz")
        )

        if fallback_text:
            question.text = fallback_text
            question.save(update_fields=["text"])

        for lang, text in texts.items():
            if text:
                translation_model.objects.update_or_create(
                    **{relation_field: question, "language": lang},
                    defaults={"text": text},
                )

    def _update_answer_options(self):
        for option_payload in self.validated_data.get("options") or []:
            option_id = option_payload.get("id")
            text = str(option_payload.get("text", "")).strip()

            if not option_id or not text:
                continue

            option = AnswerOption.objects.filter(id=option_id).first()
            if not option:
                continue

            option.text = text
            option.save(update_fields=["text"])
            AnswerOptionTranslation.objects.update_or_create(
                answer_option=option,
                language="ru",
                defaults={"text": text},
            )

    def update_general_question(self, question):
        self._update_question_translations(
            question=question,
            translation_model=GeneralQuestionTranslation,
            relation_field="question",
        )
        self._update_answer_options()
        return question

    def update_sdg_question(self, question):
        self._update_question_translations(
            question=question,
            translation_model=SDGQuestionTranslation,
            relation_field="question",
        )
        return question


class AdminQuestionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    texts = serializers.SerializerMethodField()
    sdg_number = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    def get_texts(self, obj):
        translations = {item.language: item.text for item in obj.translations.all()}
        return {lang: translations.get(lang, "") for lang in SUPPORTED_LANGS}

    def get_sdg_number(self, obj):
        goal = getattr(obj, "sdg_goal", None)
        return goal.number if goal else None

    def get_weight(self, obj):
        return None

    def get_answers(self, obj):
        options = getattr(obj, "answer_options", None)
        if options is None:
            return []

        return [
            {
                "id": option.id,
                "text": option.text,
            }
            for option in options.all()
        ]
