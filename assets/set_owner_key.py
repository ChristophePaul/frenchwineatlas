#!/usr/bin/env python3
"""Set (or change) the owner passphrase that bypasses the member popup and locks.

Run it yourself in a terminal — the passphrase is typed hidden and never written anywhere:
    python3 assets/set_owner_key.py

Only its SHA-256 fingerprint ("fw-owner:" + passphrase) is stored, in assets/access.js (OWNER_HASH).
Then, in each browser you use, open any page of the site with   #cle=<your passphrase>   at the end of
the address (e.g. index.html#cle=...). The passphrase is wiped from the address bar at once and that
browser stays in owner mode. Undo with   #cle=off .   Changing the passphrase here logs out every browser.
Run with --clear to remove the owner key entirely.
"""
import getpass, hashlib, pathlib, re, sys

JS = pathlib.Path(__file__).with_name('access.js')
src = JS.read_text(encoding='utf-8')
pat = re.compile(r"var OWNER_HASH = '[0-9a-f]*';")
if not pat.search(src):
    sys.exit("OWNER_HASH line not found in access.js")

if '--clear' in sys.argv:
    JS.write_text(pat.sub("var OWNER_HASH = '';", src), encoding='utf-8')
    print("Owner key removed.")
    sys.exit()

p1 = getpass.getpass("New owner passphrase (hidden, 10+ characters): ")
if len(p1) < 10:
    sys.exit("Too short — use at least 10 characters (a few words is ideal).")
if p1.strip() != p1 or '&' in p1 or '#' in p1:
    sys.exit("Avoid leading/trailing spaces and the characters & and # (they break the #cle= address).")
if p1.lower() == 'off':
    sys.exit("'off' is reserved.")
if getpass.getpass("Type it again: ") != p1:
    sys.exit("The two entries differ — nothing changed.")

h = hashlib.sha256(('fw-owner:' + p1).encode('utf-8')).hexdigest()
JS.write_text(pat.sub("var OWNER_HASH = '%s';" % h, src), encoding='utf-8')
print("Owner key saved in assets/access.js.")
print("Unlock a browser by opening:  index.html#cle=<your passphrase>   (undo: #cle=off)")
