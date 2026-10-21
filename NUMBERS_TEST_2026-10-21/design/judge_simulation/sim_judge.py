"""Judge's scratch check of the chosen rules (no training, repo untouched)."""
import sys, json, time
sys.path.insert(0, "/home/user/utensil-theories-transfer-protocol/experiments")
import numpy as np
import shifting_word as sw
from bible_understanding import load_verses, tokens
from pathlib import Path
HERE = Path(__file__).parent
verses = load_verses(); texts = [t for _, t in verses]
t0 = time.time()
values = sw.word_values(texts)
print("word_values s", round(time.time()-t0,1))
cached = json.loads(Path(HERE.parent/"numbers_lens/values.json").read_text())
print("cached values identical:", cached == values)
json.dump(values, open(HERE/"values.json","w"))
