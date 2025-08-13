import base64, json, mimetypes, os, re, sys
from bs4 import BeautifulSoup

HTML_PATH = os.path.join(
    os.getcwd(),
    'uncertainty_google_forms',
    'Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms.html'
)
RES_DIR = os.path.join(
    os.getcwd(),
    'uncertainty_google_forms',
    'Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms_files'
)

SECTION_TITLES = [
    'An Introduction to Error Analysis',
    'Precision and Accuracy',
    'Uncertainty as a range of believable values',
    'Estimating uncertainty for one measurement',
    'Range method: Estimating uncertainty with the range of multiple measurements',
    'Standard deviation and the Gaussian distribution',
    'Standard Form',
]

if not os.path.exists(HTML_PATH):
    print('HTML not found', file=sys.stderr)
    sys.exit(1)

raw = open(HTML_PATH, 'r', encoding='utf-8', errors='ignore').read()

# Locate title anchors
positions = []
for title in SECTION_TITLES:
    idx = raw.find(title)
    positions.append(idx)

sections = []
for i, title in enumerate(SECTION_TITLES):
    start = positions[i]
    if start == -1:
        sections.append({'title': title, 'html': ''})
        continue
    # end at next found title or end of file
    next_positions = [p for p in positions[i+1:] if p != -1]
    end = min(next_positions) if next_positions else len(raw)
    chunk = raw[start:end]

    # Strip <script> tags and external links
    soup = BeautifulSoup(chunk, 'lxml')
    for tag in soup(['script', 'style']):
        tag.decompose()

    # Inline local images as data URIs
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if not src:
            continue
        if src.startswith('http'):  # leave remote images
            continue
        # Normalize relative path
        rel = src
        # Some exports may use './folder/file' or 'folder/file'
        rel = rel.lstrip('./')
        abs_path = os.path.join(os.path.dirname(HTML_PATH), rel)
        if not os.path.exists(abs_path):
            # try within RES_DIR directly
            abs_path = os.path.join(RES_DIR, os.path.basename(rel))
        if os.path.exists(abs_path):
            mime, _ = mimetypes.guess_type(abs_path)
            if not mime:
                mime = 'application/octet-stream'
            with open(abs_path, 'rb') as f:
                data = base64.b64encode(f.read()).decode('ascii')
            img['src'] = f'data:{mime};base64,{data}'
        else:
            # if missing, drop the img to avoid broken refs
            img.decompose()

    # Remove a few heavy containers but keep inner text
    # (Already decomposed scripts/styles; rest should be fine)

    cleaned_html = str(soup)
    sections.append({'title': title, 'html': cleaned_html})

os.makedirs('data', exist_ok=True)
OUT = os.path.join('data', 'uncertainty_sections_html.json')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({'sections': sections}, f, ensure_ascii=False, indent=2)
print(f'Wrote {OUT} with {len(sections)} HTML chunks')
