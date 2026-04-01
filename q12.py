"""
Q12 – Summarize Data & Present Results as Charts and Graphs
Dataset: student_dataset_30x30.csv
Charts:  1) Bar  2) Scatter  3) Pie  4) Stair (Step)  5) Line
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv('student_dataset_30x30.csv')
df_clean = df.dropna()   # use clean rows where needed

PALETTE = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f',
           '#edc948','#b07aa1','#ff9da7','#9c755f','#bab0ac']

# ══════════════════════════════════════════════════════════════════
# 1. BAR CHART – Average subject scores
# ══════════════════════════════════════════════════════════════════
score_cols = ['Math_Score','Science_Score','English_Score',
              'History_Score','PE_Score','Art_Score']
means = df[score_cols].mean().round(2)
labels = [c.replace('_Score','') for c in score_cols]

fig1, ax1 = plt.subplots(figsize=(10, 5))
bars = ax1.bar(labels, means.values, color=PALETTE[:6],
               edgecolor='white', linewidth=0.8, zorder=3)

ax1.set_facecolor('#f9f9f9')
ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax1.set_title('Q12 – Chart 1: Average Subject Scores (Bar Chart)',
              fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Subject',  fontsize=11)
ax1.set_ylabel('Average Score (out of 100)', fontsize=11)
ax1.set_ylim(0, 110)

# Value labels on bars
for bar, val in zip(bars, means.values):
    ax1.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1.5, f'{val}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('q12_chart1_bar.png', dpi=130, bbox_inches='tight')
plt.show()
print("✓ Chart 1 (Bar) saved.")

# ══════════════════════════════════════════════════════════════════
# 2. SCATTER PLOT – Study Hours vs GPA (coloured by Grade)
# ══════════════════════════════════════════════════════════════════
grade_color = {'A':'#2ca02c','B':'#1f77b4','C':'#ff7f0e','D':'#d62728','F':'#9467bd'}

fig2, ax2 = plt.subplots(figsize=(9, 6))

for grade, grp in df_clean.groupby('Grade'):
    ax2.scatter(grp['Study_Hours'], grp['GPA'],
                color=grade_color.get(grade,'grey'),
                label=f'Grade {grade}',
                s=100, edgecolors='white', linewidths=0.6,
                alpha=0.88, zorder=4)

# Trend line
x_val = df_clean['Study_Hours'].values
y_val = df_clean['GPA'].values
m, b  = np.polyfit(x_val, y_val, 1)
xs    = np.linspace(x_val.min(), x_val.max(), 100)
ax2.plot(xs, m*xs + b, '--', color='black', lw=1.5, label=f'Trend (slope={m:.3f})')

ax2.set_facecolor('#f9f9f9')
ax2.set_xlabel('Study Hours per Day', fontsize=11)
ax2.set_ylabel('GPA (out of 10)', fontsize=11)
ax2.set_title('Q12 – Chart 2: Study Hours vs GPA (Scatter Plot)',
              fontsize=13, fontweight='bold', pad=12)
ax2.legend(title='Grade', fontsize=9, title_fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('q12_chart2_scatter.png', dpi=130, bbox_inches='tight')
plt.show()
print("✓ Chart 2 (Scatter) saved.")

# ══════════════════════════════════════════════════════════════════
# 3. PIE CHART – Grade distribution
# ══════════════════════════════════════════════════════════════════
grade_counts = df['Grade'].value_counts().reindex(['A','B','C','D','F'], fill_value=0)
explode = [0.07 if g == grade_counts.idxmax() else 0 for g in grade_counts.index]

fig3, ax3 = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax3.pie(
    grade_counts.values,
    labels=grade_counts.index,
    autopct='%1.1f%%',
    explode=explode,
    colors=['#2ca02c','#1f77b4','#ff7f0e','#d62728','#9467bd'],
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor='white', linewidth=1.5),
    textprops=dict(fontsize=12)
)
for at in autotexts:
    at.set_fontweight('bold')

ax3.set_title('Q12 – Chart 3: Grade Distribution (Pie Chart)',
              fontsize=13, fontweight='bold', pad=15)
ax3.legend(wedges, [f'Grade {g}: {v} students'
                    for g, v in zip(grade_counts.index, grade_counts.values)],
           loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('q12_chart3_pie.png', dpi=130, bbox_inches='tight')
plt.show()
print("✓ Chart 3 (Pie) saved.")

# ══════════════════════════════════════════════════════════════════
# 4. STAIR (STEP) CHART – Attendance % by Student Rank
# ══════════════════════════════════════════════════════════════════
ranked_df = df_clean.sort_values('Rank')[['Rank','Attendance_Pct','Name']].reset_index(drop=True)

fig4, ax4 = plt.subplots(figsize=(12, 5))
ax4.step(ranked_df['Rank'], ranked_df['Attendance_Pct'],
         where='mid', color='#4e79a7', lw=2.5, zorder=3, label='Attendance %')
ax4.fill_between(ranked_df['Rank'], ranked_df['Attendance_Pct'],
                 step='mid', alpha=0.18, color='#4e79a7')

ax4.axhline(ranked_df['Attendance_Pct'].mean(), color='#e15759',
            linestyle='--', lw=1.5, label=f"Mean = {ranked_df['Attendance_Pct'].mean():.1f}%")

ax4.set_facecolor('#f9f9f9')
ax4.set_xlabel('Student Rank (1 = Highest GPA)', fontsize=11)
ax4.set_ylabel('Attendance %', fontsize=11)
ax4.set_title('Q12 – Chart 4: Attendance % by Rank (Stair/Step Chart)',
              fontsize=13, fontweight='bold', pad=12)
ax4.legend(fontsize=10)
ax4.grid(True, linestyle='--', alpha=0.4, zorder=0)
ax4.set_ylim(0, 115)
ax4.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig('q12_chart4_stair.png', dpi=130, bbox_inches='tight')
plt.show()
print("✓ Chart 4 (Stair) saved.")

# ══════════════════════════════════════════════════════════════════
# 5. LINE CHART – Subject score trends across top 15 students
# ══════════════════════════════════════════════════════════════════
top15 = df_clean.sort_values('GPA', ascending=False).head(15).reset_index(drop=True)
top15['Label'] = top15['Name'].str[:4] + '.' + top15['Rank'].astype(str)

fig5, ax5 = plt.subplots(figsize=(13, 6))
line_styles = ['-', '--', '-.', ':', '-']
marker_list = ['o', 's', '^', 'D', 'v']

for col, ls, mk, c in zip(score_cols, line_styles, marker_list, PALETTE[:6]):
    ax5.plot(top15['Label'], top15[col],
             linestyle=ls, marker=mk, color=c,
             lw=2, markersize=5, alpha=0.9,
             label=col.replace('_Score',''))

ax5.set_facecolor('#f9f9f9')
ax5.set_xlabel('Student (Name.Rank)', fontsize=10)
ax5.set_ylabel('Score', fontsize=11)
ax5.set_title('Q12 – Chart 5: Subject Score Trends – Top 15 Students (Line Chart)',
              fontsize=13, fontweight='bold', pad=12)
ax5.legend(title='Subject', fontsize=9, title_fontsize=9, loc='lower left')
ax5.grid(True, linestyle='--', alpha=0.4)
plt.xticks(rotation=35, ha='right', fontsize=8)

plt.tight_layout()
plt.savefig('q12_chart5_line.png', dpi=130, bbox_inches='tight')
plt.show()
print("✓ Chart 5 (Line) saved.")

print("\n✓ Q12 COMPLETE – All 5 charts saved.")