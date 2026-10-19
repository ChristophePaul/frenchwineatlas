#!/bin/bash
# vdiff.sh slug Name  — diff a 2010 Burgundy village draft vs Morey, hiding commune-list noise
python3 _en_tools/fr_diff.py bourgogne_cote_de_nuits_morey_saint_denis "$1" "Morey-Saint-Denis" "$2" 2>&1 | grep -v "^  [~+-] \(Agencourt\|Accolay\|Alix\|Aluze\)" | cut -c1-1200
