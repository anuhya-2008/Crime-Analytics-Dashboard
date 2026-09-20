
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Crime Analytics Intelligence Dashboard",
    page_icon="🚔",
    layout="wide"
)

# -------------------------------
# Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("crime_data_1000_records.csv")
    df["Victim_Age"] = pd.to_numeric(df["Victim_Age"], errors="coerce")
    return df

df = load_data()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🚔 Police Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Crime Analysis",
        "FIR Search",
        "Add Crime",
        "Records"
    ]
)

# -------------------------------
# DASHBOARD
# -------------------------------
if page == "Dashboard":

    st.title("🚔 Crime Analytics Intelligence Dashboard")
    st.caption("Powered by Pandas • NumPy • Matplotlib")

    age = df["Victim_Age"].dropna()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Crimes", len(df))
    c2.metric("Solved", len(df[df["Status"]=="Solved"]))
    c3.metric("Pending", len(df[df["Status"]=="Pending"]))
    c4.metric("Cities", df["City"].nunique())
    c5.metric("Average Age", round(np.mean(age),1) if len(age)>0 else 0)

    st.divider()

    a, b, c = st.columns(3)

    a.metric("Maximum Age", int(np.max(age)) if len(age)>0 else 0)
    b.metric("Minimum Age", int(np.min(age)) if len(age)>0 else 0)
    c.metric("Median Age", int(np.median(age)) if len(age)>0 else 0)

# -------------------------------
# CRIME ANALYSIS
# -------------------------------
elif page == "Crime Analysis":

    st.title("📊 Crime Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5,4))
        df["Crime_Type"].value_counts().plot(
            kind="bar",
            ax=ax,
            color="steelblue"
        )
        ax.set_title("Crime Type Analysis")
        ax.set_xlabel("Crime Type")
        ax.set_ylabel("Cases")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(5,4))
        df["Status"].value_counts().plot(
            kind="pie",
            ax=ax,
            autopct="%1.1f%%",
            colors=["green","red"]
        )
        ax.set_ylabel("")
        ax.set_title("Solved vs Pending")
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(5,4))
        df["City"].value_counts().head(5).plot(
            kind="bar",
            ax=ax,
            color="orange"
        )
        ax.set_title("Top Crime Cities")
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(5,4))
        ax.hist(
            df["Victim_Age"].dropna(),
            bins=10,
            color="purple",
            edgecolor="black"
        )
        ax.set_title("Victim Age Distribution")
        ax.set_xlabel("Age")
        ax.set_ylabel("Victims")
        st.pyplot(fig)

# -------------------------------
# FIR SEARCH
# -------------------------------
elif page == "FIR Search":

    st.title("🔍 FIR Search")

    query = st.text_input("Enter FIR Number or Crime ID")

    if st.button("Search"):

        result = df[
            (df["FIR_No"].astype(str)==query) |
            (df["Crime_ID"].astype(str)==query)
        ]

        if result.empty:
            st.error("Record Not Found")
        else:
            st.success("Record Found")
            st.dataframe(result, use_container_width=True)

# -------------------------------
# ADD CRIME
# -------------------------------
elif page == "Add Crime":

    st.title("➕ Add New Crime")

    with st.form("crime_form"):

        data = {}

        for column in df.columns:
            data[column] = st.text_input(column)

        submit = st.form_submit_button("Save Record")

        if submit:

            df.loc[len(df)] = data
            df.to_csv("crime_data_1000_records.csv", index=False)

            st.success("Crime Record Saved Successfully!")

# -------------------------------
# RECORDS
# -------------------------------
elif page == "Records":

    st.title("📋 Crime Records")

    city = st.selectbox(
        "Filter by City",
        ["All"] + sorted(df["City"].dropna().unique().tolist())
    )

    status = st.selectbox(
        "Filter by Status",
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )

    filtered = df.copy()

    if city != "All":
        filtered = filtered[filtered["City"] == city]

    if status != "All":
        filtered = filtered[filtered["Status"] == status]

    st.dataframe(filtered, use_container_width=True)
    st.write(f"Showing **{len(filtered)}** records.")