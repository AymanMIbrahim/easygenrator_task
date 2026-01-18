import random
import json
import re
from pathlib import Path

def generate_ratings(total_samples, rating_distribution):
    ratings = []

    for rating, ratio in rating_distribution.items():
        count = int(total_samples * ratio)
        ratings.extend([int(rating)] * count)

    while len(ratings) < total_samples:
        ratings.append(random.choice(list(map(int, rating_distribution.keys()))))

    random.shuffle(ratings)
    return ratings


def generate_persona_indexes(total_samples, num_personas):
    personas = []

    base_count = total_samples // num_personas

    for i in range(num_personas):
        personas.extend([i] * base_count)

    while len(personas) < total_samples:
        personas.append(random.randint(0, num_personas - 1))

    random.shuffle(personas)
    return personas

def generate_persona_indexes_with_distribution(total_samples, persona_distribution):
    personas = []

    for idx, ratio in persona_distribution.items():
        count = int(total_samples * ratio)
        personas.extend([int(idx)] * count)

    while len(personas) < total_samples:
        personas.append(random.choice(list(map(int, persona_distribution.keys()))))

    random.shuffle(personas)
    return personas

def json_extract(text):
    cleaned_text = re.sub(r"```json|```", "", text).strip()

    cleaned_text = cleaned_text.replace("\\n", "\n")

    try:
        json_obj = json.loads(cleaned_text)
        return json_obj
    except json.JSONDecodeError as e:
        return None



def save_dict_as_json(data: dict, file_path: str, indent: int = 2, ensure_ascii: bool = False):
    """
    Save a Python dictionary as a JSON file.

    Args:
        data (dict): Dictionary to save
        file_path (str): Output JSON file path
        indent (int): JSON indentation level
        ensure_ascii (bool): Keep unicode characters (False recommended)
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=indent,
            ensure_ascii=ensure_ascii
        )
