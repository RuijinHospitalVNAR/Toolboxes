#!/usr/bin/env python3
"""
RMSD Structure Comparison Script

Calculate RMSD between reference and predicted PDB structures.
Similar to run_ic50_sum.py, this script extracts RMSD calculation functionality.

Author: Chufan Wang
Version: 1.0
Date: 2025
"""

import pandas as pd
import numpy as np
import sys
import os
import argparse
import subprocess
import tempfile
import re
from pathlib import Path
from typing import List, Optional, Tuple


def parse_pdb(pdb_path: str) -> Optional[np.ndarray]:
    """
    Parse PDB file and extract CA atom coordinates.
    
    Args:
        pdb_path: Path to PDB file
        
    Returns:
        Numpy array of CA atom coordinates (N x 3)
    """
    try:
        ca_coords = []
        with open(pdb_path, 'r') as f:
            for line in f:
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    atom_name = line[12:16].strip()
                    if atom_name == 'CA':
                        try:
                            x = float(line[30:38])
                            y = float(line[38:46])
                            z = float(line[46:54])
                            ca_coords.append([x, y, z])
                        except (ValueError, IndexError):
                            continue
        if len(ca_coords) == 0:
            return None
        return np.array(ca_coords)
    except Exception as e:
        print(f"Error parsing PDB {pdb_path}: {e}")
        return None


