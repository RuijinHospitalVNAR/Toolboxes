#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Circular ribbon contact map tool

Usage examples:
  # From an edges.csv (columns: source,target[,distance]) draw interactive HTML
  python circular_ribbon_contact_map.py edges.csv --output contact_map.html

  # From an mmCIF and two chains, extract sequences/contacts, then draw
  python circular_ribbon_contact_map.py --cif complex.cif --chain1 H --chain2 L --cutoff 5.0 --output H_L_contact_map.html

This file is mirrored from the author's local script so that users can
download and run it directly from the Toolboxes repository.
"""

import pandas as pd
import holoviews as hv
from holoviews import opts
import argparse
import sys
import os
from Bio.PDB import MMCIFParser, is_aa
from Bio.Data import IUPACData
import csv
import re
import matplotlib.pyplot as plt  # noqa: F401 (kept for parity with original)
import matplotlib.colors as mcolors

hv.extension('bokeh')

three_to_one = IUPACData.protein_letters_3to1


def aa3to1(resname):
    return three_to_one.get(resname.capitalize(), 'X')


def residue_label(chain_id, res):
    return f"{chain_id}_{res.get_resname()}_{res.get_id()[1]}"


def extract_chain_sequence(cif_file, chain_id):
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure('struct', cif_file)
    seq = []
    res_ids = []
    for model in structure:
        for chain in model:
            if chain.id == chain_id:
                for res in chain:
                    if is_aa(res, standard=True) and res.id[0] == ' ':
                        seq.append(aa3to1(res.get_resname()))
                        res_ids.append(res.id[1])
    return ''.join(seq), res_ids


def extract_contacts_from_cif(cif_file, chain1, chain2, cutoff=5.0):
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure('struct', cif_file)
    residues1 = []
    residues2 = []
    for model in structure:
        for chain in model:
            if chain.id == chain1:
                for res in chain:
                    if is_aa(res, standard=True) and res.id[0] == ' ':
                        residues1.append(res)
            elif chain.id == chain2:
                for res in chain:
                    if is_aa(res, standard=True) and res.id[0] == ' ':
                        residues2.append(res)
    contacts = []
    contacts_detail = []
    for res1 in residues1:
        for res2 in residues2:
            found = False
            for atom1 in res1:
                for atom2 in res2:
                    if atom1.element != 'H' and atom2.element != 'H':
                        dist = atom1 - atom2
                        if dist <= cutoff:
                            label1 = residue_label(chain1, res1)
                            label2 = residue_label(chain2, res2)
                            contacts.append((label1, label2))
                            contacts_detail.append({
                                'chain1': chain1,
                                'res1_num': res1.id[1],
                                'res1_name': res1.get_resname(),
                                'chain2': chain2,
                                'res2_num': res2.id[1],
                                'res2_name': res2.get_resname(),
                                'distance': round(dist, 3)
                            })
                            found = True
                            break
                if found:
                    break
    return contacts, contacts_detail


def get_all_residue_labels(cif_file, chain1, chain2):
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure('struct', cif_file)
    labels = []
    for model in structure:
        for chain in model:
            if chain.id in [chain1, chain2]:
                for res in chain:
                    if is_aa(res, standard=True) and res.id[0] == ' ':
                        labels.append(residue_label(chain.id, res))
    return labels


def sort_key(x):
    m = re.search(r'([A-Za-z]+)([A-Za-z]{3})(\d+)', x)
    return int(m.group(3)) if m else 0


def plot_circular_contact_map(edge_file, node_file=None, output_file=None, all_nodes=None, chain1=None, chain2=None):
    try:
        df = pd.read_csv(edge_file)
    except Exception as e:
        print(f"[✘] 读取 {edge_file} 失败，文件内容可能异常或为空。请检查文件格式。\n错误信息: {e}")
        return
    if df.empty or 'source' not in df.columns or 'target' not in df.columns:
        print(f"[✘] {edge_file} 文件为空或缺少必要的 source/target 列，无法绘图。")
        return

    if all_nodes is not None and chain1 and chain2:
        chain1_nodes = [n for n in all_nodes if n.split('_')[0] == chain1]
        chain2_nodes = [n for n in all_nodes if n.split('_')[0] == chain2]
        other_nodes = [n for n in all_nodes if n.split('_')[0] not in [chain1, chain2]]
        all_nodes = chain2_nodes + other_nodes + chain1_nodes
    elif node_file:
        node_df = pd.read_csv(node_file)
        all_nodes = list(node_df['id'])
    else:
        all_nodes = sorted(set(df['source']) | set(df['target']))

    node_map = {name: i for i, name in enumerate(all_nodes)}
    connected_nodes = set(df['source']).union(set(df['target']))

    chord_data = []
    edge_colors = []
    edge_widths = []
    contact_distance_dict = {}
    if 'distance' in df.columns:
        for idx, row in df.iterrows():
            contact_distance_dict[(row['source'], row['target'])] = row['distance']
            contact_distance_dict[(row['target'], row['source'])] = row['distance']

    for src, tgt in zip(df['source'], df['target']):
        if src in node_map and tgt in node_map:
            chord_data.append((node_map[src], node_map[tgt]))
            edge_colors.append('#FFA500')
            dist = contact_distance_dict.get((src, tgt), None)
            if dist is not None:
                min_d, max_d = 3, 8
                width = 4 - 3.5 * (min(max(dist, min_d), max_d) - min_d) / (max_d - min_d)
            else:
                width = 2
            edge_widths.append(width)

    contact_nodes = set(df['source']).union(set(df['target']))
    chain_resnum = {}
    for n in contact_nodes:
        parts = n.split('_')
        if len(parts) == 3:
            chain, _, num = parts
            chain_resnum.setdefault(chain, []).append(int(num))

    interfaces = []
    for chain, nums in chain_resnum.items():
        nums = sorted(nums)
        current = []
        last = None
        for num in nums:
            if last is not None and num == last + 1:
                current.append(num)
            else:
                if len(current) >= 2:
                    interfaces.append((chain, current))
                current = [num]
            last = num
        if len(current) >= 2:
            interfaces.append((chain, current))

    hydrophobic = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO', 'GLY'}
    polar = {'SER', 'THR', 'TYR', 'ASN', 'GLN'}
    acidic = {'ASP', 'GLU'}
    basic = {'LYS', 'ARG', 'HIS'}

    edge_colors = []
    edge_widths = []
    node_color_map = {}
    for src, tgt in zip(df['source'], df['target']):
        parts = src.split('_')
        color = mcolors.to_rgba('#AAAAAA', alpha=0.75)
        if len(parts) == 3:
            resname = parts[1].upper()
            if resname == 'CYS':
                color = mcolors.to_rgba('#000000', alpha=0.75)
            elif resname in hydrophobic:
                color = mcolors.to_rgba('#FF7744', alpha=0.75)
            elif resname in polar:
                color = mcolors.to_rgba('#87CEFA', alpha=0.75)
            elif resname in acidic:
                color = mcolors.to_rgba('#FF0000', alpha=0.75)
            elif resname in basic:
                color = mcolors.to_rgba('#B565A7', alpha=0.75)
        edge_colors.append(mcolors.to_hex(color))
        edge_widths.append(2)
        node_color_map[src] = mcolors.to_hex(color)
        node_color_map[tgt] = mcolors.to_hex(color)

    labels = [(i, name if name in connected_nodes else '') for name, i in node_map.items()]
    edges = pd.DataFrame({
        'source': [src for src, _ in chord_data],
        'target': [tgt for _, tgt in chord_data],
        'color': edge_colors,
        'value': edge_widths
    })
    nodes = pd.DataFrame(labels, columns=['index', 'name'])
    nodes['index'] = nodes['index'].astype(int)
    nodes = nodes.drop_duplicates(subset=['index']).sort_values('index').reset_index(drop=True)
    nodes['color'] = [node_color_map.get(name, 'rgba(0,0,0,0.4)') for name, _ in labels]

    nodes = hv.Dataset(nodes, 'index', ['name', 'color'])
    chord = hv.Chord((edges, nodes))
    chord.opts(
        opts.Chord(
            edge_color='color',
            edge_line_width='value',
            edge_alpha=1,
            cmap='Category20',
            labels='name',
            node_color='color',
            node_size=15,
            node_marker='s',
            label_text_font_size='8pt',
            label_text_font='Arial',
            width=600,
            height=600
        )
    )

    if output_file:
        if output_file.lower().endswith('.png'):
            html_check = os.path.splitext(output_file)[0] + '_output_check.html'
            hv.save(chord, html_check, backend='bokeh')
            print(f"[i] 已导出 {html_check}，请用浏览器打开确认HTML是否正常显示。")
            try:
                from bokeh.io import export_png
                from holoviews import render
                plot = hv.render(chord, backend='bokeh')
                export_png(plot, filename=output_file)
                print(f"[✔] Saved circular ribbon contact map as PNG to {output_file}")
            except Exception as e:
                print("[✘] PNG export failed. Ensure you have bokeh, selenium, pillow, and a web browser installed.")
                print("Error:", e)
        else:
            hv.save(chord, output_file, backend='bokeh')
            print(f"[✔] Saved circular ribbon contact map to {output_file}")
    else:
        from bokeh.plotting import show
        from holoviews import render
        show(render(chord, backend='bokeh'))


def main():
    parser = argparse.ArgumentParser(description="Plot a circular ribbon contact map from a Cytoscape-style edges.csv file or extract sequence/contact info from mmCIF.")
    parser.add_argument('edge_file', type=str, nargs='?', default=None, help='Input edges.csv file (with columns source,target)')
    parser.add_argument('--nodes', type=str, default=None, help='Optional nodes.csv file (with column id)')
    parser.add_argument('--output', type=str, default=None, help='Output HTML or PNG file (if not set, show interactively)')
    parser.add_argument('--cif', type=str, default=None, help='Input mmCIF file for sequence/contact extraction')
    parser.add_argument('--chain1', type=str, default=None, help='First chain ID in CIF')
    parser.add_argument('--chain2', type=str, default=None, help='Second chain ID in CIF')
    parser.add_argument('--cutoff', type=float, default=5.0, help='Distance cutoff (Å) for contact extraction')
    args = parser.parse_args()

    if args.cif and args.chain1 and args.chain2:
        seq1, _ = extract_chain_sequence(args.cif, args.chain1)
        seq2, _ = extract_chain_sequence(args.cif, args.chain2)
        with open(f"{args.chain1}_sequence.fasta", "w") as f:
            f.write(f">{args.chain1}\n{seq1}\n")
        with open(f"{args.chain2}_sequence.fasta", "w") as f:
            f.write(f">{args.chain2}\n{seq2}\n")
        contacts, contacts_detail = extract_contacts_from_cif(args.cif, args.chain1, args.chain2, args.cutoff)
        contacts_csv = f"{args.chain1}_{args.chain2}_contacts.csv"
        with open(contacts_csv, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['chain1','res1_num','res1_name','chain2','res2_num','res2_name','distance'])
            writer.writeheader()
            for row in contacts_detail:
                writer.writerow(row)
        if args.edge_file is None:
            edge_file = f"{args.chain1}_{args.chain2}_edges.csv"
            pd.DataFrame(contacts, columns=['source','target']).drop_duplicates().to_csv(edge_file, index=False)
            args.edge_file = edge_file

        all_nodes = get_all_residue_labels(args.cif, args.chain1, args.chain2)
        plot_circular_contact_map(args.edge_file, args.nodes, args.output, all_nodes=all_nodes, chain1=args.chain1, chain2=args.chain2)
        return

    if args.edge_file:
        plot_circular_contact_map(args.edge_file, args.nodes, args.output)
    else:
        print("[!] 未指定edge_file，未进行绘图。仅提取了序列和互作信息。")


if __name__ == "__main__":
    main()


