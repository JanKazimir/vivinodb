"""
Vivino Wine Analysis — Streamlit Dashboard

Showcases insights from a partial Vivino dataset (high-end wines only).
Run with: streamlit run app.py
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ── Paths ──────────────────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent / "data" / "vivino.db"
QUERIES_DIR = Path(__file__).parent / "queries"


# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    """
    Return a shared, cached sqlite3 connection.

    Streamlit re-runs the script on every interaction, so we cache the
    connection to avoid opening a new one each time.  The connection is
    read-only (we never write), so sharing it is safe.

    Note: we do NOT close this connection manually. SQLite cleans up when
    the process exits, and Streamlit manages the lifecycle of cached
    resources.  Closing it ourselves would break subsequent reruns.
    """
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)


def load_query(name: str) -> str:
    """Read a .sql file from the queries/ directory."""
    return (QUERIES_DIR / name).read_text(encoding="utf-8")


def run_query(name: str) -> pd.DataFrame:
    """Execute a named .sql file and return a DataFrame."""
    return pd.read_sql_query(load_query(name), get_connection())


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Vivino Analysis", page_icon="🍷", layout="wide")

# ── Sidebar — Table of Contents ───────────────────────────────────────────────
st.sidebar.title("🍷 Vivino Analysis")
st.sidebar.markdown("---")
st.sidebar.markdown("""
- [Overview](#vivino-wine-analysis)
- [Discovery](#discovery)
- [Highlighted Best Wines](#highlighted-best-wines)
- [Marketing Budget](#marketing-budget)
- [Winery Awards](#winery-awards)
- [Most Common Grapes](#most-common-grapes)
- [Flavour Profile](#flavour-profile-analysis)
- [Country Leaderboard](#country-leaderboard)
- [VIP Recommendation](#vip-recommendation)
""")

# ══════════════════════════════════════════════════════════════════════════════
# SECTIONS
# ══════════════════════════════════════════════════════════════════════════════


# ── Overview ──────────────────────────────────────────────────────────────────
st.title("🍷 Vivino Wine Analysis")
st.markdown(
    """
    This is a brief analysis of a **partial** wine dataset from Vivino.
    *Partial* means we only have access to high-end wines at the top of the
    price distribution, which also means we're talking about largely
    **delicious** wines.

    > **Note:** The main limitation of this dataset is that winery names are
    > missing for most wines. Only four winery names actually match the
    > wines we have.  Sharing the full dataset would solve this.
    """
)

# ── Discovery ─────────────────────────────────────────────────────────────────
st.header("📊 Discovery")
st.markdown(
    """
    47 wines and 246 vintages have a rating of **4.7 and above** — a small set.

    💡 *Wines can have several vintages. A vintage belongs to a single wine.
    Think of a vintage as the "Year YYYY edition" of a given wine.*
    """
)

# -- Price distribution ------------------------------------------------
st.subheader("Price Distribution of All Wines")
st.caption(
    "Huge spread, starting around 20 € per bottle, going as high as 10 k€. "
    "(Nothing under 20 € except for small 375 ml bottles.)"
)
df_prices = run_query("cheapest_wines.sql")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].boxplot(df_prices["price_euros"], vert=True)
axes[0].set_title("All wine prices", fontsize=14, fontweight="bold")
axes[0].set_ylabel("Price (€)")

axes[1].boxplot(df_prices["price_euros"], vert=True)
axes[1].set_ylim(0, 1000)
axes[1].set_title("Prices < 1 000 €", fontsize=14, fontweight="bold")
axes[1].set_ylabel("Price (€)")
fig.tight_layout()
st.pyplot(fig)

# -- Wine ratings distribution -----------------------------------------
st.subheader("Wine Ratings Distribution")
st.caption(
    "Largely normal, but the dataset starts at 4.1 and goes up to 4.9 — "
    "an artifact of only having high-end wines."
)
df_ratings = pd.read_sql_query(
    "SELECT ratings_average FROM wines", get_connection()
)
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.hist(df_ratings["ratings_average"], bins=8, edgecolor="white", alpha=0.8)
ax2.set_title("Wine ratings_average distribution", fontsize=14, fontweight="bold")
ax2.set_xlabel("ratings_average")
ax2.set_ylabel("Count")
fig2.tight_layout()
st.pyplot(fig2)

# -- Rating counts by rating -------------------------------------------
st.subheader("Average Rating Counts by Rating (wines)")
st.caption("The dip at 4.4–4.5 is odd: those wines are cheaper but less rated.")
df_rc = run_query("distrib_rating_count.sql")
fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.bar(
    df_rc["ratings_average"].astype(str),
    df_rc["AVG(ratings_count)"],
    edgecolor="white",
    alpha=0.8,
)
ax3.set_title("Avg ratings count per rating (wines)", fontsize=14, fontweight="bold")
ax3.set_xlabel("ratings_average")
ax3.set_ylabel("Average count of user ratings")
fig3.tight_layout()
st.pyplot(fig3)

# -- Average price per rating ------------------------------------------
st.subheader("Average Price per Rating (vintages)")
st.caption(
    "Higher rating → higher price, as expected. "
    "The 4.9 dip is a small-sample artifact."
)
df_apr = run_query("avg_price_by_rating.sql")
fig4, ax4 = plt.subplots(figsize=(8, 4))
ax4.bar(
    df_apr["ratings_average"].astype(str),
    df_apr["AVG(price_euros)"],
    edgecolor="white",
    alpha=0.8,
    color="#E07B39",
)
ax4.set_title("Avg price per rating (vintages)", fontsize=14, fontweight="bold")
ax4.set_xlabel("ratings_average")
ax4.set_ylabel("Average price (€)")
fig4.tight_layout()
st.pyplot(fig4)

# -- Vintages per wine -------------------------------------------------
st.subheader("Distribution of Vintages per Wine")
st.caption("Heavily left-skewed: most wines have only a few vintages.")
df_vpw = run_query("wine_appeance_count.sql")
fig5, ax5 = plt.subplots(figsize=(8, 4))
ax5.plot(df_vpw["number_of_wines"], df_vpw["vintages_per_wine"], marker="o")
ax5.set_title("Vintages per wine", fontsize=14, fontweight="bold")
ax5.set_xlabel("Number of wines")
ax5.set_ylabel("Vintages per wine")
fig5.tight_layout()
st.pyplot(fig5)

# -- Rating count by rating for vintages (dual axis) -------------------
st.subheader("Rating Count by Rating (vintages, with avg price)")
st.caption("The 4.5 rating is the 'forgotten group'.")
df_rr = run_query("average_rating_count_by_rating.sql")
plot_df = df_rr.set_index("ratings_average")

fig6, ax6 = plt.subplots(figsize=(10, 5))
ax6.bar(
    range(len(plot_df)),
    plot_df["average_ratings_count"],
    label="Average ratings count",
    alpha=0.8,
)
ax6b = ax6.twinx()
ax6b.plot(
    range(len(plot_df)),
    plot_df["average_price"],
    color="orange",
    marker="o",
    label="Average price (€)",
)
ax6.set_ylabel("Average number of user ratings")
ax6b.set_ylabel("Average price (€)")
ax6.set_xticks(range(len(plot_df)))
ax6.set_xticklabels(plot_df.index, rotation=0)
ax6.legend(loc="upper left")
ax6b.legend(loc="lower left")
ax6.set_title(
    "Avg rating count & price by vintage rating",
    fontsize=14,
    fontweight="bold",
)
fig6.tight_layout()
st.pyplot(fig6)


# ── Highlighted Best Wines ────────────────────────────────────────────────────
st.header("🏆 Highlighted Best Wines")
st.markdown(
    """
    How to select 10 wines among ~2 000? The goal is to **increase sales**,
    so price matters. We built a balanced selection across price categories,
    with variety in origin and style (reds & whites). Vintages with fewer
    than 200 ratings were excluded.

    | Category | Budget | Count |
    |---|---|---|
    | Great Deal | < 30 € | 5 (2 white, 3 red) |
    | Excellent | < 50 € | 3 (1 white, 2 red) |
    | Amazing | < 100 € | 2 |
    | Luxury | No limit | 2 |
    """
)
df_top = run_query("top_ten.sql")
display_cols = [
    "name",
    "ratings_average",
    "adjusted_price",
    "country_name",
    "region_name",
    "ratings_count",
]
st.dataframe(
    df_top[display_cols].rename(
        columns={
            "name": "Wine",
            "ratings_average": "Rating",
            "adjusted_price": "Price (€, 750 ml)",
            "country_name": "Country",
            "region_name": "Region",
            "ratings_count": "# Ratings",
        }
    ),
    use_container_width=True,
    hide_index=True,
)


# ── Marketing Budget ──────────────────────────────────────────────────────────
st.header("💰 Marketing Budget")
st.markdown(
    """
    **Best countries for Vivino** (attract users → low user-to-wine ratio):
    Moldova, Hungary, Chile.

    **Best countries for producers** (attract customers → high user-to-wine
    ratio): US, Switzerland, Portugal — lots of potential users per winery.
    """
)
df_mkt = run_query("user_count_by_country.sql")
st.dataframe(
    df_mkt.rename(
        columns={
            "name": "Country",
            "users_count": "Users",
            "wines_count": "Wines",
            "user_to_wine_ratio": "Users / Wine",
            "wineries_count": "Wineries",
            "user_to_wineries_ratio": "Users / Winery",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(df_mkt["name"], df_mkt["user_to_wine_ratio"], edgecolor="white", alpha=0.8)
ax.set_xlabel("Users per Wine")
ax.set_title("User-to-Wine Ratio by Country", fontsize=14, fontweight="bold")
fig.tight_layout()
st.pyplot(fig)


# ── Winery Awards ─────────────────────────────────────────────────────────────
st.header("🏅 Winery Awards")
st.markdown(
    """
    Only wineries with **more than 5 vintages** are considered.

    - **Quality award**: France & Italy dominate.
    - **Bang-for-buck award**: US, France and Italy at the top too. Their reputation is deserved.

    *(Winery names are unfortunately missing from the dataset.)*
    """
)

tab1, tab2 = st.tabs(["Best Quality", "Best Bang for Buck"])

with tab1:
    df_bw = run_query("best_wineries.sql")
    st.dataframe(
        df_bw.rename(
            columns={
                "wine_id": "Wine ID",
                "vintage_id": "Vintage ID",
                "count": "# Vintages",
                "wine_average": "Wine Avg",
                "winery_id": "Winery ID",
                "vintage_average": "Vintage Avg",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

with tab2:
    df_bfb = run_query("best_wineries_bang_for_buck.sql")
    st.dataframe(
        df_bfb.round(3).rename(
            columns={
                "winery_id": "Winery ID",
                "bang_for_buck": "Bang for Buck",
                "avg_rating": "Avg Rating",
                "avg_price": "Avg Price (€)",
                "norm_rating": "Norm. Rating",
                "norm_price": "Norm. Price",
                
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# ── Most Common Grapes ───────────────────────────────────────────────────────
st.header("🍇 Most Common Grapes")
st.markdown("**Top 3:** Cabernet Sauvignon, Chardonnay, Pinot Noir.")

df_grapes = run_query("most_common_grapes.sql")

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df_grapes["name"], df_grapes["wines_count"], edgecolor="white", alpha=0.8)
ax.set_title("Most Common Grapes", fontsize=14, fontweight="bold")
ax.set_ylabel("Grape")
ax.set_xlabel("Wines Count")
fig.tight_layout()
st.pyplot(fig)

st.dataframe(
    df_grapes.rename(
        columns={
            "grape_id": "Grape ID",
            "name": "Grape",
            "wines_count": "Wines Count",
        }
    ),
    use_container_width=True,
    hide_index=True,
)


# ── Flavour Profile ──────────────────────────────────────────────────────────
st.header("👅 Flavour Profile Analysis")
st.markdown(
    """
    A customer cluster likes wines with these **primary** keywords
    (each confirmed by > 10 users):

    | Keyword | Group |
    |---|---|
    | coffee | oak |
    | toast | non_oak |
    | green apple | tree_fruit |
    | cream | microbio |
    | citrus | citrus_fruit |

    **Result:** almost all matches are **Champagnes**.
    """
)
df_fp = run_query("wine_flavour_profile.sql")
st.dataframe(
    df_fp[["wine_id", "wine_name", "keyword_name", "group_name", "Keyword_count", "fizziness"]].rename(
        columns={
            "wine_id": "Wine ID",
            "wine_name": "Wine",
            "keyword_name": "Keyword",
            "group_name": "Group",
            "Keyword_count": "Keyword Count",
            "fizziness": "Fizziness",
        }
    ),
    use_container_width=True,
    hide_index=True,
)


# ── Country Leaderboard ──────────────────────────────────────────────────────
st.header("🌍 Country Leaderboard")
st.markdown(
    """
    Average wine rating is much more stable across countries than the
    vintage average — because **510 vintages have a rating of 0** (data
    artifact). The chart below excludes those zeros for a fairer comparison.
    """
)

df_wine = run_query("wine_average_by_country.sql").rename(
    columns={"AVG(ratings_average)": "wine_avg"}
)
df_vint = run_query("vintage_avg_no_zeroes.sql").rename(
    columns={"AVG(vintages.ratings_average)": "vintage_avg"}
)
df = pd.merge(df_wine, df_vint, on="country_name", how="outer").fillna(0)
df = df.sort_values("country_name")

x = np.arange(len(df))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - width / 2, df["wine_avg"], width, color="#0D33F4", edgecolor="white", alpha=0.8, label="Wine Avg")
ax.bar(x + width / 2, df["vintage_avg"], width, color="#059951", edgecolor="white", alpha=0.8, label="Vintage Avg")
ax.set_title(
    "Average Ratings by Country (5+ wines/vintages)",
    fontsize=14,
    fontweight="bold",
)
ax.set_xlabel("Country")
ax.set_ylabel("Rating Average")
ax.set_xticks(x)
ax.set_xticklabels(df["country_name"], rotation=45, ha="right")
ax.set_ylim(4.41, 4.56)
ax.grid(True, axis="y", linestyle="--", alpha=0.5)
ax.legend(loc="upper left")
fig.tight_layout()
st.pyplot(fig)


# ── VIP Recommendation ───────────────────────────────────────────────────────
st.header("🥂 VIP Recommendation")
st.markdown(
    """
    A VIP client loves **Cabernet Sauvignon**. Money is no object.

    **Top pick:** Scarecrow Cabernet Sauvignon 2015.
    """
)
df_vip = run_query("vip_recommendation.sql")
display_cols = [
    "vintage_name",
    "ratings_average",
    "price_euros",
    "region_name",
    "country_code",
    "ratings_count",
]
st.dataframe(
    df_vip[display_cols]
    .head(5)
    .rename(
        columns={
            "vintage_name": "Wine",
            "ratings_average": "Rating",
            "price_euros": "Price (€)",
            "region_name": "Region",
            "country_code": "Country",
            "ratings_count": "# Ratings",
        }
    ),
    use_container_width=True,
    hide_index=True,
)
