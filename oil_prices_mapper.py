import json
import re


def normalize_volume(volume):
    volume = volume.replace(',', '.').replace('л', ' л')
    volume = re.sub(r'\s+', ' ', volume).strip()
    return volume


def extract_brand(name):
    # First capitalized word is usually brand
    words = re.findall(r'\b[А-ЯA-Z][а-яa-zA-Z]+\b', name)
    return words[0].lower() if words else name.lower()


def extract_refinement(name):
    name = name.lower()
    if "нерафінована" in name:
        return "нерафінована"
    elif "рафінована" in name:
        return "рафінована"
    return "рафінована"  # Default assumption


def normalize_record(record):
    brand = extract_brand(record['name'])
    refinement = extract_refinement(record['name'])
    volume = normalize_volume(record['volume'])
    return (brand, refinement, volume)


def merge_data():
    # Load data
    with open('silpo.json', encoding='utf-8') as f1, \
         open('metro.json', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Create maps using normalized keys
    map1 = {normalize_record(item): item['price'] for item in data1}
    map2 = {normalize_record(item): item['price'] for item in data2}

    # Merge unique keys
    all_keys = set(map1.keys()) | set(map2.keys())

    # Create merged output
    merged = []
    for brand, refinement, volume in all_keys:
        merged.append({
            "brand": brand,
            "refinement": refinement,
            "volume": volume,
            "price_file1": map1.get((brand, refinement, volume)),
            "price_file2": map2.get((brand, refinement, volume))
        })

    # Save result
    with open('merged_output.json', 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    merge_data()
    print("Data merged and saved to merged_output.json")
