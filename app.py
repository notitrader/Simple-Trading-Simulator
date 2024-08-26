import streamlit as st
import numpy as np
import pandas as pd
import io

# Page configuration
st.title("Simple Trading Simulator")

# User input
contracts = st.sidebar.number_input("Number of Contracts", min_value=1, max_value=100, value=1)
ticks_loss = st.sidebar.number_input("Loss Ticks", min_value=1, max_value=10, value=5)
ticks_profit = st.sidebar.number_input("Profit Ticks", min_value=1, max_value=10, value=7)
win_rate = st.sidebar.slider("Win Percentage (%)", min_value=0, max_value=100, value=60) / 100
tick_value = st.sidebar.number_input("Tick Value ($)", min_value=0.01, value=12.5, step=0.01)
fee_per_contract = st.sidebar.number_input("Fee per Contract ($)", min_value=0.01, value=2.5, step=0.01)
num_trades = st.sidebar.number_input("Number of Trades", min_value=1, max_value=1000, value=200)

# Simulation
profits = []
for _ in range(num_trades):
    if np.random.rand() <= win_rate:
        profit = (ticks_profit * tick_value * contracts) - (fee_per_contract * contracts * 2)  # Winning trade minus fees
    else:
        profit = -(ticks_loss * tick_value * contracts) - (fee_per_contract * contracts * 2)  # Losing trade plus fees
    profits.append(profit)
    
cumulative_profit = np.cumsum(profits)

# Creating DataFrame to display results
df_simulation = pd.DataFrame({"Cumulative Profit": cumulative_profit})

# Displaying results
st.subheader("Simulation Results")
st.line_chart(df_simulation, use_container_width=True)

# Calculating the average cumulative profit
average_cumulative_profit = df_simulation.iloc[-1].mean()

# Calculating the maximum drawdown
drawdown = df_simulation.cummax() - df_simulation
max_drawdown = drawdown.max().max()

# Calculating the Sharpe ratio (approximate)
sharpe_ratio = (df_simulation.mean().mean() / df_simulation.std().mean()) * np.sqrt(252)

# Displaying the average cumulative profit
st.subheader(f"Average Cumulative Profits: ${average_cumulative_profit:.2f}")

# Displaying the maximum drawdown
st.subheader(f"Maximum Drawdown: ${max_drawdown:.2f}")

# Displaying the Sharpe Ratio
st.subheader(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Download results as CSV
st.subheader("Download Results")
csv = df_simulation.to_csv(index=False)
b = io.BytesIO()
b.write(csv.encode())
b.seek(0)
st.download_button(label="Download as CSV", data=b, file_name="simulation_results.csv", mime="text/csv")
