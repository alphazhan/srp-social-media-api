from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load once
_model_id = "KoalaAI/Text-Moderation"
_tokenizer = AutoTokenizer.from_pretrained(_model_id)
_model = AutoModelForSequenceClassification.from_pretrained(_model_id)

# Label-to-category map with descriptions
LABEL_MAP = {
    "S": {
        "category": "Sexual",
        "description": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
    },
    "H": {
        "category": "Hate",
        "description": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
    },
    "V": {
        "category": "Violence",
        "description": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
    },
    "HR": {
        "category": "Harassment",
        "description": "Content that may be used to torment or annoy individuals in real life, or make harassment more likely to occur.",
    },
    "SH": {
        "category": "Self-harm",
        "description": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
    },
    "S3": {
        "category": "Sexual/Minors",
        "description": "Sexual content that includes an individual who is under 18 years old.",
    },
    "H2": {
        "category": "Hate/Threatening",
        "description": "Hateful content that also includes violence or serious harm towards the targeted group.",
    },
    "V2": {
        "category": "Violence/Graphic",
        "description": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    },
    "OK": {"category": "OK", "description": "Not offensive."},
}


def _moderate_text_raw(text: str) -> list[dict]:
    """
    Returns a list of all moderation labels with their scores.
    Example:
    [
        {"label": "H", "score": 0.87},
        {"label": "OK", "score": 0.10},
        ...
    ]
    """
    inputs = _tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = _model(**inputs).logits
    probs = torch.softmax(logits, dim=-1).squeeze()
    id2label = _model.config.id2label

    results = [
        {"label": id2label[i], "score": float(probs[i])} for i in range(len(probs))
    ]
    return sorted(results, key=lambda x: x["score"], reverse=True)


def moderate_text(text: str) -> dict:
    """
    Returns the most likely moderation category and its description.
    Example:
    {
        "category": "Hate",
        "description": "Content that expresses, incites, or promotes hate..."
    }
    """
    results = _moderate_text_raw(text)
    top = results[0]
    mapped = LABEL_MAP.get(
        top["label"],
        {"category": "Unknown", "description": "No description available."},
    )
    return {"category": mapped["category"], "description": mapped["description"]}


# Example usage
if __name__ == "__main__":
    # OR: You should just disappear from this world.
    text = "I'm going to find you and make you pay."

    print(moderate_text(text))  # Clean output
    print()
    print(_moderate_text_raw(text))  # Full raw scores
