# Toolboxes

A collection of web-based bioinformatics tools hosted on GitHub Pages.

## Available Tools

### VLPIM Web Services

**VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles**

- **URL**: [VLPIM Web Services](VLPIM_Web_services/)
- **Description**: An integrated computational workflow for modulating protein immunogenicity through epitope identification, MHC-II binding evaluation, and structural superposition.
- **Features**:
  - Epitope identification using NetMHCIIpan
  - Immunogenicity analysis with S<sup>im</sup> scores
  - Structural superposition with RMSD and TM-align
  - Interactive web interface

### Circular Contact Map
Nanobody–antigen interface analysis by circular ribbon diagrams
- **URL**: [Circular Contact Map](Circular_Contact_Map/)
- **Description**: Extract contacts from mmCIF or read edges.csv and generate an interactive chord (ribbon) diagram.
- **Features**:
  - Contact extraction for two chains from mmCIF
  - Interactive HTML plot or PNG export
  - Simple CSV format: source,target[,distance]

## Repository Structure

```
Toolboxes/
├── VLPIM_Web_services/     # VLPIM web tool
├── Circular_Contact_Map/   # Circular contact map tool
├── README.md               # This file
└── index.html              # Repository homepage
```

## Contributing

More tools will be added to this repository in the future. Each tool should be placed in its own directory with appropriate documentation.

## License

Please refer to the license file in each tool's directory.

## Contact

- **Author**: Dr. Chufan Wang
- **Institution**: Ruijin Hospital, Shanghai Jiao Tong University School of Medicine
- **GitHub**: [@RuijinHospitalVNAR](https://github.com/RuijinHospitalVNAR)
