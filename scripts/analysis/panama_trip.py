import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", font_scale=1.2)
import json
import os

# Directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
input_life_list = os.path.join(base_dir, "data/life_list_cleaned.csv")
input_taxonomy = os.path.join(base_dir, "data/taxonomy.json")

# Load Data
df = pd.read_csv(input_life_list)
with open(input_taxonomy) as f:
    taxonomy = json.load(f)
tax_df = pd.DataFrame(taxonomy)

# Filters
panama_df = df[df['region'].str.startswith('PA-')]
all_before = df[~df['region'].str.startswith('PA-')]['common_name'].unique()
panama_new = panama_df[~panama_df['common_name'].isin(all_before)]
merged = pd.merge(panama_new, tax_df[['comName', 'familyComName']], left_on='common_name', right_on='comName', how='left')
merged_all = pd.merge(panama_df, tax_df[['comName', 'familyComName']], left_on='common_name', right_on='comName', how='left')


# --- 1. Bird families with the biggest increase (new families added) ---
# Find families in Panama not seen before the trip
family_counts = merged['familyComName'].value_counts().head(10)

plt.figure(figsize=(10, 6))
colors = sns.color_palette("viridis", len(family_counts))
ax = family_counts.plot(kind='bar', color=colors, edgecolor='black')
plt.title("Top 10 New Bird Families Added in Panama", fontsize=18, weight='bold')
plt.xlabel("Family", fontsize=14)
plt.ylabel("Number of New Species", fontsize=14)
ax.set_ylim(0, family_counts.max() * 1.18)
sns.despine()
ax.grid(False)

# Add numbers above bars
for i, v in enumerate(family_counts):
    ax.text(i, v + 0.3, str(v), ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.xticks(rotation=30, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig("life-list/visualizations/panama_new_families.png")
plt.show()

# --- 2. Pie Chart: Top 10 Panama Bird Families ---
family_pie = merged_all['familyComName'].value_counts().head(10)

plt.figure(figsize=(9, 9))
colors = sns.color_palette("pastel", len(family_pie))
wedges, texts, autotexts = plt.pie(
    family_pie,
    labels=family_pie.index,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(edgecolor='w', linewidth=1.5),
    colors=colors,
    textprops={'fontsize': 12}
)
plt.setp(autotexts, size=13, weight="bold", color="black")
plt.title("Top 10 Panama Bird Families", fontsize=18, weight='bold')
plt.tight_layout()
plt.savefig("life-list/visualizations/panama_family_pie.png")
plt.show()

# --- 3. Bar Chart: New Life Birds by Day in Panama ---
if 'first_observation' in panama_df.columns:
    panama_df['first_observation'] = pd.to_datetime(panama_df['first_observation'])
    panama_df['date_only'] = panama_df['first_observation'].dt.date
    daily_counts = panama_df.groupby('date_only').size()
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("crest", len(daily_counts))
    ax = daily_counts.plot(kind='bar', color=colors, edgecolor='black')
    plt.title("New Life Birds by Day in Panama", fontsize=18, weight='bold')
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Number of New Life Birds", fontsize=14)
    ax.set_ylim(0, daily_counts.max() * 1.18)
    sns.despine()
    ax.grid(False)

    # Add numbers above bars
    for i, v in enumerate(daily_counts):
        ax.text(i, v + 0.2, str(v), ha='center', va='bottom', fontweight='bold', fontsize=12)

    plt.xticks(rotation=30, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig("life-list/visualizations/panama_life_birds_by_day.png")
    plt.show()

# --- 4. Cumulative Unique Species Seen in Panama ---
# Cumulative unique species by day in Panama
panama_df['first_observation'] = pd.to_datetime(panama_df['first_observation'])
panama_df = panama_df.sort_values('first_observation')
panama_df['date_only'] = panama_df['first_observation'].dt.date
cum_species = panama_df.groupby('date_only')['common_name'].nunique().cumsum()

plt.figure(figsize=(12,6))
cum_species.plot(marker='o', color='teal')
plt.title("Cumulative Unique Species Seen in Panama", fontsize=18, weight='bold')
plt.xlabel("Date", fontsize=14)
plt.ylabel("Cumulative Unique Species", fontsize=14)
plt.tight_layout()
plt.savefig("life-list/visualizations/panama_species_accumulation.png")
plt.show()

