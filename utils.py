import re


def normalize_volume(raw_volume):
    raw_volume = raw_volume.lower().replace(',', '.').strip()
    raw_volume = re.sub(r'\s+', '', raw_volume)

    match = re.match(r'([\d.]+)(м?л)', raw_volume)
    if not match:
        return raw_volume

    amount, unit = match.groups()
    amount = float(amount)

    if unit == 'мл':
        amount /= 1000

    return f"{amount:.2f} л"
