# Circular Contact Map

Nanobody–antigen interface analysis by circular ribbon diagrams.

## Features
- Extract contacts from mmCIF for two chains
- Draw interactive chord (ribbon) plot (HTML)
- Optional PNG export

## Install
```bash
pip install pandas holoviews bokeh biopython matplotlib
```

## Usage
From mmCIF (recommended):
```bash
python scripts/circular_ribbon_contact_map.py --cif complex.cif --chain1 H --chain2 L --cutoff 5.0 --output H_L_contact_map.html
```
From edges.csv:
```bash
python scripts/circular_ribbon_contact_map.py edges.csv --output contact_map.html
```

## Input formats
- mmCIF: standard PDB/mmCIF
- edges.csv: columns `source,target[,distance]`, node format `Chain_RES3_Num` (e.g. `A_ARG_100`)

## Output
- FASTA sequences for each chain
- `*_contacts.csv` with contact pairs and distances
- Interactive HTML or PNG plot


