"""
Q10 – Variable Types and Graphical Data Exploration
Dataset: student_dataset_30x30.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv('student_dataset_30x30.csv')

# ── 1. Variable Type Classification ───────────────────────────────────────────
print("=" * 60)
print("         Q10 – VARIABLE TYPE ANALYSIS")
print("=" * 60)

num_cols  = df.select_dtypes(include=['number']).columns.tolist()
cat_cols  = df.select_dtypes(include=['object']).columns.tolist()

print(f"\n{'NUMERICAL VARIABLES':=^40}")
for c in num_cols:
    unique = df[c].nunique()
    kind   = 'Discrete' if df[c].dropna().apply(lambda x: x == int(x)).all() else 'Continuous'
    print(f"  {c:<25} | {kind}")

print(f"\n{'CATEGORICAL VARIABLES':=^40}")
for c in cat_cols:
    print(f"  {c:<25} | Unique values: {df[c].unique()[:5]}")

print(f"\nTotal Columns : {len(df.columns)}")
print(f"Numerical     : {len(num_cols)}")
print(f"Categorical   : {len(cat_cols)}")

# ── 2. Basic Statistical Summary ──────────────────────────────────────────────
print(f"\n{'DESCRIPTIVE STATISTICS':=^60}")
print(df[num_cols].describe().round(2).to_string())

# ── 3. Graphical Exploration ───────────────────────────────────────────────────
# Figure 1: Distribution of numeric variables (histograms)
score_cols = ['Math_Score','Science_Score','English_Score','History_Score','PE_Score','Art_Score']

fig1, axes = plt.subplots(2, 3, figsize=(14, 7))
fig1.suptitle('Q10 – Score Distributions (Histograms)', fontsize=14, fontweight='bold')
colors = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f','#edc948']

for ax, col, c in zip(axes.flat, score_cols, colors):
    data = df[col].dropna()
    ax.hist(data, bins=8, color=c, edgecolor='white', alpha=0.85)
    ax.axvline(data.mean(), color='black', linestyle='--', lw=1.5, label=f'Mean={data.mean():.1f}')
    ax.set_title(col.replace('_',' '), fontsize=10, fontweight='bold')
    ax.set_xlabel('Score')
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=8)
    ax.set_facecolor('#f9f9f9')

plt.tight_layout()
plt.savefig('q10_score_distributions.png', dpi=130, bbox_inches='tight')
plt.show()

# Figure 2: Categorical variable exploration
fig2, axes2 = plt.subplots(1, 4, figsize=(16, 5))
fig2.suptitle('Q10 – Categorical Variable Distributions', fontsize=13, fontweight='bold')

# Gender
vc = df['Gender'].value_counts()
axes2[0].bar(vc.index, vc.values, color=['#4e79a7','#f28e2b'], edgecolor='white')
axes2[0].set_title('Gender Distribution'); axes2[0].set_ylabel('Count')

# Grade
vc2 = df['Grade'].value_counts().reindex(['A','B','C','D','F'], fill_value=0)
grade_colors = ['#2ca02c','#1f77b4','#ff7f0e','#d62728','#9467bd']
axes2[1].bar(vc2.index, vc2.values, color=grade_colors, edgecolor='white')
axes2[1].set_title('Grade Distribution'); axes2[1].set_ylabel('Count')

# Transport
vc3 = df['Transport'].value_counts()
axes2[2].bar(vc3.index, vc3.values, color='#17becf', edgecolor='white')
axes2[2].set_title('Transport Mode'); axes2[2].set_ylabel('Count')

# Pass/Fail
vc4 = df['Pass_Fail'].value_counts()
axes2[3].bar(vc4.index, vc4.values, color=['#2ca02c','#d62728'], edgecolor='white')
axes2[3].set_title('Pass / Fail'); axes2[3].set_ylabel('Count')

for a in axes2:
    a.set_facecolor('#f9f9f9')

plt.tight_layout()
plt.savefig('q10_categorical_distributions.png', dpi=130, bbox_inches='tight')
plt.show()

# Figure 3: Correlation heatmap of numeric variables
import matplotlib.colors as mcolors

corr_cols = ['Math_Score','Science_Score','English_Score','History_Score',
             'GPA','Study_Hours','Sleep_Hours','Attendance_Pct','BMI']
corr = df[corr_cols].corr()

fig3, ax3 = plt.subplots(figsize=(9, 7))
im = ax3.imshow(corr.values, cmap='RdYlGn', vmin=-1, vmax=1, aspect='auto')
plt.colorbar(im, ax=ax3, shrink=0.8)
ax3.set_xticks(range(len(corr_cols))); ax3.set_xticklabels([c.replace('_','\n') for c in corr_cols], fontsize=8)
ax3.set_yticks(range(len(corr_cols))); ax3.set_yticklabels([c.replace('_','\n') for c in corr_cols], fontsize=8)
ax3.set_title('Q10 – Correlation Heatmap of Numeric Variables', fontsize=12, fontweight='bold')

for i in range(len(corr_cols)):
    for j in range(len(corr_cols)):
        ax3.text(j, i, f'{corr.values[i,j]:.2f}', ha='center', va='center',
                 fontsize=7.5, color='black')

plt.tight_layout()
plt.savefig('q10_correlation_heatmap.png', dpi=130, bbox_inches='tight')
plt.show()

print("\n✓ Q10 complete – 3 figures saved.")
