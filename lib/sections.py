import json
from pathlib import Path
from typing import List

DATA_PATH = Path('data/uncertainty_sections.json')

class Section:
    def __init__(self, title: str, content: List[str]) -> None:
        self.title = title
        self.content = content

    @staticmethod
    def load_all() -> List['Section']:
        data = json.loads(Path(DATA_PATH).read_text(encoding='utf-8'))
        sections = [Section(s['title'], s.get('content', [])) for s in data['sections']]
        return sections

