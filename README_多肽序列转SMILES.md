# 多肽序列转SMILES工具

这是一个用于将多肽序列转换为SMILES分子表示法的Python工具，支持天然氨基酸和非天然氨基酸。

## 功能特性

- ✅ 支持20种标准天然氨基酸
- ✅ 支持多种非天然氨基酸和修饰氨基酸
- ✅ 支持D型氨基酸
- ✅ 自动生成肽键连接
- ✅ 分子性质计算
- ✅ 分子结构可视化
- ✅ 多格式导出（SDF、PDB、MOL2）
- ✅ 完整的错误处理和验证

## 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包：
- `rdkit`: 化学信息学工具包
- `matplotlib`: 绘图库
- `numpy`: 数值计算
- `Pillow`: 图像处理

## 使用方法

### 基本使用

```python
from 多肽序列_to_SMILES import PeptideProcessor

# 创建处理器
processor = PeptideProcessor()

# 定义肽序列
sequence = ["Ala", "Gly", "Val", "Leu"]

# 生成SMILES
smiles = processor.build_peptide_smiles(sequence)
print(f"SMILES: {smiles}")

# 创建分子对象
mol = processor.create_molecule()

# 获取分子性质
properties = processor.get_molecular_properties()
print(properties)

# 可视化分子结构
processor.visualize_molecule(save_path="molecule.png")

# 导出分子文件
processor.export_molecule("molecule.sdf", "sdf")
```

### 支持的氨基酸

#### 天然氨基酸（20种）
- **非极性**: Ala, Val, Leu, Ile, Pro, Phe, Trp, Met
- **极性**: Ser, Thr, Cys, Tyr, Asn, Gln
- **带正电荷**: Lys, Arg, His
- **带负电荷**: Asp, Glu
- **特殊**: Gly

#### 非天然氨基酸
- **D型氨基酸**: D-Ala, D-Arg, D-Asp, D-Val, D-Leu, D-Ile, D-Ser, D-Thr, D-His, D-Gln
- **修饰氨基酸**: 5FPhe, Har, Tyr(Me), Orn, Abu, Nle, Aib, Sar, Hyp, Pip, Cha, Phg

### 自定义氨基酸

```python
# 自定义氨基酸字典
custom_aa_dict = {
    "Ala": "N[C@@H](C)C(=O)",
    "CustomAA": "N[C@@H](CCCC)C(=O)"  # 自定义氨基酸
}

# 使用自定义字典创建处理器
processor = PeptideProcessor(custom_aa_dict)
```

## 输出文件

运行脚本后，会在 `peptide_output` 目录下生成以下文件：

- `peptide_structure.png`: 分子结构图
- `peptide.sdf`: SDF格式分子文件
- `peptide.pdb`: PDB格式分子文件

## 分子性质

工具可以计算以下分子性质：

- `molecular_weight`: 分子量
- `logp`: 脂水分配系数
- `tpsa`: 拓扑极性表面积
- `hbd`: 氢键供体数量
- `hba`: 氢键受体数量
- `rotatable_bonds`: 可旋转键数量
- `aromatic_rings`: 芳香环数量

## 注意事项

1. **SMILES格式**: 确保氨基酸的SMILES表示法正确，特别是手性中心（@@H表示L型，@H表示D型）
2. **肽键连接**: 工具会自动处理肽键连接，确保化学结构正确
3. **3D坐标**: 如果3D坐标生成失败，会自动回退到2D坐标
4. **错误处理**: 遇到未定义的氨基酸会给出警告并停止处理

## 示例输出

```
============================================================
肽序列信息摘要
============================================================
序列长度: 29 个氨基酸
序列: Tyr-D-Arg-Asp-Ala-Ile-5FPhe-Thr-Ala-Har-Tyr(Me)-His-Orn-Val-Leu-Abu-Gln-Leu-Ser-Ala-His-Orn-Leu-Leu-Gln-Asp-Ile-Nle-D-Arg-Har
SMILES: N[C@@H](CC1=CC=C(O)C=C1)C(=O)N[C@H](CCCNC(N)=N)C(=O)...

分子性质:
  molecular_weight: 3456.78
  logp: -12.34
  tpsa: 567.89
  hbd: 15
  hba: 32
  rotatable_bonds: 28
  aromatic_rings: 3
============================================================
```

## 扩展功能

可以根据需要扩展以下功能：

1. 添加更多非天然氨基酸
2. 支持环肽结构
3. 添加二级结构预测
4. 集成分子对接功能
5. 批量处理多个序列

## 许可证

本项目采用MIT许可证。
