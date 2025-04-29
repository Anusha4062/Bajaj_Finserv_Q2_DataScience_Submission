import re

# Extraction function
def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Parsing function
def parse_lab_report(text: str):
    # Regular expression pattern to match lab test format
    lab_test_pattern = r"([A-Za-z\s\(\)]+)\s+([\d\.]+)\s+(\d+\.\d+\s*-\s*\d+\.\d+)"
    matches = re.findall(lab_test_pattern, text)
    
    lab_tests = []
    for match in matches:
        test_name, test_value, reference_range = match
        lab_tests.append({
            "test_name": test_name.strip(),
            "test_value": test_value.strip(),
            "bio_reference_range": reference_range.strip()
        })
    return lab_tests

# Out of range check function
def is_test_out_of_range(test_value: float, reference_range: str) -> bool:
    min_range, max_range = reference_range.split('-')
    min_range = float(min_range.strip())
    max_range = float(max_range.strip())
    return not (min_range <= test_value <= max_range)
