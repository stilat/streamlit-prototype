
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go


def generate_polynomial_data(start_date, end_date, coeffs):
    dates = pd.date_range(start_date, end_date)
    x = np.arange(len(dates))
    y = np.polyval(coeffs, x)
    return pd.Series(y, index=dates)

st.title("Multi-Case Visualization")
num_cases = st.sidebar.number_input("Number of Cases", min_value=1, value=3, step=1)

# Collecting data for each case
for i in range(num_cases):
    with st.sidebar.expander(f"Case {i+1} ", expanded=True):
        # Date inputs for each case
        start_date = st.date_input(f"Start Date for Case {i+1}", pd.to_datetime("2023-01-01"), key=f'start_date_{i}')
        end_date = st.date_input(f"End Date for Case {i+1}", pd.to_datetime("2023-12-31"), key=f'end_date_{i}')
        # Coefficients input for each case using sliders
        coeffs = [st.slider(f"Coefficient {j} for Case {i+1}", min_value=-100.0, max_value=100.0, value=0.0, step=0.1, key=f'coeff_{i}_{j}') for j in range(5)]


# Plotting and metrics calculation
fig = go.Figure()
metrics = {"Sum": [], "Euclidean Norm": [], "Mean": [], "Median": []}
for i in range(num_cases):
    coeffs_key = f'coeffs_{i}'
    coeffs = [st.session_state.get(f'coeff_{i}_{j}', 0) for j in range(5)]
    time_series = generate_polynomial_data(start_date, end_date, coeffs)
    fig.add_trace(go.Scatter(x=time_series.index, y=time_series, mode='lines', name=f"Case {i+1}"))
    
    metrics["Sum"].append(time_series.sum())
    metrics["Euclidean Norm"].append(np.linalg.norm(time_series))
    metrics["Mean"].append(time_series.mean())
    metrics["Median"].append(time_series.median())

fig.update_layout(title="Time Series Plot", xaxis_title='Date', yaxis_title='Value')
st.plotly_chart(fig)

# Displaying the metrics table
st.table(pd.DataFrame(metrics, index=[f"Case {i+1}" for i in range(num_cases)]))
