from transformers import pipeline

# Core pipeline using pretrained language ID model
_model_id = "juliensimon/xlm-v-base-language-id"
_classifier = pipeline("text-classification", model=_model_id)


def _detect_language_raw(text: str) -> list[dict]:
    """
    Returns full language classification output with label and confidence score.
    Example:
    [{'label': 'Kazakh', 'score': 0.938}]
    """
    return _classifier(text)


def detect_language(text: str) -> str:
    """
    Returns only the detected language label as a string.
    Example: 'Kazakh'
    """
    result = _detect_language_raw(text)
    return result[0]["label"] if result else "Unknown"


# Example usage
if __name__ == "__main__":
    text = "Қалайсың"
    print(detect_language(text))  # Kazakh
    print(_detect_language_raw(text))  # [{'label': 'Kazakh', 'score': ...}]
