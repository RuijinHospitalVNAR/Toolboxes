# VLPIM Python Scripts

This directory contains standalone Python scripts that can be used locally for VLPIM analysis.

## Download and Installation

Download the scripts from the repository:
```bash
git clone https://github.com/RuijinHospitalVNAR/Toolboxes.git
cd Toolboxes/scripts
```

Or download individual files directly from:
https://github.com/RuijinHospitalVNAR/Toolboxes/tree/main/scripts

## Available Scripts

### 1. `run_rmsd.py` - RMSD Structure Comparison

Calculate RMSD (Root Mean Square Deviation) between reference and predicted protein structures.

**Features:**
- Supports PDB and CIF file formats
- Multiple calculation methods: BioPython, Kabsch, Iterative pruning, PyMOL
- Iterative pruning alignment for improved accuracy
- Chain-specific analysis

**Usage:**
```bash
# Single structure comparison
python run_rmsd.py --reference ref.pdb --candidate pred.pdb --method biopython

# Multiple structures
python run_rmsd.py --reference ref.pdb --candidates pred1.pdb pred2.pdb --output results.csv

# Iterative pruning alignment
python run_rmsd.py --reference ref.pdb --candidate pred.pdb --method iterative --cutoff 2.0 --cycles 5

# Chain-specific analysis
python run_rmsd.py --reference ref.pdb --candidate pred.pdb --chain-ref A --chain-mob A
```

**Installation:**
```bash
pip install numpy pandas biopython
# Optional: for PyMOL method
pip install pymol-open-source
```

### 2. `run_ic50_sum.py` - Immunogenicity Score Calculation

Compute S<sup>im</sup> scores from NetMHCIIpan output files.

**Features:**
- Supports CSV, XLS, and XLSX formats
- Two-header format parsing (alleles + fields)
- Enhance and reduce modes
- Per-peptide and sequence-level aggregation

**Usage:**
```bash
# Basic usage
python run_ic50_sum.py input.csv reduce

# Specify output directory
python run_ic50_sum.py input.csv reduce --outdir results/

# Enhance mode
python run_ic50_sum.py input.csv enhance
```

**Input Format:**
- First row: HLA allele names (e.g., DRB1_0101, DRB1_1501)
- Second row: Field names (Peptide, nM, Rank, etc.)
- Subsequent rows: Data rows

**Installation:**
```bash
pip install pandas numpy openpyxl
```

### 3. `epitope_analyzer.py` - Epitope Identification and Analysis

Identify and analyze epitopes from NetMHCIIpan results with core extension and binding strength filtering.

**Features:**
- Parse NetMHCIIpan output files (standard and Excel formats)
- Filter epitopes by binding strength (Strong/Weak binding)
- Extend core sequences to target length
- Support for enhance/reduce modes

**Usage:**
```bash
# Basic usage
python epitope_analyzer.py --netmhcii-file results.xls --vlp-sequence "MKTAYIAKQR..." --target-length 15 --top-n 10 --mode reduce

# Specify output file
python epitope_analyzer.py --netmhcii-file results.xls --vlp-sequence "MKTAYIAKQR..." --output epitopes.csv
```

**Installation:**
```bash
pip install pandas numpy openpyxl
```

## Requirements

All scripts require:
- Python 3.7+
- pandas
- numpy

Additional dependencies:
- `run_rmsd.py`: biopython (required), pymol-open-source (optional)
- `run_ic50_sum.py`: openpyxl (for Excel files)
- `epitope_analyzer.py`: openpyxl (for Excel files)

**Install all dependencies:**
```bash
pip install pandas numpy biopython openpyxl
```

## File Formats

### NetMHCIIpan Output Format

The scripts support both standard text output and Excel format from NetMHCIIpan:

**Standard Format:**
```
Pos  Peptide     Allele      IC50(nM)  Rank(%)
1    MKTAYIAKQR  DRB1*01:01  1234.5    2.3
```

**Excel Format (Wide Table):**
- Row 1: HLA allele names
- Row 2: Field names (Core, Score, Rank, nM, etc.)
- Row 3+: Data rows

### Structure Files

- **PDB format**: Standard Protein Data Bank format
- **CIF format**: mmCIF format (used by AlphaFold3)

## Examples

### Example 1: Calculate RMSD for AlphaFold3 predictions

```bash
python run_rmsd.py \
    --reference reference.pdb \
    --candidate-dir ./alphafold_predictions \
    --method iterative \
    --cutoff 2.5 \
    --cycles 5 \
    --output rmsd_results.csv
```

### Example 2: Compute immunogenicity scores

```bash
python run_ic50_sum.py \
    netmhcii_results.xls \
    reduce \
    --outdir ./results
```

### Example 3: Identify top epitopes

```bash
python epitope_analyzer.py \
    --netmhcii-file DP_P03146_NetMHCIIpan.xls \
    --vlp-sequence "MDIDPYKEFGATVELLSFLPSDFFPSVRDLLDTASALYREALESPEHCSPHHTALRQAILCWGELMTLATWVGVNLEDPASRDLVVSYVNTNMGLKFRQLLWFHISCLTFGRETVIEYLVSFGVWIRTPPAYRPPNAPILSTLPETTVV" \
    --target-length 15 \
    --top-n 10 \
    --mode reduce \
    --output selected_epitopes.csv
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure all dependencies are installed:
```bash
pip install --upgrade pandas numpy biopython openpyxl
```

### File Format Issues

- Ensure NetMHCIIpan files are in the correct format (two-header for Excel files)
- Check that PDB/CIF files contain CA atoms
- Verify file encoding is UTF-8 for text files

### PyMOL Not Found

If using `--method pymol`, ensure PyMOL is installed:
```bash
pip install pymol-open-source
# Or download from https://pymol.org/2/
```

## Citation

If you use these scripts in your research, please cite:

```bibtex
@software{vlpim,
  title={VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles},
  author={Chufan Wang},
  year={2025},
  url={https://github.com/RuijinHospitalVNAR/Toolboxes}
}
```

## Contact

For questions or issues, please open an issue on GitHub:
https://github.com/RuijinHospitalVNAR/Toolboxes/issues

