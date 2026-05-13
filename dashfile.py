import streamlit as st
import pandas as pd
import plotly.express as px

st.sidebar.title("About This Project")
st.sidebar.write("Data Source: NPCI Official UPI Statistics")
st.sidebar.write("Period: June 2021 - March 2026")
st.sidebar.write("Built with: Python, Pandas, Plotly, Streamlit")
st.sidebar.write("By: Harsha Diwan")
st.title("India UPI Payments Analytics (2021-2026)")

col1, col2, col3 = st.columns(3)

col1.metric("Volume Growth", "5x", "2021 to 2026")
col2.metric("Peak Growth Rate", "77%", "2022-23")
col3.metric("Highest Month", "March", "FY End Effect")

#loding files from2021-2026 (combining)
files = {
    '2021-22': 'upi_2021_22.xlsx',
    '2022-23': 'upi_2022_23.xlsx',
    '2023-24': 'upi_2023_24.xlsx',
    '2024-25': 'upi_2024_25.xlsx',
    '2025-26': 'upi_2025_26.xlsx',
}

df = []
for key,value in files.items():
    temp = pd.read_excel(value)
    temp ['FY'] = key
    df = df + [temp]

master_df = pd.concat(df , ignore_index=True)
master_df.columns = ['month', 'vol', 'volavg', 'val', 'valavg', 'FY']

# cleaning and sorting
master_df['date'] = pd.to_datetime(master_df['month'], format='%B-%Y')
master_df = master_df.sort_values('date', ignore_index=True)
master_df['month_name'] = master_df['date'].dt.month_name()

#total value divided by total volume = average amount per transaction
master_df['avg_txn_value'] = master_df['val'] / master_df['vol']


# Chart 1 - Volume Growth
fig = px.line(master_df, x='date', y='vol',
              title='UPI Transaction Volume Growth (2021-2026)',
              labels={'date': 'Month', 'vol': 'Volume (in Millions)'})
st.plotly_chart(fig)

# Insight 1
st.write("Insight 1: UPI transaction volume grew 5x in 4 years - from 40,786 Mn in 2021-22 to 205,046 Mn in 2025-26.")

# Chart 2 - YoY Growth Rate
fy_vol = master_df.groupby('FY')['vol'].sum()
growth = fy_vol.pct_change() * 100
growth_df = growth.reset_index()
growth_df.columns = ['FY', 'growth_pct']

fig2 = px.bar(growth_df, x='FY', y='growth_pct',
              title='UPI YoY Growth Rate (%) by Financial Year',
              labels={'FY': 'Financial Year', 'growth_pct': 'Growth %'})
st.plotly_chart(fig2)
st.write("Insight 2: Growth rate slowing from 77% in 2022-23 to 29% in 2025-26. Normal for maturing platforms.")

# Chart 3 - Monthly Seasonality
monthly_avg = master_df.groupby('month_name')['vol'].mean()

fig3 = px.bar(monthly_avg.reset_index(), x='month_name', y='vol',
              title='UPI Average Monthly Transaction Volume (2021-2026)',
              labels={'month_name': 'Month', 'vol': 'Avg Volume (Millions)'},
              category_orders={'month_name': ['January', 'February', 'March', 'April',
                                               'May', 'June', 'July', 'August',
                                               'September', 'October', 'November', 'December']})
st.plotly_chart(fig3)
st.write("Insight 3: March is always highest due to financial year end. June is always lowest - start of new FY.")

# Chart 4 - Average Transaction Value
fig4 = px.line(master_df, x='date', y='avg_txn_value',
               title='UPI Average Transaction Value Over Time (2021-2026)',
               labels={'date': 'Month', 'avg_txn_value': 'Avg Transaction Value'})
st.plotly_chart(fig4)
st.write("Insight 4: Average transaction value falling from 190 to 130. UPI moved from urban high-value payments to everyday micro-transactions.")
