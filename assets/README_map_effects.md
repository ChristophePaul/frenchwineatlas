# Region map effects — what they are and how to put them back

Added 2026-10-14 to the 25 region maps (the regional pages in `WEB Site/` plus
`Bourgogne Regions/Cote-d_Or.html`, `Saone-et-Loire.html`, `Beaujolais.html`, `Chablis_et_de_l_Auxerrois.html`).

| Effect | What the visitor sees | Where it lives |
|---|---|---|
| Elevation curves | Dark-brown contour lines; the 20 m and 100 m curves fade when zoomed out and reach full strength two zoom levels in | each page — `contour_fade_apply.py` |
| Softened colours | Dark appellation colours (Saint-Joseph, Hermitage, Côte de Nuits villages…) blended ~40 % toward cream so the curves show through; legend matches | each page — `soften_fills_apply.py` |
| Focus mode | Selecting an appellation fades every other appellation to 10 %, so its real coverage stands out | each page — `focus_apply.py`, `focus_exit_apply.py`, `focus_special_apply.py` |
| Leaving focus | Same row again, Escape, or a click on a faded commune (Côte-d'Or, Saône-et-Loire, Bordeaux, Beaujolais, Alsace grands crus: close the info card) | each page — `focus_exit_apply.py`, `focus_special_apply.py` |
| Sidebar = popup | A sidebar appellation row outlines the appellation's full area and counts its communes, exactly like choosing it from a commune's popup (before: only the communes painted in its colour, e.g. Saint-Bris 2 instead of 5) | each page — `sidebar_area_apply.py` |
| Rhône septentrional trim | Beaujolais, Côte roannaise and Côtes du Forez removed (own maps); only the 19 southernmost Rhône (69) communes kept (the 10 for Côte-Rôtie/Condrieu + a band showing the département continues north) and 35 Loire (42) communes (its 5 Rhône-side appellation communes + Pilat within ~12 km + the southern strip to the Ardèche); both outlines left open on their cut edges | `Rhone-septentrional.html` data — `rhone_sept_trim_apply.py` (needs shapely) |
| Beaujolais et Lyonnais | Coteaux du Lyonnais added to the Beaujolais map (48 communes, card from the 2011 CDC, sage-green fill, region button); map renamed « Vignobles du Beaujolais et du Lyonnais » (file name unchanged) | `Beaujolais.html` — `beaujolais_lyonnais_apply.py`; menu label in `nav_build.py`, home link in `index.html`, EN text in `i18n_maps_dict.json` |
| Coteaux du Lyonnais cadastral plan | `Plan Cadastraux/Beaujolais_Lyonnais/Coteaux-du-Lyonnais.html` (24 090 parcels, 7 704.6 ha); its button on the Beaujolais map comes from `plan_links_apply.py`, which now also covers `Bourgogne Regions/Beaujolais.html` | build: `GeoJson Files/Lyonnais/` (build_rh.py lyonnais → assemble_rh.py) |
| Beaujolais crus cadastral plans | 10 pages in `Plan Cadastraux/Beaujolais_Lyonnais/` (Saint-Amour … Côte de Brouilly); « Accéder au plan cadastral » at the bottom of the detail popup and of the selected-appellation card on the Beaujolais map, and for Saint-Amour on the Saône-et-Loire map (`plan_links_apply.py` SUBPAGES) | build: `GeoJson Files/Beaujolais/` (build_rh.py <cru> → assemble_rh.py; cards read from Beaujolais.html) |
| Beaujolais & Beaujolais-Villages plans | `Beaujolais.html` (132 293 parcels, 39 654 ha) and `Beaujolais-Villages.html` (49 818 parcels, 15 949 ha, the 28 « Beaujolais + commune » dénominations as a village layer) in `Plan Cadastraux/Beaujolais_Lyonnais/`, parcels in `*_parcelles/` loaded on zoom (keep those folders next to the pages) | build: `GeoJson Files/Beaujolais/` (keys beaujolais, bv); `plan_links_apply.py` alias « Beaujolais (régionale) » |
| Crus « mention » fix | The crus' fiches said « Primeur / Nouveau autorisée »; corrected per CDC (« cru du Beaujolais »; Brouilly 2024: none; Régnié: no local CDC, line removed) | `beaujolais_crus_mention_apply.py` (step 9) |
| Single-appellation communes | On the Bordeaux and Beaujolais maps, clicking a commune with only one appellation (all Coteaux du Lyonnais communes) now locks the popup and opens that appellation's detail with its plan button (before: a plain « Commune » card) | `single_aoc_pin_apply.py` (step 10) |
| Mâconnais cadastral plans | 7 pages in `Plan Cadastraux/Maconnais/`: Pouilly-Fuissé (22 premiers crus), Pouilly-Loché (Les Mûres), Pouilly-Vinzelles (3 premiers crus), Saint-Véran, Viré-Clessé, Mâcon-Villages (5 crus dashed) and Mâcon (27 « Mâcon + commune » dénominations); Mâcon and Mâcon-Villages load parcels on zoom (`*_parcelles/`). Plan buttons in the Saône-et-Loire popups | build: `GeoJson Files/Maconnais/`; cards from Saone-et-Loire.html |
| Côte chalonnaise cadastral plans | 7 pages in `Plan Cadastraux/Cote_Chalonnaise/`: Bouzeron, Rully (23 premiers crus), Mercurey (32), Givry (37), Montagny (49), Bourgogne Côte Chalonnaise (5 villages dashed) and Bourgogne Côtes du Couchois. Plan buttons in the Saône-et-Loire popups and, for Rully, the Côte-d'Or popup (`plan_links_apply.py` SUBPAGES) | build: `GeoJson Files/Chalonnais/`; village cards from Saone-et-Loire.html, the two Bourgogne dénominations from the CDC Bourgogne (arrêté 6 janvier 2026) |
| Chablis & Auxerrois cadastral plans | 10 pages in `Plan Cadastraux/Chablis_Auxerrois/`: Petit Chablis, Irancy, Saint-Bris, Vézelay and the six Bourgogne dénominations (Côtes d'Auxerre, Chitry, Coulanges-la-Vineuse, Tonnerre, Épineuil, Côte Saint-Jacques); plan buttons in the Chablis map popups (`plan_links_apply.py` SUBPAGES) | build: `GeoJson Files/Auxerrois/`; cards from Chablis_et_de_l_Auxerrois.html |
| « Accéder au plan cadastral et Climats » | Where no parcel plan exists, the Burgundy maps' popup button opens the village's climats map in `Bourgogne Regions/Bourgogne climats/` (Chablis + Chablis Grand Cru; the Côte-d'Or villages; each grand cru → its village's map, Blagny → Meursault). Côte-d'Or 56/74 linked (no map: Marsannay, Chorey-lès-Beaune, Saint-Romain, régionales). The button is also at the bottom of the selected-appellation card (`#readout.has-card`, opened from the sidebar or by clicking a grand cru parcel) on the Côte-d'Or and Saône-et-Loire maps | `plan_links_apply.py` (CLIM_ALIAS; readout patch) — backups `_backups/2026-10-15/` |
| Chablis crus + appellation card | On the Chablis & Auxerrois map: « Chablis 1er Cru » (8 communes) and a full « Chablis Grand Cru » fiche in the commune info-tip, with their climats as chips (CDC Chablis 2023 / Chablis grand cru 2024); a selected-appellation card (#readout, like Côte-d'Or) opens from a sidebar row or a click in a commune's list and ends with the plan / climats button | `chablis_crus_apply.py` (then `plan_links_apply.py`, `i18n_build.py`) — backup `_backups/2026-10-15/` |
| Chablis Grand Cru climats map | `Bourgogne climats/Chablis Grand Cru — …`: the Chablis 1er Cru climats map renamed « Chablis Grand Cru » and opening zoomed on the 7 grands crus; the Chablis Grand Cru buttons point to it; in the menu under Climats › Chablis | `chablis_gc_map_build.py` (rerun if the Chablis climats map changes) |
| Selection framing | The map flies to the selection in the space left clear by the title card, legend and info card | `theme.js` (shared, nothing to rerun) |

## After rebuilding a map page

The effects are written into the page itself, so a page regenerated from its source loses them.
Run, from `WEB Site/`:

```bash
python3 assets/map_effects_apply.py "Rhone-meridional.html"
```

Pass one or several pages (`"Bourgogne Regions/Cote-d_Or.html"` etc.). It runs the ten scripts in the
right order and skips whatever is already in place, so running it twice is harmless.
Tested 2026-10-14: applied to the original pages, it reproduces the live pages byte for byte.

The usual post-rebuild steps still apply as well — `assets/theme_apply.py`, `assets/smooth_zoom_apply.py`,
`plan_links_apply.py` (in `WEB Site/`), `assets/i18n_build.py`, `assets/nav_build.py` if a page was added.

## The individual scripts

- `contour_fade_apply.py` — contour colour, zoom fade, legend sample. The fade starts at each map's own opening zoom.
- `soften_fills_apply.py` — colours darker than relative luminance 0.12 in the page's appellation data; the two
  Rhône pages use hand-tuned values listed in the script.
- `focus_apply.py` — focus mode on the 21 pages built from the shared template (outline + `highlightAppel` /
  `highlightFill` / `highlightRegional`).
- `focus_exit_apply.py` — the ways out of focus mode on those same pages.
- `sidebar_area_apply.py` — sidebar rows that name a real appellation use its full area; group rows
  ("Chablis / Petit Chablis", "Bourgogne régionale"…) keep the colour-group behaviour.
- `focus_special_apply.py` — Côte-d'Or (villages, grands crus, sous-régionales, dénominations; régionales keep
  the full map), Saône-et-Loire, Alsace grand-cru parcels, Bordeaux, Beaujolais.

To change which Côte-d'Or appellations use focus mode, edit `FOCUS_KINDS` / `FOCUS_APPELS` in the page
(and in `focus_special_apply.py` so a rebuild keeps it).

## Backups

`WEB Site/_backups/2026-10-14/`
- `1_originals/` — the 25 pages before any of these changes
- `2_before_focus/` — after the curves and colours, before focus mode
- `4_before_rhone_trim/` — Rhône septentrional before the trim (+ `.after-69-trim.html`, the intermediate Rhône-only version)
- `5_before_lyonnais/` — Beaujolais page, `index.html`, `nav_build.py`/`nav.js`, `i18n_maps_dict.json`/`i18n_maps.js` before the Lyonnais addition
- `3_before_sidebar_area/` — the 20 shared-template pages before the sidebar/popup fix
- `assets/theme.js` — `theme.js` before the selection-framing hook

The `_backups` folder is about 360 MB and is not part of the site: leave it out when publishing.
