# VLPIM Web Services

**VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles**

## Overview

VLPIM Web Services provides an integrated computational workflow for modulating protein immunogenicity through:
- Epitope identification using NetMHCIIpan
- MHC-II binding evaluation
- Structural superposition analysis

## Quick Start

Simply open `index.html` in your web browser or visit the [live version](https://ruijinhospitalvnar.github.io/Toolboxes/VLPIM_Web_services/) on GitHub Pages.

## Features

### 1. Epitope Identification
- Upload NetMHCIIpan output files (.txt, .xls, .xlsx)
- Enter VLP amino acid sequence
- Identify and extend epitopes to target length (9-15 aa)
- Filter by binding strength (Strong/Weak binding)

### 2. Immunogenicity Analysis
- Compute S<sup>im</sup> scores from NetMHCIIpan results
- Enhance or Reduce modes for immunogenicity modulation
- Export results to CSV

### 3. Structural Superposition
- Calculate RMSD between reference and predicted structures
- Support for Kabsch, Iterative pruning, and TM-align methods
- Upload PDB or CIF format structure files

## File Formats

- **NetMHCIIpan output**: Standard text format (.txt) or Excel format (.xls/.xlsx)
- **Structure files**: PDB or CIF format
- **Sequences**: Amino acid sequences (FASTA format or plain text)

## Example Files

The following example files are included:
- `DP_P03146_NetMHCIIpan.xls`: Example NetMHCIIpan output
- `seq-a .csv`: Example immunogenicity input table
- `6htx.pdb`: Example structure file

## Usage

1. **Step 1: Epitope identify**
   - Upload NetMHCIIpan output (`.txt/.xls/.xlsx`) and enter VLP sequence
   - Set Top N epitopes, target length (9-15 aa), and analysis mode (Enhance/Reduce)
   - Optional: click **Load example**
   - Click **Epitopes identification**
   - Optional: click **Export extended epitopes** to download `selected_epitopes.csv`

2. **Step 4.1: Immunogenicity analysis**
   - Upload NetMHCIIpan output (`.txt/.csv/.xls/.xlsx`) and select mode (Enhance/Reduce)
   - Optional: click **Load example** (uses `seq-a .csv`)
   - Click **Compute S<sup>im</sup> scores**
   - Review peptide score table and click **Export CSV** (combined output, e.g. `sim_im_reduce_combined.csv`)

3. **Step 4.2: Structural superposition**
   - Upload reference and predicted structures (`.pdb/.cif`)
   - Select method: Kabsch / Iterative / TM-align
   - Optional: click **Load example 1** or **Load example 2**
   - Click **Calculate RMSD** and review RMSD result card (TM-score is shown for TM-align)

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern browsers with JavaScript enabled

## Notes

- All calculations are performed client-side (in your browser)
- Sequence/structure analysis data is processed locally in the browser
- Anonymous traffic analytics is optional (disabled by default; can be enabled by user)
- If analytics is enabled, page-view metrics may be sent to Google Analytics
- Large files may take longer to process

## Citation

If you use VLPIM in your research, please cite:

```
@software{vlpim,
  title={VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles},
  author={Chufan Wang},
  year={2025},
  url={https://github.com/RuijinHospitalVNAR/VLPIM}
}
```

## Contact

- **Author**: Dr. Chufan Wang
- **Institution**: Ruijin Hospital, Shanghai Jiao Tong University School of Medicine
- **GitHub**: [@RuijinHospitalVNAR](https://github.com/RuijinHospitalVNAR)

