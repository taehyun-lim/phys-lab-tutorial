import json, re, sys, os
from bs4 import BeautifulSoup

HTML_PATH = os.path.join(
    os.getcwd(),
    'uncertainty_google_forms',
    'Uncertainty Intro Tutorial [For Physics 100_200 lab] - Google Forms.html'
)

if not os.path.exists(HTML_PATH):
    print(f'HTML not found: {HTML_PATH}', file=sys.stderr)
    sys.exit(1)

html = open(HTML_PATH, 'r', encoding='utf-8', errors='ignore').read()
soup = BeautifulSoup(html, 'lxml')

# Title
page_title = soup.title.get_text(strip=True) if soup.title else ''

# Try to capture visible header/description if present
header_desc = ''
meta_desc = soup.find('meta', attrs={'property':'og:description'})
if meta_desc and meta_desc.get('content'):
    header_desc = meta_desc['content']

# Questions are complex in Forms HTML. We'll heuristically extract blocks containing
# question text and any associated explanatory text. This won't capture every styling nuance,
# but it will preserve exact text content in order.

questions = []

# A broad search: look for divs that resemble question containers by presence of required markers or labels
for div in soup.find_all('div'):
    text = div.get_text('\n', strip=True)
    if not text:
        continue
    if ('* Indicates required question' in text):
        continue
    # Heuristics: keep blocks with question-like punctuation or key phrases
    if (re.search(r'[?]$', text)
        or '±' in text
        or 'standard form' in text.lower()
        or 'believable' in text.lower()
        or 'A student measures the voltage' in text
        or 'Total points' in text
        or 'An Introduction to Error Analysis' in text):
        # Filter very long or chrome UI blocks
        if len(text) > 1200:
            continue
        # Deduplicate near-duplicates
        if questions and text == questions[-1].get('raw_text'):
            continue
        questions.append({'raw_text': text})

# Post-filter: keep only unique texts preserving order
seen = set()
unique_questions = []
for q in questions:
    t = q['raw_text']
    if t not in seen:
        seen.add(t)
        unique_questions.append(q)

out = {
    'page_title': page_title,
    'header_description': header_desc,
    'questions': unique_questions,
}

os.makedirs('data', exist_ok=True)
OUT_PATH = os.path.join('data', 'uncertainty_quiz.json')
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'Wrote {OUT_PATH} with {len(unique_questions)} candidate blocks')
