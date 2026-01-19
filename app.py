import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial
st.set_page_config(page_title="US Vehicles Analysis", layout="wide")

st.header('Exploratory Data Analysis (EDA) with US vehicles')

st.markdown('''
##### The goal of this project is to show how to combine different skills and apply the learning concepts building an EDA web project deploy.
''')

# Función para cargar y limpiar datos (con cache para velocidad)
@st.cache_data
def load_data():
    data = pd.read_csv('vehicles_us.csv')
    # Limpieza básica
    data['model_year'] = data['model_year'].fillna(data['model_year'].median())
    data['odometer'] = data['odometer'].fillna(data['odometer'].median())
    data['is_4wd'] = data['is_4wd'].fillna(0).astype(bool)
    data['date_posted'] = pd.to_datetime(data['date_posted'])
    return data

data = load_data()

# Mostrar datos crudos con un checkbox
if st.checkbox('Show raw data'):
    st.write(data.head(20))

st.divider()

# Sección de botones originales
st.subheader('Interactive Plots')
col1, col2 = st.columns(2)

with col1:
    if st.button('Construir histograma'):
        st.write('Creating an histogram of the odometer data')
        fig = go.Figure(data=[go.Histogram(x=data['odometer'])])
        fig.update_layout(title_text='Odometer distribution', xaxis_title='Odometer', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if st.button('Construir gráfico de dispersión'):
        st.write('Creating an odometer vs. price scatter plot')
        fig = go.Figure(data=go.Scatter(x=data['odometer'], y=data['price'], mode='markers'))
        fig.update_layout(title='Price vs. Odometer', xaxis_title='Odometer', yaxis_title='Price ($)')
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- NUEVA SECCIÓN: ANÁLISIS ELABORADO ---
st.subheader('Advanced Market Analysis')

# Usamos pestañas para organizar los nuevos requerimientos
tab1, tab2, tab3 = st.tabs(["Vehicle Specs", "Fuel & Transmission", "Market Speed"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.write("#### Model Year Distribution")
        fig_year = px.histogram(data, x='model_year', color_discrete_sequence=['indianred'])
        st.plotly_chart(fig_year, use_container_width=True)
    
    with c2:
        st.write("#### Condition Percentage")
        cond_counts = data['condition'].value_counts(normalize=True).reset_index()
        fig_cond = px.pie(cond_counts, values='proportion', names='condition', hole=0.3)
        st.plotly_chart(fig_cond, use_container_width=True)

with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.write("#### Fuel Type Usage")
        fuel_counts = data['fuel'].value_counts(normalize=True).reset_index()
        fig_fuel = px.bar(fuel_counts, x='fuel', y='proportion', color='fuel')
        st.plotly_chart(fig_fuel, use_container_width=True)
    
    with c4:
        st.write("#### Transmission by Vehicle Type")
        # Gráfico agrupado para ver transmisión y tipo simultáneamente
        fig_type = px.histogram(data, x="type", color="transmission", barmode='group')
        st.plotly_chart(fig_type, use_container_width=True)

with tab3:
    st.write("#### Fastest Sold Vehicles (Shortest time listed)")
    # Obtenemos los 10 con menor tiempo
    fast_sales = data.sort_values(by='days_listed').head(10)
    # Mostramos una tabla estilizada
    st.table(fast_sales[['model', 'model_year', 'price', 'days_listed', 'condition']])