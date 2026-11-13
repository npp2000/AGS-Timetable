import os
import re
import random
from bs4 import BeautifulSoup

# Path to your exported HTML timetable folder
EXPORT_FOLDER = "C:\\FET\\AGS\\timetables\\Primary School-45"

# CSS file name
CSS_FILE_NAME = "style.css"

# Base Google Calendar–style colors
BASE_COLORS = [
    "#d7aefb",  # Purple
    "#aecbfa",  # Blue
    "#fbbc04",  # Yellow
    "#ccff90",  # Green
    "#fdcfe8",  # Pink
    "#f28b82",  # Red
    "#a7ffeb",  # Teal
    "#fff475"   # Light Yellow
]

def generate_color(subject_index):
    """Pick a color from BASE_COLORS or generate random pastel."""
    if subject_index < len(BASE_COLORS):
        return BASE_COLORS[subject_index]
    # Generate random pastel color
    r = random.randint(150, 255)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    return f"rgb({r},{g},{b})"

def process_html_files():
    subjects_found = set()

    # First pass: collect all subjects
    for filename in os.listdir(EXPORT_FOLDER):
        if filename.lower().endswith(".html"):
            file_path = os.path.join(EXPORT_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                for td in soup.find_all("td"):
                    text = td.get_text(strip=True)
                    if text:
                        # Assume subject is first word or line
                        subject_name = text.split("\n")[0].split(" ")[0]
                        subjects_found.add(subject_name.strip())

    # Assign colors dynamically
    subject_color_map = {}
    for idx, subject in enumerate(sorted(subjects_found)):
        subject_color_map[subject] = generate_color(idx)

    # Second pass: update HTML files with classes and CSS link
    for filename in os.listdir(EXPORT_FOLDER):
        if filename.lower().endswith(".html"):
            file_path = os.path.join(EXPORT_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            # Add CSS link if missing
            head = soup.find("head")
            if head and not soup.find("link", href=CSS_FILE_NAME):
                css_link = soup.new_tag("link", rel="stylesheet", href=CSS_FILE_NAME)
                head.append(css_link)

            # Tag cells with subject classes
            for td in soup.find_all("td"):
                text = td.get_text(strip=True)
                for subject in subject_color_map:
                    if re.search(rf"\b{subject}\b", text, re.IGNORECASE):
                        td["class"] = td.get("class", []) + ["subject", subject.lower()]
                        break

            # Save updated HTML
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(soup))

            print(f"Processed: {file_path}")

    # Generate CSS file
    generate_css(subject_color_map)

def generate_css(subject_color_map):
    """Generate Google Calendar–style CSS dynamically."""
    css_content = [
        "body { font-family: 'Roboto', Arial, sans-serif; background-color: #fafafa; color: #202124; margin: 0; padding: 20px; }",
        "table { border-collapse: collapse; width: 100%; background-color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden; }",
        "th { background-color: #f1f3f4; color: #5f6368; padding: 12px; text-align: center; font-weight: 500; font-size: 0.95em; border-bottom: 1px solid #dadce0; }",
        "td { padding: 10px; text-align: center; border-bottom: 1px solid #e0e0e0; vertical-align: middle; }",
        "tr:nth-child(even) { background-color: #f8f9fa; }",
        "tr:hover { background-color: #e8f0fe; }",
        ".teacher { font-size: 0.85em; color: #5f6368; }",
        ".room { font-size: 0.8em; color: #5f6368; }",
        "@media screen and (max-width: 768px) { table, thead, tbody, th, td, tr { display: block; } th { position: sticky; top: 0; background-color: #f1f3f4; } td { border: none; border-bottom: 1px solid #e0e0e0; } }"
    ]

    # Add subject-specific colors
    for subject, color in subject_color_map.items():
        css_content.append(f".subject.{subject.lower()} {{ background-color: {color}; font-weight: 500; padding: 6px; border-radius: 4px; }}")

    # Save CSS file
    css_path = os.path.join(EXPORT_FOLDER, CSS_FILE_NAME)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write("\n".join(css_content))

    print(f"Generated CSS with {len(subject_color_map)} subjects: {css_path}")

if __name__ == "__main__":
    if not os.path.exists(EXPORT_FOLDER):
        print(f"Folder '{EXPORT_FOLDER}' not found.")
    else:
        process_html_files()
