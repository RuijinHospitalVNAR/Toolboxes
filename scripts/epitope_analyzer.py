#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Epitope Analysis Tool

This tool analyzes NetMHCIIpan prediction results without running NetMHCIIpan.
It performs:
1. Parse NetMHCIIpan output file
2. Filter and select epitopes based on binding strength
3. Extend Core sequences to target length
4. Export results

Author: [Chufan Wang]
Version: 1.0
Date: 2025
"""

import os
import sys
import argparse
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

import pandas as pd


class ImmunogenicityMode(Enum):
    """Enumeration for immunogenicity modulation modes."""
    REDUCE = "reduce"
    ENHANCE = "enhance"


@dataclass
class AnalysisConfig:
    """Configuration class for the epitope analysis."""
    # Input parameters
    netmhcii_output: str  # NetMHCIIpan output file
    fasta_path: str  # Original VLP sequence file
    mode: ImmunogenicityMode
    
    # Output parameters
    output_dir: str = "results"
    log_level: str = "INFO"
    
    # Epitope selection parameters
    epitopes_number: int = 10
    epitope_length: int = 15  # Target epitope length (9-15 aa), extend from core if needed
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        pass


class EpitopeAnalyzer:
    """Main class for epitope analysis."""
    
    def __init__(self, config: AnalysisConfig):
        """Initialize the analyzer with configuration."""
        self.config = config
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        # Create output directory if it doesn't exist
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Configure logging
        log_file = os.path.join(self.config.output_dir, "epitope_analysis.log")
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        return logging.getLogger(__name__)
    
    def _validate_inputs(self) -> None:
        """Validate input files and parameters."""
        self.logger.info("Validating input parameters...")
        
        # Check NetMHCIIpan output file
        if not os.path.exists(self.config.netmhcii_output):
            raise FileNotFoundError(f"NetMHCIIpan output file not found: {self.config.netmhcii_output}")
        
        # Check FASTA file
        if not os.path.exists(self.config.fasta_path):
            raise FileNotFoundError(f"FASTA file not found: {self.config.fasta_path}")
        
        # Validate file extensions
        if not self.config.fasta_path.lower().endswith(('.fasta', '.fa')):
            raise ValueError(f"Invalid FASTA file extension: {self.config.fasta_path}")
        
        # Validate mode
        if not isinstance(self.config.mode, ImmunogenicityMode):
            if isinstance(self.config.mode, str):
                self.config.mode = ImmunogenicityMode(self.config.mode.lower())
            else:
                raise ValueError(f"Invalid mode: {self.config.mode}")
        
        self.logger.info("Input validation completed successfully")
    
    def _save_config(self) -> None:
        """Save configuration to file for reproducibility."""
        config_file = os.path.join(self.config.output_dir, "analysis_config.json")
        config_dict = asdict(self.config)
        # Convert enum to string for JSON serialization
        config_dict['mode'] = self.config.mode.value
        
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        self.logger.info(f"Configuration saved to {config_file}")
    
    def _parse_netmhcii_output(self, output_file: str) -> pd.DataFrame:
        """
        Parse NetMHCIIpan output file.
        
        Supports multiple formats:
        1. Standard format: Pos Peptide ID Allele Core %Rank_EL BA_Rank BA_IC50 BA_Raw Score
        2. Wide-table format: multiple HLA alleles in columns (Core, Inverted, Score, Rank, Score_BA, nM, Rank_BA)
        """
        epitopes = []
        
        try:
            with open(output_file, 'r') as f:
                lines = f.readlines()
            
            # Detect format by checking if file has HLA allele names in header
            is_wide_format = False
            hla_alleles = []
            header_line = ""
            
            for i, line in enumerate(lines[:3]):
                if 'HLA-' in line.upper() or 'DRB1_' in line.upper():
                    is_wide_format = True
                    header_line = line.strip()
                    # Extract HLA allele names from header
                    parts = line.split('\t')
                    for part in parts:
                        if 'HLA-' in part.upper() or 'DRB1_' in part.upper():
                            hla_alleles.append(part.strip())
                    break
            
            if is_wide_format:
                self.logger.info(f"Detected wide-table format with {len(hla_alleles)} HLA alleles")
                return self._parse_wide_table_format(lines, hla_alleles)
            else:
                self.logger.info("Detected standard tabular format")
                return self._parse_standard_format(lines)
        
        except Exception as e:
            self.logger.error(f"Failed to parse NetMHCIIpan output: {e}")
            raise
    
    def _parse_wide_table_format(self, lines: List[str], hla_alleles: List[str]) -> pd.DataFrame:
        """
        Parse wide-table format where each HLA has columns: Core, Inverted, Score, Rank, Score_BA, nM, Rank_BA
        
        Format example:
        Pos  Peptide  ID  Target  Core  Inverted  Score  Rank  Score_BA  nM  Rank_BA  [Core  Inverted  Score  Rank  Score_BA  nM  Rank_BA ...]
        """
        epitopes = []
        
        # Find header line (line 2, 0-indexed line 1)
        header_line = lines[1].strip()
        header_parts = header_line.split('\t')
        
        # Find the data start line (usually line 2 or 3)
        data_start_idx = 2
        while data_start_idx < len(lines) and (lines[data_start_idx].strip().startswith('#') or not lines[data_start_idx].strip()):
            data_start_idx += 1
        
        self.logger.info(f"Parsing wide-table format, data starts at line {data_start_idx + 1}")
        
        # Parse each data line
        for line_idx in range(data_start_idx, len(lines)):
            line = lines[line_idx].strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('\t')
            if len(parts) < 5:
                continue
            
            try:
                # Parse position, peptide, ID from first 3 columns
                pos = int(parts[0])
                peptide = parts[1]
                seq_id = parts[2] if len(parts) > 2 else "Sequence"
                
                # For wide format: Target column, then alternating HLA columns
                # Each HLA has: Core, Inverted, Score, Rank, Score_BA, nM, Rank_BA (7 columns)
                cols_per_allele = 7
                data_start_col = 4  # After Pos, Peptide, ID, Target
                
                # Process each HLA allele
                for i, allele in enumerate(hla_alleles):
                    allele_start_col = data_start_col + (i * cols_per_allele)
                    
                    if allele_start_col + 6 < len(parts):
                        try:
                            core = parts[allele_start_col]
                            inverted = parts[allele_start_col + 1] if len(parts) > allele_start_col + 1 else "0"
                            score = float(parts[allele_start_col + 2]) if len(parts) > allele_start_col + 2 else None
                            rank = float(parts[allele_start_col + 3]) if len(parts) > allele_start_col + 3 else None
                            score_ba = float(parts[allele_start_col + 4]) if len(parts) > allele_start_col + 4 else None
                            nm = float(parts[allele_start_col + 5]) if len(parts) > allele_start_col + 5 else None
                            rank_ba = float(parts[allele_start_col + 6]) if len(parts) > allele_start_col + 6 else None
                            
                            # Calculate position information
                            start_pos = pos
                            end_pos = start_pos + len(peptide) - 1
                            
                            epitopes.append({
                                'sequence': peptide,
                                'core': core if core and core != 'NA' else peptide,
                                'start': start_pos,
                                'end': end_pos,
                                'score': score if score is not None else 0.0,
                                'rank_el': rank,  # Rank is %Rank_EL
                                'rank': rank_ba,  # Rank_BA is BA_Rank
                                'ic50': nm,
                                'raw_score': score_ba,
                                'allele': allele,
                                'seq_id': seq_id,
                                'method': 'NetMHCIIpan-4.3'
                            })
                        except (ValueError, IndexError) as e:
                            continue
                        
            except (ValueError, IndexError) as e:
                continue
        
        self.logger.info(f"Parsed {len(epitopes)} epitope entries from wide-table format")
        return pd.DataFrame(epitopes)
    
    def _parse_standard_format(self, lines: List[str]) -> pd.DataFrame:
        """
        Parse standard NetMHCIIpan format.
        
        Format: Pos Peptide ID Allele Core %Rank_EL BA_Rank BA_IC50 BA_Raw Score
        Or: Pos Peptide ID Allele BA_Rank BA_IC50 BA_Raw Score (if Core not available)
        """
        epitopes = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
                
            parts = line.split()
            # Try to parse format with Core and %Rank_EL (9+ columns)
            if len(parts) >= 9:
                try:
                    pos = int(parts[0])
                    peptide = parts[1]
                    seq_id = parts[2] if len(parts) > 2 else ""
                    allele = parts[3]
                    core = parts[4] if len(parts) > 4 else ""
                    rank_el = float(parts[5]) if len(parts) > 5 else None
                    ba_rank = float(parts[6]) if len(parts) > 6 else None
                    ba_ic50 = float(parts[7]) if len(parts) > 7 else None
                    ba_raw = float(parts[8]) if len(parts) > 8 else None
                    score = float(parts[9]) if len(parts) > 9 else None
                    
                    # Calculate position information
                    start_pos = pos
                    end_pos = start_pos + len(peptide) - 1
                    
                    epitopes.append({
                        'sequence': peptide,
                        'core': core if core else peptide,  # Use peptide as core if core not available
                        'start': start_pos,
                        'end': end_pos,
                        'score': score if score is not None else ba_raw if ba_raw is not None else 0.0,
                        'rank_el': rank_el,  # %Rank_EL
                        'rank': ba_rank,     # BA_Rank
                        'ic50': ba_ic50,
                        'raw_score': ba_raw,
                        'allele': allele,
                        'seq_id': seq_id,
                        'method': 'NetMHCIIpan-4.3'
                    })
                except (ValueError, IndexError) as e:
                    # Try alternative format without Core (8 columns)
                    if len(parts) >= 8:
                        try:
                            pos = int(parts[0])
                            peptide = parts[1]
                            seq_id = parts[2] if len(parts) > 2 else ""
                            allele = parts[3]
                            ba_rank = float(parts[4])
                            ba_ic50 = float(parts[5])
                            ba_raw = float(parts[6])
                            score = float(parts[7])
                            
                            start_pos = pos
                            end_pos = start_pos + len(peptide) - 1
                            
                            epitopes.append({
                                'sequence': peptide,
                                'core': peptide,  # Use peptide as core when not available
                                'start': start_pos,
                                'end': end_pos,
                                'score': score,
                                'rank_el': None,  # Not available
                                'rank': ba_rank,
                                'ic50': ba_ic50,
                                'raw_score': ba_raw,
                                'allele': allele,
                                'seq_id': seq_id,
                                'method': 'NetMHCIIpan-4.3'
                            })
                        except (ValueError, IndexError):
                            continue
                    continue
        
        return pd.DataFrame(epitopes)
    
    def _get_sequence_length(self) -> int:
        """Get sequence length from FASTA file."""
        try:
            seq_length = 0
            with open(self.config.fasta_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('>'):
                        seq_length += len(line)
            return seq_length
        except Exception as e:
            self.logger.warning(f"Failed to read sequence length: {e}")
            raise
    
    def _get_full_sequence(self) -> str:
        """Get full protein sequence from FASTA file."""
        sequence = ""
        with open(self.config.fasta_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('>'):
                    sequence += line
        if not sequence:
            raise ValueError("Empty sequence read from FASTA file")
        return sequence
    
    def _filter_epitopes_by_binding(self, epitope_df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter epitopes based on strong/weak binding counts per Core sequence.
        
        Criteria:
        - Strong binding: %Rank_EL <= 1.00%
        - Weak binding: 1.00% < %Rank_EL <= 5.00%
        - Number of strong binding = strong + weak binding counts per Core
        
        For reduce mode: select top N cores with highest number of strong binding
        For enhance mode: select bottom N cores with lowest number of strong binding
        
        Args:
            epitope_df: DataFrame with epitope predictions
            
        Returns:
            Filtered DataFrame with selected epitopes
        """
        self.logger.info("Filtering epitopes based on binding strength...")
        
        if epitope_df.empty:
            return epitope_df
        
        # Determine which rank column to use
        rank_col = None
        if 'rank_el' in epitope_df.columns:
            rank_col = 'rank_el'
            self.logger.info("Using %Rank_EL for binding classification")
        elif 'rank' in epitope_df.columns:
            rank_col = 'rank'
            self.logger.warning("%Rank_EL not available, using BA_Rank instead")
        else:
            self.logger.warning("No rank information available, skipping filtering")
            return epitope_df
        
        # Ensure core column exists
        if 'core' not in epitope_df.columns:
            if 'sequence' in epitope_df.columns:
                epitope_df['core'] = epitope_df['sequence']
                self.logger.info("Core column not found, using sequence as core")
            else:
                self.logger.warning("Neither core nor sequence column found, skipping filtering")
                return epitope_df
        
        # Classify binding strength
        # Strong binding: %Rank <= 1.00%
        # Weak binding: 1.00% < %Rank <= 5.00%
        def classify_binding(rank_value):
            if pd.isna(rank_value):
                return None
            if rank_value <= 1.00:
                return 'strong'
            elif rank_value <= 5.00:
                return 'weak'
            else:
                return None
        
        epitope_df['binding_class'] = epitope_df[rank_col].apply(classify_binding)
        
        # Count strong and weak bindings per core
        core_binding_counts = []
        for core in epitope_df['core'].unique():
            core_data = epitope_df[epitope_df['core'] == core]
            strong_count = len(core_data[core_data['binding_class'] == 'strong'])
            weak_count = len(core_data[core_data['binding_class'] == 'weak'])
            number_of_strong_binding = strong_count + weak_count
            
            core_binding_counts.append({
                'core': core,
                'strong_count': strong_count,
                'weak_count': weak_count,
                'number_of_strong_binding': number_of_strong_binding
            })
        
        core_counts_df = pd.DataFrame(core_binding_counts)
        
        # Sort by number_of_strong_binding
        core_counts_df = core_counts_df.sort_values(
            'number_of_strong_binding',
            ascending=False
        ).reset_index(drop=True)
        
        self.logger.info(f"Core sequences ranked: {len(core_counts_df)} unique cores")
        self.logger.info(f"Top 5 cores by binding count: {core_counts_df.head(5)['core'].tolist()}")
        
        # Determine effective number of epitopes to select based on sequence length
        # To prevent overlapping mutation regions, limit epitopes for short sequences
        try:
            # Read sequence length from FASTA
            seq_length = self._get_sequence_length()
            if seq_length < 200:
                # For sequences shorter than 200 amino acids, limit to maximum 3 epitopes
                n_effective = min(self.config.epitopes_number, 3)
                self.logger.info(f"Sequence length ({seq_length} aa) < 200, limiting epitopes to {n_effective}")
            else:
                n_effective = self.config.epitopes_number
        except Exception as e:
            self.logger.warning(f"Could not determine sequence length: {e}, using user-defined value")
            n_effective = self.config.epitopes_number
        
        # Select top or bottom N cores based on mode
        if self.config.mode == ImmunogenicityMode.REDUCE:
            # Reduce mode: select cores with highest binding (top N)
            selected_cores = core_counts_df.head(n_effective)['core'].tolist()
            self.logger.info(f"Reduce mode: selecting top {n_effective} cores with highest binding")
        else:  # ENHANCE
            # Enhance mode: select cores with lowest binding (bottom N)
            selected_cores = core_counts_df.tail(n_effective)['core'].tolist()
            self.logger.info(f"Enhance mode: selecting bottom {n_effective} cores with lowest binding")
        
        # Filter epitope_df to only include selected cores
        filtered_df = epitope_df[epitope_df['core'].isin(selected_cores)].copy()
        
        # Add binding count information to filtered epitopes
        if not filtered_df.empty:
            core_counts_dict = dict(zip(
                core_counts_df['core'],
                core_counts_df['number_of_strong_binding']
            ))
            filtered_df['number_of_strong_binding'] = filtered_df['core'].map(core_counts_dict)
        
        self.logger.info(f"Selected {len(selected_cores)} cores, resulting in {len(filtered_df)} epitopes")
        
        return filtered_df
    
    def _extend_core_sequences(self, epitope_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extend Core sequences to target epitope_length using amino acids from the original VLP sequence.
        
        Extension strategy:
        - Target length: epitope_length (default 15, range 9-15 aa)
        - Maximum forward extension (toward N-terminal): 2 amino acids
        - Maximum backward extension (toward C-terminal): 4 amino acids
        - Priority: extend forward first (up to 2 aa), then backward (up to 4 aa)
        - All extended amino acids come from the original input VLP sequence
        - Example: 9-mer core -> forward 2 aa + backward 4 aa -> 15-mer
        
        Args:
            epitope_df: DataFrame with core sequences and positions
            
        Returns:
            DataFrame with extended sequences and updated positions
        """
        self.logger.info(f"Extending core sequences to target length {self.config.epitope_length}...")
        
        if epitope_df.empty:
            return epitope_df
        
        # Get full protein sequence from original VLP FASTA file
        try:
            full_sequence = self._get_full_sequence()
            seq_length = len(full_sequence)
        except Exception as e:
            self.logger.warning(f"Could not read full sequence: {e}, skipping extension")
            return epitope_df
        
        # Validate target length
        if self.config.epitope_length < 9 or self.config.epitope_length > 15:
            self.logger.warning(f"Invalid epitope_length {self.config.epitope_length}, must be 9-15. Using 15.")
            target_length = 15
        else:
            target_length = self.config.epitope_length
        
        extended_sequences = []
        extended_starts = []
        extended_ends = []
        
        for _, row in epitope_df.iterrows():
            core_seq = row.get('core', row.get('sequence', ''))
            core_start = int(row.get('start', 1))
            core_end = int(row.get('end', core_start + len(core_seq) - 1))
            
            core_len = len(core_seq)
            
            # If core is already at or above target length, keep as is
            if core_len >= target_length:
                extended_sequences.append(core_seq)
                extended_starts.append(core_start)
                extended_ends.append(core_end)
                continue
            
            # Calculate extension needed
            extension_needed = target_length - core_len
            max_forward = min(2, extension_needed)
            max_backward = min(4, extension_needed - max_forward)
            
            # Calculate new start and end positions (1-based)
            new_start = max(1, core_start - max_forward)
            new_end = min(seq_length, core_end + max_backward)
            
            # Extract extended sequence from full sequence
            extended_seq = full_sequence[new_start - 1:new_end]
            
            extended_sequences.append(extended_seq)
            extended_starts.append(new_start)
            extended_ends.append(new_end)
            
            self.logger.debug(
                f"Extended core {core_seq} ({core_len}aa) at [{core_start}-{core_end}] "
                f"to {extended_seq} ({len(extended_seq)}aa) at [{new_start}-{new_end}]"
            )
        
        # Update DataFrame with extended sequences
        result_df = epitope_df.copy()
        result_df['sequence'] = extended_sequences
        result_df['start'] = extended_starts
        result_df['end'] = extended_ends
        
        self.logger.info(f"Extended {len(result_df)} epitope sequences")
        
        return result_df
    
    def run_analysis(self) -> pd.DataFrame:
        """
        Run the complete epitope analysis pipeline.
        
        Returns:
            DataFrame containing analysis results
        """
        self.logger.info(f"Starting epitope analysis pipeline...")
        self.logger.info(f"Input NetMHCIIpan output: {self.config.netmhcii_output}")
        self.logger.info(f"Input FASTA: {self.config.fasta_path}")
        self.logger.info(f"Mode: {self.config.mode.value}")
        self.logger.info(f"Output directory: {self.config.output_dir}")
        
        try:
            # Validate inputs
            self._validate_inputs()
            
            # Save configuration
            self._save_config()
            
            # Run analysis steps
            self.logger.info("Step 1: Parsing NetMHCIIpan output...")
            epitope_df = self._parse_netmhcii_output(self.config.netmhcii_output)
            self.logger.info(f"Parsed {len(epitope_df)} epitopes from NetMHCIIpan output")
            
            if epitope_df.empty:
                raise ValueError("No epitopes found in NetMHCIIpan output")
            
            self.logger.info("Step 2: Filtering epitopes based on binding strength...")
            epitope_df = self._filter_epitopes_by_binding(epitope_df)
            self.logger.info(f"After filtering: {len(epitope_df)} epitopes selected")
            
            self.logger.info("Step 3: Extending core sequences to target length...")
            epitope_df = self._extend_core_sequences(epitope_df)
            
            # Save results
            result_file = os.path.join(self.config.output_dir, "selected_epitopes.csv")
            epitope_df.to_csv(result_file, index=False)
            
            self.logger.info(f"Results saved to {result_file}")
            
            # Log completion
            self.logger.info("=" * 60)
            self.logger.info("EPITOPE ANALYSIS COMPLETED SUCCESSFULLY!")
            self.logger.info(f"Total epitopes selected: {len(epitope_df)}")
            self.logger.info("=" * 60)
            
            return epitope_df
            
        except Exception as e:
            self.logger.error(f"Epitope analysis failed: {e}")
            raise


def create_config_from_args(args) -> AnalysisConfig:
    """Create configuration from command line arguments."""
    return AnalysisConfig(
        netmhcii_output=args.netmhcii_output,
        fasta_path=args.fasta,
        mode=ImmunogenicityMode(args.mode),
        output_dir=args.output_dir,
        log_level=args.log_level,
        epitopes_number=args.epitopes_number,
        epitope_length=args.epitope_length
    )


def main():
    """Main entry point for the epitope analysis tool."""
    parser = argparse.ArgumentParser(
        description="Epitope Analysis Tool - Analyze NetMHCIIpan prediction results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - reduce immunogenicity
  python epitope_analyzer.py --netmhcii-output netmhcii.out --fasta protein.fasta --mode reduce
  
  # Enhance immunogenicity with custom parameters
  python epitope_analyzer.py --netmhcii-output netmhcii.out --fasta protein.fasta --mode enhance --epitopes-number 15 --epitope-length 12
  
  # Custom output directory and log level
  python epitope_analyzer.py --netmhcii-output netmhcii.out --fasta protein.fasta --mode reduce --output-dir custom_results --log-level DEBUG
        """
    )
    
    # Required arguments
    parser.add_argument('--netmhcii-output', type=str, required=True,
                       help='NetMHCIIpan output file path')
    parser.add_argument('--fasta', type=str, required=True,
                       help='Input FASTA file path')
    parser.add_argument('--mode', type=str, choices=['reduce', 'enhance'],
                       default='reduce',
                       help='Immunogenicity mode: reduce or enhance (default: reduce)')
    
    # Optional arguments
    parser.add_argument('--output-dir', type=str, default='results',
                       help='Output directory for results (default: results)')
    parser.add_argument('--log-level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level (default: INFO)')
    
    # Epitope selection parameters
    parser.add_argument('--epitopes-number', type=int, default=10,
                       help='Number of epitopes to select based on binding strength (default: 10)')
    parser.add_argument('--epitope-length', type=int, default=15,
                       help='Target epitope length (9-15 aa), extends from core if needed (default: 15)')
    
    args = parser.parse_args()
    
    try:
        # Create configuration
        config = create_config_from_args(args)
        
        # Initialize and run analysis
        analyzer = EpitopeAnalyzer(config)
        results = analyzer.run_analysis()
        
        print("\n" + "=" * 60)
        print("EPITOPE ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"Total epitopes selected: {len(results)}")
        print(f"Results saved in: {config.output_dir}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nAnalysis failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

