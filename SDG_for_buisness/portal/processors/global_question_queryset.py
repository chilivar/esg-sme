from .model_interface import ModelInterface
from portal.models import GeneralQuestion, AnswerOption

class GlobalQuestionQuerySet(ModelInterface):
    def __init__(self, lang):
        self.lang = lang

    def get_data(self):
        global_questions = self.get_question()

        questions = self.srtuct_questions(global_questions)

        return questions


    def post_data(self, data, **kwargs):
        pass

    def get_question(self):
        queryset = GeneralQuestion.objects.filter(
            translations__language=self.lang,
            answer_options__translations__language=self.lang
        ).values(
            "id", "text", "active", "translations__text", "answer_options__translations__text"
        )

        return list(queryset)

    def srtuct_questions(self, data):
        result = {}

        for item in data:
            q_id = item["id"]

            if q_id not in result:
                result[q_id] = {
                    "id": q_id,
                    "text": item["translations__text"],
                    "answer_options": []
                }

            result[q_id]["answer_options"].append(
                item["answer_options__translations__text"]
            )

        final_result = list(result.values())

        return final_result
