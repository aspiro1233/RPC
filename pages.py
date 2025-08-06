import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq
import os
from datetime import datetime
import time
import json
from typing import List, Dict, Any
import altair as alt
import numpy as np

# Additional Streamlit pages
def create_data_explorer_page():
    """Create a dedicated data exploration page"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">📊 Data Explorer</h1>
        <p class="hero-subtitle">Interactive exploration of all datasets</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load datasets
    datasets = load_datasets()
    
    if not datasets:
        st.error("No datasets loaded. Please check your data folder.")
        return
    
    # Dataset selection
    dataset_options = [key for key in datasets.keys() if isinstance(datasets[key], pd.DataFrame)]
    selected_dataset = st.selectbox("Choose a dataset to explore:", dataset_options)
    
    if selected_dataset and selected_dataset in datasets:
        df = datasets[selected_dataset]
        
        # Dataset overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Columns", f"{df.shape[1]}")
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        with col4:
            missing_data = df.isnull().sum().sum()
            st.metric("Missing Values", f"{missing_data}")
        
        # Data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(20), use_container_width=True)
        
        # Column analysis
        st.subheader("🔍 Column Analysis")
        col_tabs = st.tabs(["Numeric Columns", "Categorical Columns", "Missing Data"])
        
        with col_tabs[0]:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                selected_numeric = st.multiselect("Select numeric columns to analyze:", numeric_cols, default=list(numeric_cols)[:3])
                if selected_numeric:
                    st.write("Statistical Summary:")
                    st.dataframe(df[selected_numeric].describe(), use_container_width=True)
                    
                    # Distribution plots
                    for col in selected_numeric[:2]:  # Limit to first 2 columns
                        fig = px.histogram(df, x=col, title=f"Distribution of {col}", nbins=30)
                        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                        st.plotly_chart(fig, use_container_width=True)
        
        with col_tabs[1]:
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                for col in categorical_cols[:3]:  # Limit to first 3 columns
                    st.write(f"**{col}** - Unique values: {df[col].nunique()}")
                    value_counts = df[col].value_counts().head(10)
                    if len(value_counts) > 1:
                        fig = px.pie(values=value_counts.values, names=value_counts.index, title=f"{col} Distribution")
                        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                        st.plotly_chart(fig, use_container_width=True)
        
        with col_tabs[2]:
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0]
            if len(missing_data) > 0:
                fig = px.bar(x=missing_data.index, y=missing_data.values, title="Missing Data by Column")
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No missing data found!")

def create_analytics_dashboard():
    """Create an analytics dashboard page"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">📈 Analytics Dashboard</h1>
        <p class="hero-subtitle">Comprehensive insights across all datasets</p>
    </div>
    """, unsafe_allow_html=True)
    
    datasets = load_datasets()
    
    if not datasets:
        st.error("No datasets loaded.")
        return
    
    # Key metrics overview
    st.subheader("🎯 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Air Quality Metrics
    if 'aqi' in datasets:
        aqi_df = datasets['aqi']
        avg_aqi = aqi_df['AQI'].mean() if 'AQI' in aqi_df.columns else 0
        with col1:
            st.metric(
                "Average AQI", 
                f"{avg_aqi:.0f}",
                delta=f"{'🔴' if avg_aqi > 100 else '🟢'} {'Poor' if avg_aqi > 100 else 'Good'}"
            )
    
    # Health Metrics
    if 'idsp' in datasets:
        health_df = datasets['idsp']
        total_cases = health_df['Cases'].sum() if 'Cases' in health_df.columns else 0
        with col2:
            st.metric(
                "Total Disease Cases",
                f"{total_cases:,}",
                delta="📊 Current outbreaks"
            )
    
    # Population Metrics
    if 'population' in datasets:
        pop_df = datasets['population']
        total_pop = pop_df['Total_Population'].sum() if 'Total_Population' in pop_df.columns else 0
        with col3:
            st.metric(
                "Total Population",
                f"{total_pop/1000000:.1f}M",
                delta="👥 2025 projection"
            )
    
    # Vehicle Metrics
    if 'vahan' in datasets:
        vehicle_df = datasets['vahan']
        total_vehicles = vehicle_df['Registrations'].sum() if 'Registrations' in vehicle_df.columns else 0
        with col4:
            st.metric(
                "Vehicle Registrations",
                f"{total_vehicles:,}",
                delta="🚗 Latest data"
            )
    
    # Detailed visualizations
    st.subheader("📊 Detailed Analytics")
    
    # Create tabs for different analysis
    analysis_tabs = st.tabs(["🌬️ Air Quality", "🏥 Health Trends", "👥 Demographics", "🚗 Transportation"])
    
    with analysis_tabs[0]:
        if 'aqi' in datasets:
            aqi_df = datasets['aqi']
            
            # Top 10 most polluted cities
            if 'AQI' in aqi_df.columns and 'City' in aqi_df.columns:
                top_polluted = aqi_df.nlargest(10, 'AQI')
                fig = px.bar(
                    top_polluted,
                    x='AQI',
                    y='City',
                    title='Top 10 Most Polluted Cities',
                    color='AQI',
                    color_continuous_scale='Reds',
                    orientation='h'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Pollutant correlation
            pollutant_cols = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
            available_pollutants = [col for col in pollutant_cols if col in aqi_df.columns]
            
            if len(available_pollutants) > 1:
                corr_matrix = aqi_df[available_pollutants].corr()
                fig = px.imshow(
                    corr_matrix,
                    title='Pollutant Correlation Matrix',
                    color_continuous_scale='RdBu_r'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with analysis_tabs[1]:
        if 'idsp' in datasets:
            health_df = datasets['idsp']
            
            # Disease distribution
            if 'Disease' in health_df.columns and 'Cases' in health_df.columns:
                disease_cases = health_df.groupby('Disease')['Cases'].sum().sort_values(ascending=False)
                fig = px.pie(
                    values=disease_cases.values,
                    names=disease_cases.index,
                    title='Disease Distribution by Cases'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # State-wise health impact
            if 'State' in health_df.columns and 'Cases' in health_df.columns:
                state_cases = health_df.groupby('State')['Cases'].sum().sort_values(ascending=False).head(10)
                fig = px.bar(
                    x=state_cases.index,
                    y=state_cases.values,
                    title='Top 10 States by Disease Cases'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with analysis_tabs[2]:
        if 'population' in datasets:
            pop_df = datasets['population']
            
            # Population distribution
            if 'State' in pop_df.columns and 'Total_Population' in pop_df.columns:
                top_states = pop_df.nlargest(10, 'Total_Population')
                fig = px.treemap(
                    top_states,
                    path=['State'],
                    values='Total_Population',
                    title='Population Distribution by State'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Urban vs Rural population
            if 'Urban_Population' in pop_df.columns and 'Rural_Population' in pop_df.columns:
                urban_rural = pd.DataFrame({
                    'Population_Type': ['Urban', 'Rural'],
                    'Population': [pop_df['Urban_Population'].sum(), pop_df['Rural_Population'].sum()]
                })
                fig = px.pie(
                    urban_rural,
                    values='Population',
                    names='Population_Type',
                    title='Urban vs Rural Population Distribution'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with analysis_tabs[3]:
        if 'vahan' in datasets:
            vehicle_df = datasets['vahan']
            
            # Vehicle type distribution
            if 'Vehicle_Class' in vehicle_df.columns and 'Registrations' in vehicle_df.columns:
                vehicle_dist = vehicle_df.groupby('Vehicle_Class')['Registrations'].sum()
                fig = px.pie(
                    values=vehicle_dist.values,
                    names=vehicle_dist.index,
                    title='Vehicle Registration Distribution by Type'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Fuel type trends
            if 'Fuel_Type' in vehicle_df.columns and 'Registrations' in vehicle_df.columns:
                fuel_trends = vehicle_df.groupby('Fuel_Type')['Registrations'].sum().sort_values(ascending=False)
                fig = px.bar(
                    x=fuel_trends.index,
                    y=fuel_trends.values,
                    title='Vehicle Registrations by Fuel Type',
                    color=fuel_trends.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)

def create_settings_page():
    """Create a settings and configuration page"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">⚙️ Settings & Configuration</h1>
        <p class="hero-subtitle">Customize your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Configuration
    st.subheader("🔌 API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Groq API settings
        api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API key")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            st.success("✅ API Key updated!")
        
        # Model selection
        model_options = [
            "llama-3.2-70b-versatile",
            "llama-3.2-11b-text-preview",
            "llama-3.1-70b-versatile"
        ]
        selected_model = st.selectbox("AI Model", model_options)
        
        # Temperature setting
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.1, 0.1)
    
    with col2:
        # Display settings
        st.subheader("🎨 Display Settings")
        
        # Theme toggle (mock - Streamlit handles themes)
        theme_option = st.radio("Theme Preference", ["Auto", "Dark", "Light"])
        
        # Chart preferences
        chart_style = st.selectbox("Chart Style", ["Plotly", "Altair", "Both"])
        
        # Animation preferences
        animations_enabled = st.checkbox("Enable Animations", value=True)
    
    # Data Management
    st.subheader("📊 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh All Data"):
            st.cache_data.clear()
            st.success("Cache cleared! Data will refresh on next load.")
    
    with col2:
        if st.button("📥 Export Chat History"):
            if st.session_state.messages:
                chat_data = {
                    "exported_at": datetime.now().isoformat(),
                    "messages": st.session_state.messages
                }
                st.download_button(
                    "📄 Download JSON",
                    data=json.dumps(chat_data, indent=2),
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No chat history to export.")
    
    with col3:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
    
    # System Information
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Application Version**: 1.0.0
        **Streamlit Version**: {st.__version__}
        **Python Version**: {os.sys.version.split()[0]}
        **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """)
    
    with col2:
        # Dataset status
        datasets = load_datasets()
        dataset_status = []
        for name, df in datasets.items():
            if isinstance(df, pd.DataFrame):
                status = f"✅ {name}: {len(df)} records"
            else:
                status = f"ℹ️ {name}: metadata"
            dataset_status.append(status)
        
        st.info("**Dataset Status**:\n" + "\n".join(dataset_status))

# Navigation function
def create_navigation():
    """Create navigation sidebar"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        page_options = {
            "🏠 Home": "home",
            "📊 Data Explorer": "explorer", 
            "📈 Analytics Dashboard": "analytics",
            "⚙️ Settings": "settings"
        }
        
        selected_page = st.radio("Go to:", list(page_options.keys()))
        return page_options[selected_page]

# Enhanced main function
def main_enhanced():
    """Enhanced main function with multiple pages"""
    
    # Load custom CSS first
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Create navigation
    current_page = create_navigation()
    
    # Route to appropriate page
    if current_page == "home":
        main()  # Original chat interface
    elif current_page == "explorer":
        create_data_explorer_page()
    elif current_page == "analytics":
        create_analytics_dashboard()
    elif current_page == "settings":
        create_settings_page()

# Import all the functions from the original app
# (The functions from the previous app.py would be included here)
# For brevity, I'm not repeating them all, but they would be included

if __name__ == "__main__":
    # Use enhanced main function
    main_enhanced()
