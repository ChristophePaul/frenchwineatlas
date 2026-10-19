French translation of the two Wine Chemistry pages (2026-10-16).
Each translated block carries data-fr / data-en; assets/nav.js swaps them (FR/EN button, first-visit chooser). French is the default.
The originals (English only) are in _backups/wine_chemistry_2026-10-16/.
To redo it from an English original:  python3 apply.py <original.html> <xx_keys.json> <xx_fr.txt> <out.html>
  xx_fr.txt = "index<TAB>French" per line, aligned with xx_keys.json ("=" keeps the English, used for bibliography titles).
Needs beautifulsoup4.
