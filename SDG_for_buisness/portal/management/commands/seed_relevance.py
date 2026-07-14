from django.core.management.base import BaseCommand
from django.db import transaction

from portal.models import AnswerOption, RelevanceRule, SDGGoal


VALID_GOAL_NUMBERS = {1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17}


RULES_BY_ANSWER_ID = {
    1: ([1, 3, 8, 10, 12], [4, 5, 6, 7, 9, 13, 15, 16, 17]),
    2: ([1, 3, 8, 10, 12], [4, 5, 6, 7, 9, 13, 15, 16, 17]),
    3: ([1, 3, 4, 5, 8, 10, 12], [6, 7, 9, 13, 15, 17]),
    4: ([1, 3, 4, 5, 6, 7, 8, 10, 12, 13, 15, 16], [9, 17]),
    5: ([1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17], []),
    6: ([1, 3, 8, 10, 12], [4, 6, 7, 9, 13, 15, 16, 17]),
    7: ([3, 6, 7, 8, 9, 12, 13, 15], [4, 5, 10, 16, 17]),
    8: ([1, 3, 4, 5, 8, 10, 12, 16, 17], [6, 7, 9, 13, 15]),
    9: ([4, 5, 8, 9, 10, 16, 17], [1, 3, 6, 7, 12, 13, 15]),
    10: ([1, 3, 5, 6, 7, 8, 10, 12, 13, 15], [4, 9, 16, 17]),
    11: ([1, 3, 6, 7, 8, 9, 10, 12, 13, 15], [4, 17]),
    12: ([1, 3, 5, 7, 8, 9, 12], [4, 6, 10, 13, 15, 16, 17]),
    13: ([1, 3, 4, 5, 8, 10, 12, 16], [6, 7, 9, 13, 15, 17]),
    14: ([1, 3, 4, 5, 8, 10, 16], [6, 7, 9, 12, 13, 15, 17]),
    15: ([1, 3, 4, 5, 8, 10, 17], [6, 7, 9, 12, 13, 15, 16]),
    16: ([1, 4, 5, 6, 7, 8, 10, 12, 13], [3, 9, 16, 17]),
    17: ([1, 3, 4, 5, 8, 10, 16, 17], [6, 7, 9, 12, 13, 15]),
    18: ([1, 3, 4, 5, 8, 10, 16, 17], [6, 7, 9, 12, 13, 15]),
    19: ([1, 3, 4, 5, 8, 10, 16, 17], [6, 7, 9, 12, 13, 15]),
    20: ([1, 3, 5], []),
    21: ([1, 3, 5, 8, 10], [7, 9, 12, 13, 15, 16, 17]),
    22: ([1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15], []),
    23: ([1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17], []),
    24: ([1, 3, 5, 8, 10, 12, 16, 17], [4, 6, 7, 9, 13, 15]),
    25: ([1, 3, 5, 8, 10, 12, 16, 17], [4, 6, 7, 9, 13, 15]),
    26: ([1, 3, 5, 6, 7, 8, 10, 12, 13], [4, 16, 17]),
    27: ([1, 3, 4, 5, 6, 7, 8, 10, 12, 13, 15, 16, 17], [9]),
    28: ([1, 3, 5], []),
    29: ([3, 6, 7, 8, 9, 12, 13, 15], [4, 5, 10, 16, 17]),
    30: ([1, 3, 5, 6, 7, 8, 12, 13], [9, 15, 16, 17]),
    31: ([1, 3, 8, 12], [6, 7, 9, 13, 15]),
    32: ([1, 3, 4, 5, 8], [6, 7, 9, 12, 13, 15]),
    33: ([4, 5, 8, 9, 16], [1, 3, 6, 7, 12, 13, 15]),
    34: ([6, 7, 8, 9, 12, 13, 15], [4, 5, 10, 16, 17]),
    35: ([6, 7, 12, 13, 15], [1, 3, 5, 8, 9, 10, 16, 17]),
    36: ([6, 12], [1, 3, 5, 7, 8, 9, 10, 13, 15, 16, 17]),
    37: ([12], [1, 3, 5, 6, 7, 8, 9, 10, 13, 15, 16, 17]),
    38: ([], [6, 7, 12, 13, 15]),
    39: ([9, 16, 17], [1, 3, 5, 6, 7, 8, 10, 12, 13, 15]),
    40: ([8, 10], [1, 5, 6, 7, 9, 12, 13, 15]),
    41: ([1, 3, 10], [6, 7, 8, 9, 12, 13, 15, 16, 17]),
    42: ([8, 10, 17], [1, 3, 5, 6, 7, 9, 12, 13, 15, 16]),
    43: ([], [1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17]),
    44: ([1, 3, 5, 8, 12, 17], [10, 16]),
    45: ([8, 9, 12, 16, 17], [1, 3, 5, 7, 10]),
    46: ([8, 9, 16, 17], [1, 3, 4, 5, 6, 7, 10, 12, 13, 15]),
    47: ([10, 16, 17], [1, 3, 4, 5, 6, 7, 8, 9, 12, 13, 15]),
    48: ([1, 3, 5, 8, 10, 12, 17], [4, 6, 7, 9, 13, 15, 16]),
    49: ([1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17], []),
    50: ([1, 3, 4, 5, 8, 10, 16], [6, 7, 9, 12, 13, 15, 17]),
    51: ([6, 7, 8, 12, 13, 15], [1, 3, 4, 5, 9, 10, 16, 17]),
    52: ([1, 3, 4, 5, 8, 10, 12], [6, 7, 9, 13, 15, 16, 17]),
    53: ([4, 5, 8, 9, 16], [6, 7, 10, 12, 13, 15]),
    54: ([1, 3, 5, 8, 10], [4, 9, 16, 17]),
    55: ([1, 3, 5, 8, 10, 12, 17], [16]),
    56: ([1, 3, 4, 5, 8, 10, 12], [6, 7, 9, 13, 15, 16, 17]),
    57: ([1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17], []),
    58: ([], [1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17]),
    59: ([4, 5, 8, 9, 10, 16, 17], [1, 3, 6, 7, 12, 13, 15]),
    60: ([1, 3, 4, 5, 8, 9, 10, 12, 16, 17], [6, 7, 13, 15]),
    61: ([1, 3, 4, 5, 8, 9, 10, 12, 16], [6, 7, 13, 15]),
    62: ([1, 3, 5, 8, 10, 12], [4, 6, 7, 9, 13, 15, 16, 17]),
    63: ([], [1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17]),
}


