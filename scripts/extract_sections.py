import json, os, re, sys
from bs4 import BeautifulSoup

HTML_PATH = os.path.join(
    os.getcwd(),
    'uncertainty_google_forms',
    'Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms.html'
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

UI_NOISE = set([
    'Questions', 'Responses', 'Settings', 'Total points', 'Form title', 'Form description',
    '* Indicates required question', 'Question', 'Question Type', 'Answer key', 'Required',
    'Loading image…', 'Loading...', 'Loading…', 'Copy responder link', 'Shorten URL', 'Copy',
    'Published', 'All changes saved in Drive',
])

if not os.path.exists(HTML_PATH):
    print(f'HTML not found: {HTML_PATH}', file=sys.stderr)
    sys.exit(1)

html = open(HTML_PATH, 'r', encoding='utf-8', errors='ignore').read()
soup = BeautifulSoup(html, 'lxml')
text = soup.get_text('\n', strip=True)

# Clean and split into lines
lines = [ln for ln in (ln.strip() for ln in text.split('\n')) if ln]

# Compact duplicate runs and drop obvious UI noise and icon glyph lines
clean_lines = []
for ln in lines:
    if any(sym in ln for sym in ('','','','','','')):
        continue
    if any(noise in ln for noise in UI_NOISE):
        continue
    clean_lines.append(ln)

# Find indices of section titles in order
indices = []
for title in SECTION_TITLES:
    try:
        idx = clean_lines.index(title)
    except ValueError:
        idx = -1
    indices.append(idx)

# Build sections with content spans
sections = []
for i, title in enumerate(SECTION_TITLES):
    start = indices[i]
    if start == -1:
        sections.append({'title': title, 'content': []})
        continue
    end = len(clean_lines)
    for j in range(i+1, len(SECTION_TITLES)):
        if indices[j] != -1:
            end = indices[j]
            break
    content = clean_lines[start+1:end]
    sections.append({'title': title, 'content': content})

os.makedirs('data', exist_ok=True)
OUT = os.path.join('data', 'uncertainty_sections.json')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({'sections': sections}, f, ensure_ascii=False, indent=2)
print(f'Wrote {OUT} with {len(sections)} sections')
