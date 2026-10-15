"""Вшивает sounds/*.mp3 в index.html блоком <script id="sounds"> (base64 в JSON).

Запуск из корня проекта: python3 sounds/embed.py
"""

import base64
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
names = [
    "music",
    "rain",
    "wind",
    "whoosh",
    "paper",
    "kalimba",
    "splash",
    "drop",
    "drip",
]
data = {
    n: base64.b64encode((root / "sounds" / f"{n}.mp3").read_bytes()).decode()
    for n in names
}
block = f'<script id="sounds" type="application/json">{json.dumps(data)}</script>\n'

page = (root / "index.html").read_text(encoding="utf-8")
old = re.compile(r'<script id="sounds" type="application/json">.*?</script>\n', re.DOTALL)
if old.search(page):
    page = old.sub(lambda _: block, page, count=1)
else:
    page = page.replace(
        '<script type="importmap">', block + '<script type="importmap">', 1
    )
(root / "index.html").write_text(page, encoding="utf-8")
print(f"вшито {len(names)} звуков, {sum(map(len, data.values())) // 1024} КБ base64")
