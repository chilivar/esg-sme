from collections import defaultdict

from portal.models import RelevanceRule, SDGGoal, SDGQuestion


EXCLUDED_GOAL_NUMBERS_BY_ANSWER_ID = {
    1: {5},  # До 5 сотрудников
    2: {5},  # 6–10 сотрудников
}


def calculate_sdg_scores(answer_option_ids):
    if not answer_option_ids:
        return {}

    scores = defaultdict(int)

    rules = RelevanceRule.objects.filter(
        answer_option_id__in=answer_option_ids
    ).only("sdg_goal_id", "weight")

    for rule in rules:
        scores[rule.sdg_goal_id] += rule.weight

    return dict(scores)


def get_excluded_goal_ids(answer_option_ids):
    excluded_goal_numbers = set()

    for answer_id in answer_option_ids:
        excluded_goal_numbers.update(EXCLUDED_GOAL_NUMBERS_BY_ANSWER_ID.get(answer_id, set()))

    if not excluded_goal_numbers:
        return set()

    return set(
        SDGGoal.objects.filter(number__in=excluded_goal_numbers).values_list("id", flat=True)
    )


def get_top_sdg_goals(scores, min_goals=5, max_goals=10):
    if not scores:
        return []

    ranked_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    positive_scores = [item for item in ranked_scores if item[1] > 0]

    selected_scores = positive_scores if len(positive_scores) >= min_goals else ranked_scores[:min_goals]
    selected_scores = selected_scores[:max_goals]

    goal_ids = [goal_id for goal_id, _score in selected_scores]
    goals_by_id = SDGGoal.objects.in_bulk(goal_ids)

    return [
        {"goal": goals_by_id[goal_id], "score": score}
        for goal_id, score in selected_scores
        if goal_id in goals_by_id
    ]


def get_questions_for_goals(goal_entries, limit_per_goal=4):
    goal_ids = [entry["goal"].id for entry in goal_entries]
    if not goal_ids:
        return {}

    questions = (
        SDGQuestion.objects.filter(sdg_goal_id__in=goal_ids, active=True)
        .select_related("sdg_goal")
        .prefetch_related("translations")
        .order_by("sdg_goal_id", "id")
    )

    grouped = defaultdict(list)

    for question in questions:
        if len(grouped[question.sdg_goal_id]) < limit_per_goal:
            grouped[question.sdg_goal_id].append(question)

    return {goal_id: grouped.get(goal_id, []) for goal_id in goal_ids}
