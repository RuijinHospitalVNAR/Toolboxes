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
- Compute S^im scores from NetMHCIIpan results
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
- `6htx.pdb`: Example structure file

## Usage

1. **Epitope Identification**:
   - Upload NetMHCIIpan output file
   - Enter VLP sequence
   - Select Top N epitopes and Target length
   - Choose Enhance or Reduce mode
   - Click "epitopes identification"

2. **Immunogenicity Analysis**:
   - Upload NetMHCIIpan output file
   - Select mode (Enhance/Reduce)
   - Click "Compute S^im scores"

3. **Structural Superposition**:
   - Upload reference and predicted structures
   - Select alignment method (Kabsch/Iterative/TM-align)
   - Click "Calculate RMSD"

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern browsers with JavaScript enabled

## Notes

- All calculations are performed client-side (in your browser)
- No data is sent to external servers
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