STRONG_WEIGHTS_BY_ANSWER_ID = {
    10: {
        6: 4,
        7: 4,
        12: 4,
        13: 4,
        15: 4,
    },
    11: {
        6: 4,
        7: 4,
        9: 4,
        12: 4,
        13: 4,
        15: 4,
    },
    16: {
        6: 4,
        7: 4,
        12: 4,
        13: 4,
    },
    19: {
        4: 4,
    },
    34: {
        6: 4,
        7: 4,
        9: 4,
        12: 4,
        13: 4,
        15: 4,
    },
}


class Command(BaseCommand):
    help = "Seed relevance rules for adaptive survey logic"

    def handle(self, *args, **kwargs):
        answer_ids = set(RULES_BY_ANSWER_ID.keys())
        existing_answers = set(
            AnswerOption.objects.filter(id__in=answer_ids).values_list("id", flat=True)
        )

        missing_answers = sorted(answer_ids - existing_answers)
        if missing_answers:
            self.stdout.write(
                self.style.ERROR(
                    f"Не найдены AnswerOption с id: {', '.join(map(str, missing_answers))}"
                )
            )
            return

        goals_by_number = {
            goal.number: goal.id
            for goal in SDGGoal.objects.filter(number__in=VALID_GOAL_NUMBERS)
        }

        missing_goal_numbers = sorted(VALID_GOAL_NUMBERS - set(goals_by_number.keys()))
        if missing_goal_numbers:
            self.stdout.write(
                self.style.ERROR(
                    f"Не найдены SDGGoal с number: {', '.join(map(str, missing_goal_numbers))}"
                )
            )
            return

        rules_to_create = []
        seen_pairs = set()

        for answer_id, (plus_numbers, minus_numbers) in RULES_BY_ANSWER_ID.items():
            plus_set = set(plus_numbers)
            minus_set = set(minus_numbers) - plus_set
            strong_weights = STRONG_WEIGHTS_BY_ANSWER_ID.get(answer_id, {})

            for goal_number in sorted(plus_set):
                goal_id = goals_by_number[goal_number]
                pair = (answer_id, goal_id)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    rules_to_create.append(
                        RelevanceRule(
                            answer_option_id=answer_id,
                            sdg_goal_id=goal_id,
                            weight=strong_weights.get(goal_number, 2),
                        )
                    )

            for goal_number in sorted(minus_set):
                goal_id = goals_by_number[goal_number]
                pair = (answer_id, goal_id)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    rules_to_create.append(
                        RelevanceRule(answer_option_id=answer_id, sdg_goal_id=goal_id, weight=-3)
                    )

        with transaction.atomic():
            RelevanceRule.objects.all().delete()
            RelevanceRule.objects.bulk_create(rules_to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f"Правила релевантности загружены: {len(rules_to_create)} записей."
            )
        )
