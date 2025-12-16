import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NBA Player Stats Explorer")

st.markdown(
    """
This app performs simple webscraping of NBA player stats data!

- **Python libraries:** base64, pandas, streamlit
- **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
"""
)

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2021))))

@st.cache_data
def load_data(year: int) -> pd.DataFrame:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    df = pd.read_html(url, header=0)[0]

    # Flatten multi-index columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)

    # Strip whitespace in column names
    df.columns = df.columns.astype(str).str.strip()

    # Remove repeated header rows
    if "Rk" in df.columns:
        df = df[df["Rk"] != "Rk"]

    df = df.fillna(0)

    # Drop rank column
    if "Rk" in df.columns:
        df = df.drop(columns=["Rk"])

    return df

playerstats = load_data(selected_year)

# Debug: show columns so you can confirm Team column name
st.write("Columns:", list(playerstats.columns))

# ---- Team column detection (robust) ----
if "Tm" in playerstats.columns:
    team_col = "Tm"
elif "Team" in playerstats.columns:
    team_col = "Team"
else:
    st.error("Could not find team column. Check the printed Columns list above.")
    st.stop()

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats[team_col].astype(str).unique())
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ["C", "PF", "SF", "PG", "SG"]
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# Filtering data
df_selected = playerstats[
    (playerstats[team_col].isin(selected_team)) & (playerstats["Pos"].isin(selected_pos))
]

st.header("Display Player Stats of Selected Team(s)")
st.write(
    f"Data Dimension: {df_selected.shape[0]} rows and {df_selected.shape[1]} columns."
)
st.dataframe(df_selected)

def filedownload(df: pd.DataFrame) -> str:
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'

st.markdown(filedownload(df_selected), unsafe_allow_html=True)

# Heatmap
if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")

    # Correlation on numeric columns only
    corr = df_selected.select_dtypes(include=[np.number]).corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(corr, mask=mask, vmax=1, square=True, ax=ax)

    st.pyplot(fig)
