import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re

df = pd.read_csv("Companies_dataset.csv", index_col=0)

# ─────────────────────────────────────────────
# Question 1: Find the headquarter place names
# ─────────────────────────────────────────────
def extract_hq_city(hq_str):
    if pd.isna(hq_str):
        return "Unknown"
    base = hq_str.split("+")[0].strip()
    city = base.split(",")[0].strip()
    return city

df["hq_city"] = df["hq"].apply(extract_hq_city)
hq_df = df[["name", "hq_city"]].reset_index(drop=True).head(10)

fig1 = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Company</b>", "<b>Headquarter City</b>"],
        fill_color="steelblue",
        font=dict(color="white", size=13),
        align="center",
        height=35
    ),
    cells=dict(
        values=[hq_df["name"], hq_df["hq_city"]],
        fill_color=[["#f0f4f8", "#e0eaf4"] * 5],
        font=dict(size=12),
        align="center",
        height=30
    )
)])
fig1.update_layout(
    title="Question 1: Top 10 Company Headquarters",
    height=450
)
fig1.show()

# ─────────────────────────────────────────────
# Question 2: Funnel Chart – Companies Review Wise
# ─────────────────────────────────────────────

def parse_reviews(rev_str):
    if pd.isna(rev_str):
        return 0
    num = re.sub(r"[^0-9.]", "", rev_str.replace("k", ""))
    try:
        val = float(num)
        if "k" in rev_str.lower() or "k" in rev_str:
            val *= 1000
        return int(val)
    except ValueError:
        return 0

df["review_num"] = df["review_count"].apply(parse_reviews)

top_reviews = df[["name", "review_num"]].sort_values("review_num", ascending=False).head(10)

fig2 = go.Figure(go.Funnel(
    y=top_reviews["name"],
    x=top_reviews["review_num"],
    textinfo="value+percent initial",
    marker=dict(color=px.colors.sequential.Blues_r[:len(top_reviews)])
))
fig2.update_layout(
    title="Funnel Chart: Top 10 Companies by Review Count",
    height=700
)
fig2.show()

# ─────────────────────────────────────────────
# Question 3: Bar Chart – Companies Year Wise
# ─────────────────────────────────────────────

def parse_years(yr_str):
    if pd.isna(yr_str):
        return None
    match = re.search(r"(\d+)", str(yr_str))
    return int(match.group(1)) if match else None

df["age"] = df["years"].apply(parse_years)

top_years = df[["name", "age"]].dropna().sort_values("age", ascending=False).head(10)

fig3 = px.bar(
    top_years,
    x="name",
    y="age",
    color="age",
    color_continuous_scale="Viridis",
    title="Bar Chart: Companies by Age (Years Old) – Top 10",
    labels={"name": "Company", "age": "Age (Years)"}
)
fig3.update_layout(xaxis_tickangle=-45, height=550)
fig3.show()

# ─────────────────────────────────────────────
# Question 4: Line Chart – Companies Rating Wise
# ─────────────────────────────────────────────

df["rating_num"] = pd.to_numeric(df["ratings"], errors="coerce")
rating_df = df[["name", "rating_num"]].dropna().sort_values("rating_num", ascending=False).head(10)

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=rating_df["name"],
    y=rating_df["rating_num"],
    mode="lines+markers",
    line=dict(color="royalblue", width=2),
    marker=dict(size=7, color="orange"),
    text=rating_df["rating_num"],
    textposition="top center"
))
fig4.update_layout(
    title="Line Chart: Top 10 Companies by Rating",
    xaxis_title="Company",
    yaxis_title="Rating (out of 5)",
    xaxis_tickangle=-45,
    height=550,
    yaxis=dict(range=[4.7, 5.05])
)
fig4.show()

# ─────────────────────────────────────────────
# Question 5: Pie Chart – Companies Employees Wise
# ─────────────────────────────────────────────

emp_counts = (
    df["employees"]
    .dropna()
    .str.replace(r"\s*\(India\)", "", regex=True)
    .str.strip()
    .value_counts()
    .head(5)
    .reset_index()
)
emp_counts.columns = ["employee_range", "count"]

fig5 = px.pie(
    emp_counts,
    names="employee_range",
    values="count",
    title="Pie Chart: Companies Distribution by Employee Count Range",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.3
)
fig5.update_traces(textinfo="percent+label")
fig5.update_layout(height=550)
fig5.show()
