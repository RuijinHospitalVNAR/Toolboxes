import pandas as pd
import numpy as np
import sys
import os
import argparse

# 输入文件路径（请确保路径存在）
DEFAULT_CSV_PATH = r"f:\H盘备份\课题相关\VLPs从头设计-计算机辅助\deimmunology VLPs设计\Based on P03146\新框架\de novo design-proteinMPNN\HBcout\6htx_out-降原\两位点\seq a\seq-a .csv"


def normalize_allele(allele_label: str) -> str:
    """将 DRB1_0101 转换为 DRB1*01:01"""
    try:
        code = allele_label.split('_')[1]
        return f"DRB1*{code[:2]}:{code[2:]}"
    except Exception:
        return allele_label


def main():
    parser = argparse.ArgumentParser(description='Compute wy2-aligned immunogenicity scores (per-row + seqsum).')
    parser.add_argument('input', nargs='?', default=DEFAULT_CSV_PATH, help='Input CSV/XLS/XLSX path')
    parser.add_argument('mode', nargs='?', default='reduce', choices=['reduce', 'enhance'], help='Mode: reduce or enhance')
    parser.add_argument('--outdir', default=os.path.join('web_service', 'results'), help='Output directory for results')
    args = parser.parse_args() if len(sys.argv) > 1 else argparse.Namespace(input=DEFAULT_CSV_PATH, mode='reduce', outdir=os.path.join('web_service','results'))

    csv_path = args.input
    mode = args.mode
    outdir = args.outdir

    # 读取原始两行表头 + 数据（支持csv/txt/xls/xlsx）
    ext = os.path.splitext(csv_path)[1].lower()
    if ext in ('.xlsx', '.xls'):
        try:
            raw = pd.read_excel(csv_path, header=None, dtype=str)
        except Exception:
            # 退回为以制表符读取
            raw = pd.read_csv(csv_path, header=None, dtype=str, sep='\t', engine='python')
    else:
        raw = pd.read_csv(csv_path, header=None, dtype=str, encoding='utf-8', engine='python')
    if raw.shape[0] < 2:
        raise ValueError("文件格式异常：需要至少两行表头（allele 行 + 字段行）")

    header_alleles = list(raw.iloc[0].fillna(''))
    header_fields = list(raw.iloc[1].fillna(''))

    data = raw.iloc[2:].reset_index(drop=True)
    data.columns = pd.MultiIndex.from_arrays([header_alleles, header_fields])

    # 基础列：仅限第一个等位基因块之前的空 allele 列，以及尾部 Ave/NB
    try:
        first_allele_idx = next(i for i, a in enumerate(header_alleles) if a and a.startswith('DRB1_'))
    except StopIteration:
        first_allele_idx = len(header_alleles)

    base_map = {'Pos': 'Pos', 'Peptide': 'Peptide', 'ID': 'ID', 'Target': 'Target', 'Ave': 'Ave', 'NB': 'NB'}
    base_df = pd.DataFrame()

    # 前缀基础列（如 Pos, Peptide, ID, Target）
    for i in range(first_allele_idx):
        a, f = header_alleles[i], header_fields[i]
        col = (a, f)
        if a == '' and col in data.columns and f in base_map:
            base_df[base_map[f]] = data[col].astype(str)

    # 尾部 Ave/NB（如果存在）
    for i in range(len(header_fields)):
        a, f = header_alleles[i], header_fields[i]
        if a == '' and f in ('Ave', 'NB'):
            col = (a, f)
            if col in data.columns:
                base_df[base_map[f]] = data[col].astype(str)

    # 收集等位基因 nM(IC50)
    # 逐列扫描，携带最近一次出现的等位基因标签，将其赋予后续字段
    ic50_cols = {}
    current_allele = None
    for i in range(len(header_fields)):
        a_raw = header_alleles[i]
        f_raw = header_fields[i]
        if a_raw and a_raw.startswith('DRB1_'):
            current_allele = normalize_allele(a_raw)
        if f_raw == 'nM' and current_allele is not None:
            col = (header_alleles[i], header_fields[i])
            # 实际数据在该列（即使 allele 头为空，因为我们用 current_allele 记忆）
            # 通过单层位置选取，避免 MultiIndex 匹配失败
            series = data.iloc[:, i].astype(str)
            ic50_cols[current_allele] = series

    ic50_df = pd.DataFrame(ic50_cols)
    ic50_df = ic50_df.apply(pd.to_numeric, errors='coerce')

    total_rows = len(data)
    # 优先从原始 data 中取 ('', 'Peptide')，否则用 base_df 或占位符
    if ('', 'Peptide') in data.columns:
        peptides_series = data.loc[:, ('', 'Peptide')]
        if isinstance(peptides_series, pd.DataFrame):
            peptides_series = peptides_series.iloc[:, 0]
        peptides_series = peptides_series.astype(str)
    elif 'Peptide' in base_df.columns:
        peptides_series = base_df['Peptide'].astype(str)
    else:
        peptides_series = pd.Series([f"pep_{i}" for i in range(total_rows)], dtype=str)
    peptides = peptides_series.reset_index(drop=True)

    # 与 wy2-score sum.py 对齐：按等位基因做排名 → 线性缩放得分（Rank 越小得分越高）
    score_df = pd.DataFrame(index=ic50_df.index)
    for allele in ic50_df.columns:
        ranks = ic50_df[allele].rank(method='average')
        min_rank = ranks.min()
        max_rank = ranks.max()
        denom = (max_rank - min_rank) if (max_rank - min_rank) != 0 else np.nan
        # rank-norm: 0..100，rank小→分数小
        score = ((ranks - min_rank) / denom) * 100.0
        score_df[f'Score_{allele}'] = score.fillna(50.0)

    # Overall Score（sum across alleles）
    if mode == 'reduce':
        # 降原：弱结合好（分大好），统一最小化 → 取反
        overall_score_sum = (100.0 - score_df).sum(axis=1, skipna=True)
    else:
        # 升原：强结合好（分小好），直接求和并最小化
        overall_score_sum = score_df.sum(axis=1, skipna=True)

    # 统一长度
    n = ic50_df.shape[0]
    peptides_vals = peptides.iloc[:n].astype(str).tolist()
    # Align IDs if available
    id_series = None
    if 'ID' in base_df.columns:
        id_series = base_df['ID'].astype(str).reset_index(drop=True).iloc[:n]
    allele_count_vals = ic50_df.notna().sum(axis=1).iloc[:n].astype(int).tolist()
    best_ic50_vals = ic50_df.min(axis=1, skipna=True).round(2).iloc[:n].astype(float).tolist()
    overall_vals = overall_score_sum.round(3).iloc[:n].astype(float).tolist()

    out = pd.DataFrame({
        'Peptide': peptides_vals,
        'ID': id_series.values if id_series is not None else [None]*n,
        'Allele_Count': allele_count_vals,
        'Best_IC50(nM)': best_ic50_vals,
        'Overall_Score_Sum': overall_vals,
    })
    out = out.sort_values('Overall_Score_Sum', ascending=(mode=='reduce')).reset_index(drop=True)

    # 保存结果
    try:
        os.makedirs(outdir, exist_ok=True)
        base = os.path.splitext(os.path.basename(csv_path))[0]
        out_path = os.path.join(outdir, f"{base}_{mode}_wy2_scores.csv")
        out.reset_index().to_csv(out_path, index=False)
        # Sequence-level aggregation if ID present
        if 'ID' in out.columns:
            seq_sum = out.reset_index().groupby('ID', dropna=False)['Overall_Score_Sum'].sum().reset_index()
            seq_sum = seq_sum.sort_values('Overall_Score_Sum', ascending=True)
            seq_path = os.path.join(outdir, f"{base}_{mode}_wy2_seqsum.csv")
            seq_sum.to_csv(seq_path, index=False)
        print(f"Saved: {out_path}")
    except Exception as e:
        print(f"Save failed: {e}")

    # 打印前10
    print("前10个（与 wy2 规则一致，Overall Score 越小越好）：")
    try:
        print(out.head(10).to_string())
    except Exception:
        print(out.head(10))

    print("\n统计：")
    print(f"总肽段数: {len(out)}")
    print(f"等位基因列数: {ic50_df.shape[1]}")


if __name__ == "__main__":
    main()


