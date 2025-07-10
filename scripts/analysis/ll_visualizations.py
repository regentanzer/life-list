import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
sns.set_theme(style="whitegrid", font_scale=1.2)

# Directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
input_life_list = os.path.join(base_dir, "data/life_list_cleaned.csv")
input_taxonomy = os.path.join(base_dir, "data/taxonomy.json")

# Load Data
df = pd.read_csv(input_life_list)
with open(input_taxonomy) as f:
    taxonomy = json.load(f)
tax_df = pd.DataFrame(taxonomy)

merged = pd.merge(df, tax_df[['comName', 'familyComName']], left_on='common_name', right_on='comName', how='left')


# --- 1. Birds seen in each region/state ---
plt.figure(figsize=(8, 6))
region_counts = df['region'].value_counts()
colors = sns.color_palette("crest", len(region_counts))
ax = region_counts.plot(kind='bar', color=colors, edgecolor='black')
plt.title("Birds Seen by Region/State", fontsize=18, weight='bold')
plt.xlabel("Region/State", fontsize=14)
plt.ylabel("Number of Birds", fontsize=14)
ax.set_ylim(0, region_counts.max() * 1.15)
sns.despine()
ax.grid(False)
for i, v in enumerate(region_counts):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold', fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig("life-list/visualizations/ll_birds_by_region.png")
plt.show()

# --- 2. Pie chart of families seen ---
family_counts = merged['familyComName'].value_counts().head(10)  # Top 10 families
labels = [f"{fam} ({count})" for fam, count in zip(family_counts.index, family_counts.values)]

plt.figure(figsize=(8, 8))
colors = sns.color_palette("pastel", len(family_counts))
wedges, texts, autotexts = plt.pie(
    family_counts,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(edgecolor='w', linewidth=1.5),
    colors=colors,
    textprops={'fontsize': 13}
)
plt.setp(autotexts, size=14, weight="bold", color="black")
plt.title("Top 10 Bird Families", fontsize=18, weight='bold')
plt.tight_layout()
plt.savefig("life-list/visualizations/ll_top_families_pie.png")
plt.show()

# --- 3. Cumulative life birds per month/year ---
df['first_observation'] = pd.to_datetime(df['first_observation'])
df['year_month'] = df['first_observation'].dt.to_period('M')
monthly_counts = df.groupby('year_month').size()
cumulative_counts = monthly_counts.cumsum()

plt.figure(figsize=(12, 6))
cumulative_counts.index = cumulative_counts.index.to_timestamp()  # For better x-axis labels
plt.plot(cumulative_counts, marker='o', color=sns.color_palette("crest", 1)[0])
plt.title("Cumulative Life Birds by Month", fontsize=18, weight='bold')
plt.xlabel("Month", fontsize=14)
plt.ylabel("Total Life Birds", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig("life-list/visualizations/ll_cumulative_life_birds.png")
plt.show()

# --- 4. Percentage of hummingbirds seen ---
hummingbirds = tax_df[tax_df['familyComName'] == 'Hummingbirds']
my_hummingbirds = merged[merged['familyComName'] == 'Hummingbirds']['common_name'].nunique()
total_hummingbirds = hummingbirds['comName'].nunique()
percent = 100 * my_hummingbirds / total_hummingbirds

print(f"You've seen {my_hummingbirds} of {total_hummingbirds} hummingbird species ({percent:.2f}%)")

plt.figure(figsize=(6,6))
plt.pie([my_hummingbirds, total_hummingbirds - my_hummingbirds],
        labels=['Seen', 'Not Seen'],
        autopct='%1.1f%%',
        colors=['#4caf50', '#cccccc'],
        wedgeprops=dict(edgecolor='w', linewidth=1.5),
        textprops={'fontsize': 13})
plt.title("Percentage of World Hummingbirds Seen", fontsize=16, weight='bold')
plt.tight_layout()
plt.savefig("life-list/visualizations/ll_hummingbirds_seen_pie.png")
plt.show()

# --- 5. Top 10 families by percent of world seen ---
family_stats = (
    merged.groupby('familyComName')['common_name'].nunique()
    / tax_df.groupby('familyComName')['comName'].nunique()
).sort_values(ascending=False)

top10 = family_stats.head(10) * 100
plt.figure(figsize=(10,6))
colors = sns.color_palette("viridis", len(top10))
ax = top10.plot(kind='bar', color=colors, edgecolor='black')
plt.ylabel("Percent of World Family Seen", fontsize=14)
plt.xlabel("Family", fontsize=14)
plt.title("Top 10 Bird Families by Percent Seen", fontsize=18, weight='bold')
ax.set_ylim(0, top10.max() * 1.15)
total_seen = merged['common_name'].nunique()
total_world = tax_df['comName'].nunique()
plt.suptitle(f"Total species seen: {total_seen} / {total_world} ({100*total_seen/total_world:.2f}%)", fontsize=11, y=0.92)
for i, family in enumerate(top10.index):
    seen = merged[merged['familyComName'] == family]['common_name'].nunique()
    total = tax_df[tax_df['familyComName'] == family]['comName'].nunique()
    percent = round(top10.iloc[i])
    ax.text(
        i, 
        top10.iloc[i] + 1, 
        f"{seen}/{total}\n({percent}%)", 
        ha='center', 
        va='bottom', 
        fontweight='bold', 
        fontsize=12
    )
plt.xticks(rotation=30, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("life-list/visualizations/ll_top_families_percent_seen.png")
plt.show()