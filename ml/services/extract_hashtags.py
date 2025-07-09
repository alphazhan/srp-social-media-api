from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk

# One-time download for sentence tokenization (used internally by some models)
nltk.download("punkt")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-base-tag-generation")
model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-base-tag-generation")


def extract_hashtags(text: str) -> list[str]:
    """
    Generate hashtags from input text using a T5 tag generation model.

    Tags are returned in lowercase with spaces replaced by underscores.
    """
    inputs = tokenizer([text], max_length=512, truncation=True, return_tensors="pt")
    output = model.generate(
        **inputs, num_beams=8, do_sample=True, min_length=10, max_length=64
    )
    decoded = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    tags = set(tag.strip().lower().replace(" ", "_") for tag in decoded.split(","))
    return list(tags)


# Example
if __name__ == "__main__":
    sample_text = """
    Python is a high-level, interpreted, general-purpose programming language. Its
    design philosophy emphasizes code readability with the use of significant
    indentation. Python is dynamically-typed and garbage-collected.
    """
    hashtags = extract_hashtags(sample_text)
    print(hashtags)

    # ['python_programming', 'tech', 'developer', 'software_development',
    # 'python', 'science', 'software_engineering', 'technology', 'engineering',
    # 'programming', 'programming_languages', 'coding', 'computer_science',
    # 'digital', 'software', 'code']
