import json

def normalize_adaptive_payload(request):
    data = request.data

    if isinstance(data, dict) and "answers" in data:
        answers = data.get("answers")
        if isinstance(answers, str):
            try:
                answers = json.loads(answers)
            except json.JSONDecodeError:
                pass
        return {"answers": answers}

    if hasattr(data, "getlist"):
        answers = data.getlist("answers")
        if not answers:
            answers = data.getlist("answers[]")
        if answers:
            return {"answers": answers}

    raw_body = request.body.decode("utf-8").strip() if request.body else ""
    if raw_body:
        try:
            parsed = json.loads(raw_body)
        except json.JSONDecodeError:
            parsed = None

        if isinstance(parsed, dict):
            if "answers" in parsed:
                return {"answers": parsed["answers"]}
            if "answers[]" in parsed:
                return {"answers": parsed["answers[]"]}

    return {}

