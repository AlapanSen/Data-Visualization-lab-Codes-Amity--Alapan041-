"""
Q11 – Identify Outliers and Missing Data (IF ANY) in the Dataset
Dataset: student_dataset_30x30.csv
Methods: IQR method for outliers | Heatmap for missing data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv('student_dataset_30x30.csv')
num_cols = df.select_dtypes(include='number').columns.tolist()

# ═══════════════════════════════════════════════════════════════════
# PART A – MISSING DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════════
print("=" * 60)
print("          Q11 – MISSING DATA ANALYSIS")
print("=" * 60)

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
missing_df = missing_df[missing_df['Missing Count'] > 0]

if missing_df.empty:
    print("No missing values found in the dataset.")
else:
    print(missing_df.to_string())
    print(f"\nTotal missing cells : {df.isnull().sum().sum()}")
    print(f"Total cells         : {df.size}")
    print(f"Overall missing %   : {df.isnull().sum().sum()/df.size*100:.2f}%")

# Visualise missing data – bar chart
fig1, axes = plt.subplots(1, 2, figsize=(14, 5))
fig1.suptitle('Q11 – Missing Data Visualisation', fontsize=13, fontweight='bold')

# Bar chart of missing %
axes[0].barh(missing_df.index, missing_df['Missing %'], color='#e15759', edgecolor='white')
axes[0].set_xlabel('Missing %')
axes[0].set_title('Missing Value % per Column')
axes[0].set_facecolor('#f9f9f9')
for i, v in enumerate(missing_df['Missing %']):
    axes[0].text(v + 0.3, i, f'{v}%', va='center', fontsize=9)

# Heatmap-style boolean grid for all columns
miss_num = df[num_cols].isnull()
im = axes[1].imshow(miss_num.T.values, cmap='Reds', aspect='auto', interpolation='nearest')
axes[1].set_yticks(range(len(num_cols)))
axes[1].set_yticklabels([c.replace('_','\n') for c in num_cols], fontsize=7)
axes[1].set_xlabel('Student Index')
axes[1].set_title('Missing Value Map (Red = Missing)')
axes[1].set_facecolor('#f9f9f9')

plt.tight_layout()
plt.savefig('q11_missing_data.png', dpi=130, bbox_inches='tight')
plt.show()

# ═══════════════════════════════════════════════════════════════════
# PART B – OUTLIER DETECTION (IQR Method)
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("          Q11 – OUTLIER DETECTION (IQR)")
print("=" * 60)

target_cols = ['Math_Score','Science_Score','PE_Score','Weight_kg',
               'Family_Income_LPA','Attendance_Pct']

outlier_summary = {}
for col in target_cols:
    data = df[col].dropna()
    Q1, Q3 = data.quantile(0.25), data.quantile(0.75)
    IQR    = Q3 - Q1
    lower  = Q1 - 1.5 * IQR
    upper  = Q3 + 1.5 * IQR
    outs   = df[(df[col] < lower) | (df[col] > upper)][['Name', col]]
    outlier_summary[col] = {'Q1': round(Q1,2), 'Q3': round(Q3,2),
                             'IQR': round(IQR,2), 'Lower': round(lower,2),
                             'Upper': round(upper,2), 'Outliers': len(outs)}
    if not outs.empty:
        print(f"\n  {col}:")
        print(f"    IQR bounds → [{lower:.2f}, {upper:.2f}]")
        print(outs.to_string(index=False))

# Box plots for outlier visualisation
fig2, axes2 = plt.subplots(2, 3, figsize=(14, 8))
fig2.suptitle('Q11 – Outlier Detection via Box Plots (IQR Method)', fontsize=13, fontweight='bold')
colors2 = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f','#edc948']

for ax, col, c in zip(axes2.flat, target_cols, colors2):
    data = df[col].dropna()
    bp = ax.boxplot(data, vert=True, patch_artist=True, widths=0.4,
                    boxprops=dict(facecolor=c, color='black', alpha=0.8),
                    medianprops=dict(color='black', lw=2),
                    flierprops=dict(marker='o', color='red', markersize=7,
                                   markerfacecolor='red', label='Outlier'),
                    whiskerprops=dict(color='black', lw=1.2),
                    capprops=dict(color='black', lw=1.5))
    ax.set_title(col.replace('_',' '), fontsize=10, fontweight='bold')
    ax.set_ylabel('Value')
    ax.set_facecolor('#f9f9f9')

    # Annotate outlier values
    Q1, Q3 = data.quantile(0.25), data.quantile(0.75)
    IQR = Q3 - Q1
    outliers = data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)]
    for ov in outliers:
        ax.text(1.12, ov, f' {ov:.1f}', va='center', fontsize=8, color='red')

plt.tight_layout()
plt.savefig('q11_boxplot_outliers.png', dpi=130, bbox_inches='tight')
plt.show()

# ── Summary table ─────────────────────────────────────────────────────────────
print("\n{'OUTLIER SUMMARY TABLE':=^60}")
print(f"{'Column':<25} {'Lower':>8} {'Upper':>8} {'# Outliers':>12}")
print("-" * 55)
for col, info in outlier_summary.items():
    print(f"{col:<25} {info['Lower']:>8.2f} {info['Upper']:>8.2f} {info['Outliers']:>12}")

print("\n✓ Q11 complete – 2 figures saved.")