def parse_cif(cif_path: str) -> Optional[np.ndarray]:
    """
    Parse CIF file and extract CA atom coordinates.
    
    Args:
        cif_path: Path to CIF file
        
    Returns:
        Numpy array of CA atom coordinates (N x 3)
    """
    try:
        ca_coords = []
        in_atom_site = False
        header_cols = {}
        
        with open(cif_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Check if we're in the atom_site loop
                if line.startswith('loop_'):
                    in_atom_site = False
                    header_cols = {}
                    continue
                
                if line.startswith('_atom_site.'):
                    in_atom_site = True
                    col_name = line.replace('_atom_site.', '').strip()
                    header_cols[col_name] = len(header_cols)
                    continue
                
                if in_atom_site and line and not line.startswith('#'):
                    # Parse data line
                    parts = line.split()
                    if len(parts) >= 13:
                        # Check if this is a CA atom
                        label_atom_id_idx = header_cols.get('label_atom_id', 3)
                        cartn_x_idx = header_cols.get('Cartn_x', 10)
                        cartn_y_idx = header_cols.get('Cartn_y', 11)
                        cartn_z_idx = header_cols.get('Cartn_z', 12)
                        
                        if len(parts) > max(cartn_x_idx, cartn_y_idx, cartn_z_idx):
                            label_atom = parts[label_atom_id_idx] if label_atom_id_idx < len(parts) else ''
                            
                            if label_atom == 'CA':
                                try:
                                    x = float(parts[cartn_x_idx])
                                    y = float(parts[cartn_y_idx])
                                    z = float(parts[cartn_z_idx])
                                    ca_coords.append([x, y, z])
                                except (ValueError, IndexError):
                                    continue
        
        if len(ca_coords) == 0:
            return None
        return np.array(ca_coords)
    except Exception as e:
        print(f"Error parsing CIF {cif_path}: {e}")
        return None


def parse_structure(file_path: str) -> Optional[np.ndarray]:
    """
    Parse structure file (PDB or CIF) and extract CA atom coordinates.
    
    Args:
        file_path: Path to structure file
        
    Returns:
        Numpy array of CA atom coordinates (N x 3)
    """
    if file_path.lower().endswith('.cif'):
        return parse_cif(file_path)
    elif file_path.lower().endswith('.pdb'):
        return parse_pdb(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return None


def center_coordinates(coords: np.ndarray) -> np.ndarray:
    """Center coordinates at origin."""
    return coords - np.mean(coords, axis=0)


def kabsch_algorithm(P: np.ndarray, Q: np.ndarray) -> tuple:
    """
    Kabsch algorithm for optimal rotation matrix.
    
    Args:
        P: Reference coordinates (N x 3)
        Q: Target coordinates (N x 3)
        
    Returns:
        Rotation matrix R and translation vector t
    """
    # Center both sets of coordinates
    P_centered = center_coordinates(P)
    Q_centered = center_coordinates(Q)
    
    # Compute covariance matrix
    H = P_centered.T @ Q_centered
    
    # SVD
    U, S, Vt = np.linalg.svd(H)
    
    # Rotation matrix
    R = Vt.T @ U.T
    
    # Ensure proper rotation (det(R) = 1)
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T
    
    # Translation vector
    t = np.mean(Q, axis=0) - R @ np.mean(P, axis=0)
    
    return R, t


def calculate_rmsd_pymol(reference_file: str, candidate_file: str) -> float:
    """
    Calculate RMSD using PyMOL's align command.
    Supports both Python API and command-line execution.
    
    Args:
        reference_file: Path to reference structure file (PDB or CIF)
        candidate_file: Path to candidate structure file (PDB or CIF)
        
    Returns:
        RMSD value in Angstroms
    """
    import subprocess
    import tempfile
    
    # Try Python API first
    try:
        import __main__
        __main__.pymol_argv = ['pymol', '-Q', '-c']
        import pymol
        from pymol import cmd
        
        # Initialize PyMOL
        pymol.finish_launching()
        
        # Load structures
        ref_obj = 'ref_structure'
        cand_obj = 'cand_structure'
        
        # Load files (PyMOL supports both PDB and CIF)
        cmd.load(reference_file, ref_obj)
        cmd.load(candidate_file, cand_obj)
        
        # Select CA atoms for alignment
        ref_ca = f"{ref_obj} and name CA"
        cand_ca = f"{cand_obj} and name CA"
        
        # Align structures using PyMOL's align command
        # align mobile to target, returns (RMSD, aligned_atoms, matching_atoms)
        rmsd_result = cmd.align(cand_ca, ref_ca, cycles=5, transform=1, object='aln')
        
        # Extract RMSD from result
        if isinstance(rmsd_result, (list, tuple)) and len(rmsd_result) > 0:
            rmsd = float(rmsd_result[0])
        else:
            # Fallback: use pair_fit
            rmsd = cmd.pair_fit(cand_ca, ref_ca)[0]
        
        # Clean up
        try:
            cmd.delete(ref_obj)
            cmd.delete(cand_obj)
            cmd.delete('aln')
        except:
            pass
        
        return float(rmsd)
        
    except ImportError:
        # Fallback to command-line PyMOL
        print("PyMOL Python API not available, trying command-line execution...")
        
        # Create PyMOL script to calculate and print RMSD
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pml', delete=False) as script_file:
            script_content = f"""
load {reference_file}, ref_structure
load {candidate_file}, cand_structure
align_result = cmd.align("cand_structure and name CA", "ref_structure and name CA", cycles=5, transform=1)
rmsd_value = align_result[0]
print(f"PYMOL_RMSD_VALUE:{{rmsd_value}}")
"""
            script_file.write(script_content)
            script_path = script_file.name
        
        try:
            # Try to find PyMOL executable
            pymol_cmd = None
            for cmd_name in ['pymol', 'pymol2']:
                try:
                    result = subprocess.run(['which', cmd_name] if sys.platform != 'win32' else ['where', cmd_name],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        pymol_cmd = cmd_name
                        break
                except:
                    continue
            
            if not pymol_cmd:
                # Try common paths
                common_paths = [
                    r'C:\Program Files\PyMOL\PyMOL.exe',
                    r'C:\Program Files (x86)\PyMOL\PyMOL.exe',
                    '/usr/bin/pymol',
                    '/usr/local/bin/pymol'
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        pymol_cmd = path
                        break
            
            if not pymol_cmd:
                raise RuntimeError("PyMOL executable not found. Please install PyMOL or use --method kabsch")
            
            # Execute PyMOL script
            cmd_args = [pymol_cmd, '-Q', '-c', '-r', script_path]
            result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=60)
            
            # Parse output for RMSD
            import re
            rmsd = None
            
            # Look for our custom marker
            for line in result.stdout.split('\n') + result.stderr.split('\n'):
                if 'PYMOL_RMSD_VALUE:' in line:
                    match = re.search(r'PYMOL_RMSD_VALUE:([0-9.]+)', line)
                    if match:
                        rmsd = float(match.group(1))
                        break
                elif 'RMSD' in line or 'rmsd' in line.lower():
                    # Try to extract number from RMSD output
                    match = re.search(r'RMSD\s*[=:]\s*([0-9.]+)', line, re.IGNORECASE)
                    if match:
                        rmsd = float(match.group(1))
                        break
                    # Alternative pattern
                    match = re.search(r'RMS\s*[=:]\s*([0-9.]+)', line, re.IGNORECASE)
                    if match:
                        rmsd = float(match.group(1))
                        break
            
            if rmsd is None:
                # Alternative: use PyMOL's pair_fit and parse output
                script_content2 = f"""
load {reference_file}, ref_structure
load {candidate_file}, cand_structure
pair_result = cmd.pair_fit("cand_structure and name CA", "ref_structure and name CA")
rmsd_value = pair_result[0]
print(f"PYMOL_RMSD_VALUE:{{rmsd_value}}")
"""
                with tempfile.NamedTemporaryFile(mode='w', suffix='.pml', delete=False) as script_file2:
                    script_file2.write(script_content2)
                    script_path2 = script_file2.name
                
                result2 = subprocess.run([pymol_cmd, '-Q', '-c', '-r', script_path2],
                                       capture_output=True, text=True, timeout=60)
                
                for line in result2.stdout.split('\n') + result2.stderr.split('\n'):
                    if 'PYMOL_RMSD_VALUE:' in line:
                        match = re.search(r'PYMOL_RMSD_VALUE:([0-9.]+)', line)
                        if match:
                            rmsd = float(match.group(1))
                            break
                
                try:
                    os.unlink(script_path2)
                except:
                    pass
            
            if rmsd is None:
                raise RuntimeError("Could not extract RMSD from PyMOL output")
            
            # Clean up
            try:
                os.unlink(script_path)
            except:
                pass
            
            return float(rmsd)
            
        except Exception as e:
            raise RuntimeError(f"PyMOL command-line execution failed: {e}")
        
    except Exception as e:
        if "ImportError" in str(type(e).__name__):
            raise ImportError("PyMOL is not installed. Please install pymol or use --method kabsch")
        else:
            raise RuntimeError(f"PyMOL RMSD calculation failed: {e}")


def calculate_rmsd_kabsch(reference_file: str, candidate_file: str) -> float:
    """
    Calculate RMSD using Kabsch algorithm (fallback method).
    
    Args:
        reference_file: Path to reference structure file (PDB or CIF)
        candidate_file: Path to candidate structure file (PDB or CIF)
        
    Returns:
        RMSD value in Angstroms
    """
    # Parse structure files
    ref_coords = parse_structure(reference_file)
    cand_coords = parse_structure(candidate_file)
    
    if ref_coords is None:
        raise ValueError(f"No CA atoms found in reference structure: {reference_file}")
    if cand_coords is None:
        raise ValueError(f"No CA atoms found in candidate structure: {candidate_file}")
    
    # Use minimum length
    min_len = min(len(ref_coords), len(cand_coords))
    if min_len < 3:
        raise ValueError(f"Not enough atoms for RMSD calculation (need at least 3, got {min_len})")
    
    ref_subset = ref_coords[:min_len]
    cand_subset = cand_coords[:min_len]
    
    # Align structures using Kabsch algorithm
    R, t = kabsch_algorithm(ref_subset, cand_subset)
    
    # Transform candidate coordinates
    cand_aligned = (R @ cand_subset.T).T + t
    
    # Calculate RMSD
    squared_diff = np.sum((ref_subset - cand_aligned) ** 2, axis=1)
    rmsd = np.sqrt(np.mean(squared_diff))
    
    return float(rmsd)


def calculate_rmsd_biopython(reference_file: str, candidate_file: str) -> float:
    """
    Calculate RMSD using Bio.PDB.Superimposer on CA atoms (first model).
    Supports PDB and CIF via PDBParser/MMCIFParser.
    """
    try:
        from Bio.PDB import PDBParser, MMCIFParser, Superimposer
    except Exception as e:
        raise ImportError(f"Biopython is required: {e}")

    # Choose appropriate parsers
    ref_parser = MMCIFParser(QUIET=True) if reference_file.lower().endswith('.cif') else PDBParser(QUIET=True)
    mob_parser = MMCIFParser(QUIET=True) if candidate_file.lower().endswith('.cif') else PDBParser(QUIET=True)

    ref_struct = ref_parser.get_structure('ref', reference_file)
    mob_struct = mob_parser.get_structure('mob', candidate_file)

    # First model only
    ref_model = next(ref_struct.get_models())
    mob_model = next(mob_struct.get_models())

    ref_cas = [a for a in ref_model.get_atoms() if a.get_id() == 'CA']
    mob_cas = [a for a in mob_model.get_atoms() if a.get_id() == 'CA']
    if len(ref_cas) == 0 or len(mob_cas) == 0:
        raise ValueError("No CA atoms found in one or both structures")

    n = min(len(ref_cas), len(mob_cas))
    if n < 3:
        raise ValueError(f"Not enough atoms for RMSD calculation (need at least 3, got {n})")

    sup = Superimposer()
    sup.set_atoms(ref_cas[:n], mob_cas[:n])
    return float(sup.rms)


def _get_ca_coordinates_biopython(structure_file: str, chain_id: Optional[str] = None) -> np.ndarray:
    """Extract CA coordinates from a PDB or CIF structure; optional chain filter."""
    from Bio.PDB import PDBParser, MMCIFParser
    parser = MMCIFParser(QUIET=True) if structure_file.lower().endswith('.cif') else PDBParser(QUIET=True)
    structure = parser.get_structure('struct', structure_file)
    ca_coords: List[np.ndarray] = []
    for model in structure:
        for chain in model:
            if chain_id and chain.id != chain_id:
                continue
            for residue in chain:
                try:
                    atom = residue['CA']
                    ca_coords.append(atom.get_coord())
                except Exception:
                    continue
    if not ca_coords:
        raise ValueError(f"No CA atoms found in structure {structure_file} (chain={chain_id or 'any'})")
    return np.asarray(ca_coords, dtype=float)


def calculate_rmsd_iterative(reference_file: str,
                             candidate_file: str,
                             chain_ref: Optional[str] = None,
                             chain_mob: Optional[str] = None,
                             cutoff: float = 2.0,
                             max_cycles: int = 5) -> Tuple[float, int, int]:
    """
    Iterative prune alignment on CA atoms using Bio.PDB.Superimposer with Atom objects.

    Returns (rmsd, aligned_atoms, cycles_used).
    """
    from Bio.PDB import PDBParser, MMCIFParser, Superimposer

    # Parse structures and collect CA Atom objects (respect chain filters)
    def get_ca_atoms(structure_path: str, chain_id: Optional[str]) -> List["Atom"]:
        parser = MMCIFParser(QUIET=True) if structure_path.lower().endswith('.cif') else PDBParser(QUIET=True)
        structure = parser.get_structure('s', structure_path)
        model = next(structure.get_models())
        atoms = []
        for chain in model:
            if chain_id and chain.id != chain_id:
                continue
            for residue in chain:
                atom = residue.child_dict.get('CA') if hasattr(residue, 'child_dict') else None
                if atom is not None:
                    atoms.append(atom)
        return atoms

    ref_atoms = get_ca_atoms(reference_file, chain_ref)
    mob_atoms = get_ca_atoms(candidate_file, chain_mob)

    if len(ref_atoms) == 0 or len(mob_atoms) == 0:
        raise ValueError("No CA atoms found in one or both structures for iterative alignment")

    n = min(len(ref_atoms), len(mob_atoms))
    if n < 3:
        raise ValueError(f"Not enough atoms for RMSD calculation (need at least 3, got {n})")
    ref_atoms = ref_atoms[:n]
    mob_atoms = mob_atoms[:n]

    # Coordinate matrices for distance computation
    ref_coords_all = np.asarray([a.get_coord() for a in ref_atoms], dtype=float)
    mob_coords_all = np.asarray([a.get_coord() for a in mob_atoms], dtype=float)

    mask = np.ones(n, dtype=bool)
    distances = None
    used_cycles = 0
    sup = Superimposer()

    for cycle in range(max_cycles):
        used_cycles = cycle + 1
        # Filter Atom lists by current mask
        ref_inliers = [atom for atom, keep in zip(ref_atoms, mask) if keep]
        mob_inliers = [atom for atom, keep in zip(mob_atoms, mask) if keep]
        if len(ref_inliers) < 3 or len(mob_inliers) < 3:
            break
        sup.set_atoms(ref_inliers, mob_inliers)
        R, t = sup.rotran
        mob_aligned = (R @ mob_coords_all.T).T + t
        distances = np.linalg.norm(ref_coords_all - mob_aligned, axis=1)
        new_mask = distances < cutoff
        if np.array_equal(new_mask, mask):
            break
        if not np.any(new_mask):
            break
        mask = new_mask

    if distances is None:
        raise RuntimeError("Iterative alignment failed to compute distances")

    if not np.any(mask):
        raise ValueError("All atoms pruned; try increasing cutoff or cycles")

    final_rmsd = float(np.sqrt(np.mean((distances[mask]) ** 2)))
    aligned_atoms = int(np.sum(mask))
    return final_rmsd, aligned_atoms, used_cycles


def calculate_rmsd(reference_file: str, candidate_file: str, method: str = 'biopython', *,
                   chain_ref: Optional[str] = None,
                   chain_mob: Optional[str] = None,
                   cutoff: float = 2.0,
                   cycles: int = 5) -> float:
    """
    Calculate RMSD between two structure files.
    
    Args:
        reference_file: Path to reference structure file (PDB or CIF)
        candidate_file: Path to candidate structure file (PDB or CIF)
        method: Calculation method ('biopython' or 'kabsch')
        
    Returns:
        RMSD value in Angstroms
    """
    if method == 'biopython':
        try:
            return calculate_rmsd_biopython(reference_file, candidate_file)
        except Exception as e:
            print(f"Warning: BioPython method failed ({e}), falling back to Kabsch algorithm")
            return calculate_rmsd_kabsch(reference_file, candidate_file)
    if method == 'pymol':
        return calculate_rmsd_pymol(reference_file, candidate_file)
    if method == 'iterative':
        rmsd, _, _ = calculate_rmsd_iterative(
            reference_file,
            candidate_file,
            chain_ref=chain_ref,
            chain_mob=chain_mob,
            cutoff=cutoff,
            max_cycles=cycles,
        )
        return rmsd
    return calculate_rmsd_kabsch(reference_file, candidate_file)


def compare_structures(reference_pdb: str,
                       candidate_pdbs: List[str],
                       output_csv: str,
                       method: str = 'biopython',
                       *,
                       chain_ref: Optional[str] = None,
                       chain_mob: Optional[str] = None,
                       cutoff: float = 2.0,
                       cycles: int = 5) -> pd.DataFrame:
    """
    Compare multiple candidate structures against a reference structure.
    
    Args:
        reference_pdb: Path to reference PDB file
        candidate_pdbs: List of paths to candidate PDB files
        output_csv: Path to output CSV file
        
    Returns:
        DataFrame with RMSD results
    """
    results = []
    
    for i, cand_pdb in enumerate(candidate_pdbs):
        try:
            rmsd = calculate_rmsd(
                reference_pdb,
                cand_pdb,
                method=method,
                chain_ref=chain_ref,
                chain_mob=chain_mob,
                cutoff=cutoff,
                cycles=cycles,
            )
            results.append({
                'Structure_ID': i + 1,
                'Candidate_PDB': os.path.basename(cand_pdb),
                'RMSD_Angstroms': round(rmsd, 3),
                'Status': 'Good' if rmsd < 2.0 else 'High deviation'
            })
        except Exception as e:
            results.append({
                'Structure_ID': i + 1,
                'Candidate_PDB': os.path.basename(cand_pdb),
                'RMSD_Angstroms': None,
                'Status': f'Error: {str(e)}'
            })
    
    df = pd.DataFrame(results)
    df = df.sort_values('RMSD_Angstroms', ascending=True, na_position='last')
    df['Rank'] = range(1, len(df) + 1)
    
    if output_csv:
        df.to_csv(output_csv, index=False)
        print(f"Results saved to: {output_csv}")
    
    return df


def main():
    parser = argparse.ArgumentParser(
        description='Calculate RMSD between reference and predicted PDB structures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare single structure (using PyMOL by default)
  python run_rmsd.py --reference ref.pdb --candidate pred.pdb
  
  # Compare multiple structures using PyMOL
  python run_rmsd.py --reference ref.pdb --candidates pred1.pdb pred2.pdb pred3.pdb --output results.csv
  
  # Compare structures in a directory using Kabsch algorithm (if PyMOL unavailable)
  python run_rmsd.py --reference ref.pdb --candidate-dir ./structures --output results.csv --method kabsch
  
Note: PyMOL installation:
  - Python API: pip install pymol-open-source
  - Standalone: Download from https://pymol.org/2/
  
  If PyMOL is not installed, the script will automatically fall back to the Kabsch algorithm.
        """
    )
    
    parser.add_argument('--reference', type=str, required=True,
                       help='Path to reference structure file (PDB or CIF)')
    parser.add_argument('--candidate', type=str, nargs='?',
                       help='Path to single candidate structure file (PDB or CIF)')
    parser.add_argument('--candidates', type=str, nargs='+',
                       help='Paths to multiple candidate structure files (PDB or CIF)')
    parser.add_argument('--candidate-dir', type=str,
                       help='Directory containing candidate structure files')
    parser.add_argument('--output', type=str, default='rmsd_results.csv',
                       help='Output CSV file path (default: rmsd_results.csv)')
    parser.add_argument('--outdir', type=str, default=os.path.join('web_service', 'results'),
                       help='Output directory for results (default: web_service/results)')
    parser.add_argument('--method', type=str, choices=['biopython', 'kabsch', 'iterative', 'pymol'], default='biopython',
                       help='RMSD calculation method: biopython (default), kabsch, iterative (prune), or pymol (refined)')
    parser.add_argument('--chain-ref', type=str, default=None,
                       help='Chain ID to use for reference structure (iterative)')
    parser.add_argument('--chain-mob', type=str, default=None,
                       help='Chain ID to use for candidate structure (iterative)')
    parser.add_argument('--cutoff', type=float, default=2.0,
                       help='Inlier cutoff (Å) for iterative prune alignment (default: 2.0)')
    parser.add_argument('--cycles', type=int, default=5,
                       help='Maximum cycles for iterative prune alignment (default: 5)')
    
    args = parser.parse_args()
    
    # Validate reference structure
    if not os.path.exists(args.reference):
        print(f"Error: Reference structure file not found: {args.reference}")
        sys.exit(1)
    
    # Collect candidate structure files
    candidate_pdbs = []
    
    if args.candidate:
        if not os.path.exists(args.candidate):
            print(f"Error: Candidate structure file not found: {args.candidate}")
            sys.exit(1)
        candidate_pdbs.append(args.candidate)
    
    if args.candidates:
        for cand in args.candidates:
            if not os.path.exists(cand):
                print(f"Warning: Candidate structure file not found: {cand}")
                continue
            candidate_pdbs.append(cand)
    
    if args.candidate_dir:
        if not os.path.isdir(args.candidate_dir):
            print(f"Error: Candidate directory not found: {args.candidate_dir}")
            sys.exit(1)
        for file in os.listdir(args.candidate_dir):
            if file.lower().endswith(('.pdb', '.cif')):
                candidate_pdbs.append(os.path.join(args.candidate_dir, file))
    
    if not candidate_pdbs:
        print("Error: No candidate PDB files specified")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.outdir, exist_ok=True)
    output_path = os.path.join(args.outdir, args.output)
    
    # Calculate RMSD
    print(f"Reference structure: {args.reference}")
    print(f"Number of candidate structures: {len(candidate_pdbs)}")
    print("Calculating RMSD...")
    
    try:
        results_df = compare_structures(
            args.reference,
            candidate_pdbs,
            output_csv=output_path,
            method=args.method,
            chain_ref=args.chain_ref,
            chain_mob=args.chain_mob,
            cutoff=args.cutoff,
            cycles=args.cycles,
        )
        
        print("\nRMSD Results:")
        print("=" * 60)
        try:
            print(results_df.to_string(index=False))
        except UnicodeEncodeError:
            # Fallback for Windows console encoding issues
            print(results_df.to_string(index=False).encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
        print("=" * 60)
        
        print(f"\nSummary:")
        print(f"Total structures compared: {len(results_df)}")
        valid_rmsd = results_df[results_df['RMSD_Angstroms'].notna()]
        if len(valid_rmsd) > 0:
            print(f"Structures with RMSD < 2.0 Angstroms: {len(valid_rmsd[valid_rmsd['RMSD_Angstroms'] < 2.0])}")
            avg_rmsd = valid_rmsd['RMSD_Angstroms'].mean()
            print(f"Average RMSD: {avg_rmsd:.3f} Angstroms")
            print(f"Min RMSD: {valid_rmsd['RMSD_Angstroms'].min():.3f} Angstroms")
            print(f"Max RMSD: {valid_rmsd['RMSD_Angstroms'].max():.3f} Angstroms")
        else:
            print("No valid RMSD calculations completed")
        
    except Exception as e:
        print(f"Error calculating RMSD: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

