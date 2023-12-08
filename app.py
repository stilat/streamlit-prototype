import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Function to generate polynomial data
def generate_polynomial_data(start_date, end_date, coeffs):
    dates = pd.date_range(start_date, end_date)
    x = np.arange(len(dates))
    y = np.polyval(coeffs, x)
    return pd.Series(y, index=dates)

# Function to convert data to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=True).encode('utf-8')

# Streamlit app layout
st.title("Visualization of Polynomial Time Series")
num_cases = st.sidebar.number_input("Number of Cases", min_value=1, value=3, step=1)

# Collecting data for each case
data_series = []
for i in range(num_cases):
    with st.sidebar.expander(f"Case {i+1}", expanded=True):
        # Date inputs for each case
        start_date = st.date_input(f"Start Date for Case {i+1}", pd.to_datetime("2023-01-01"), key=f'start_date_{i}')
        end_date = st.date_input(f"End Date for Case {i+1}", pd.to_datetime("2023-12-31"), key=f'end_date_{i}')
        # Coefficients input for each case using sliders
        coeffs = [st.slider(f"Coefficient {j} for Case {i+1}", min_value=-100.0, max_value=100.0, value=0.0, step=0.1, key=f'coeff_{i}_{j}') for j in range(5)]
        time_series = generate_polynomial_data(start_date, end_date, coeffs)
        data_series.append(time_series)

# Plotting and metrics calculation
fig = go.Figure()
metrics = {"Sum": [], "Euclidean Norm": [], "Mean": [], "Median": []}
for i, time_series in enumerate(data_series):
    fig.add_trace(go.Scatter(x=time_series.index, y=time_series, mode='lines', name=f"Case {i+1}"))
    
    metrics["Sum"].append(time_series.sum())
    metrics["Euclidean Norm"].append(np.linalg.norm(time_series))
    metrics["Mean"].append(time_series.mean())
    metrics["Median"].append(time_series.median())

fig.update_layout(title="Time Series Plot", xaxis_title='Date', yaxis_title='Value')
st.plotly_chart(fig)

# Displaying the metrics table
st.table(pd.DataFrame(metrics, index=[f"Case {i+1}" for i in range(num_cases)]))

# Add download buttons in the bottom horizontally
cols = st.columns(num_cases)
for i, col in enumerate(cols):
    time_series = data_series[i]
    csv = convert_df_to_csv(time_series)
    with col:
        st.download_button(
            label=f"Download data for Case {i+1} as CSV",
            data=csv,
            file_name=f'time_series_case_{i+1}.csv',
            mime='text/csv',
        )
