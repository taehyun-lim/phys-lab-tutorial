import json
from pathlib import Path
from typing import List

DATA_PATH = Path('data/uncertainty_sections_html.json')

class SectionHTML:
    def __init__(self, title: str, html: str) -> None:
        self.title = title
        self.html = html

    @staticmethod
    def load_all() -> List['SectionHTML']:
        data = json.loads(Path(DATA_PATH).read_text(encoding='utf-8'))
        return [SectionHTML(s['title'], s.get('html', '')) for s in data['sections']]
