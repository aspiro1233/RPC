import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Clean Air - AI Health & Environment Insights",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "AI-powered insights on air quality, health data, and environmental trends"
    }
)

import pandas as pd
try:
    import plotly.express as px
    import plotly.graph_objects as go
    print("Successfully imported plotly!")
except ImportError as e:
    st.error(f"Error importing plotly: {e}")
    print(f"Error importing plotly: {e}")
    import sys
    print(f"Python path: {sys.path}")
    # Use alternative visualization library
    import altair as alt
from groq import Groq
import os
from datetime import datetime
import time
import json
from typing import List, Dict, Any
import altair as alt
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

# Page configuration moved to the top

# Custom CSS for beautiful UI
def load_custom_css():
    # Add CSS styles as a regular string (no f-string) to avoid syntax errors
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Variables - Enterprise Color Scheme */
    :root {
        --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        --secondary-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --neutral-color: #64748b;
        --glass-bg: rgba(15, 23, 42, 0.6);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom Header */
    .hero-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #667eea22, #764ba222, #4facfe22);
        animation: gradientMove 6s ease-in-out infinite;
    }
    
    @keyframes gradientMove {
        0% { transform: translateX(-50px); opacity: 0.5; }
        50% { transform: translateX(50px); opacity: 0.8; }
        100% { transform: translateX(-50px); opacity: 0.5; }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #cbd5e1;
        font-weight: 300;
        position: relative;
        z-index: 2;
    }
    
    .enterprise-badge {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: #f0f9ff;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 3;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Chat Container */
    .chat-container {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message Bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #f0f9ff;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 8px 20px;
        margin: 0.5rem 0 0.5rem auto;
        max-width: 80%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: #f8fafc;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 8px;
        margin: 0.5rem auto 0.5rem 0;
        max-width: 85%;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
        border-color: rgba(79, 172, 254, 0.3);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #f0f9ff;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 172, 254, 0.4);
    }
    
    /* Metric Cards */
    [data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    /* Chat Input Styling */
    .stChatInput > div > div > textarea {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #f8fafc;
    }
    
    /* Loading Animation */
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    
    .loading-dots div {
        position: absolute;
        top: 33px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #4facfe;
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }
    
    .loading-dots div:nth-child(1) {
        left: 8px;
        animation: lds-ellipsis1 0.6s infinite;
    }
    
    .loading-dots div:nth-child(2) {
        left: 8px;
        animation: lds-ellipsis2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(3) {
        left: 32px;
        animation: lds-ellipsis2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(4) {
        left: 56px;
        animation: lds-ellipsis3 0.6s infinite;
    }
    
    @keyframes lds-ellipsis1 {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }
    
    @keyframes lds-ellipsis2 {
        0% { transform: translate(0, 0); }
        100% { transform: translate(24px, 0); }
    }
    
    @keyframes lds-ellipsis3 {
        0% { transform: scale(1); }
        100% { transform: scale(0); }
    }
    
    /* Data Visualization Styling */
    .plot-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Code block styling - hiding all code */
    pre {
        display: none !important;
    }
    
    code {
        display: none !important;
    }
    
    .language-python {
        display: none !important;
    }
    
    /* Quick Query Buttons */
    .quick-query-btn {
        background: rgba(79, 172, 254, 0.1);
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        color: #4facfe;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .quick-query-btn:hover {
        background: rgba(79, 172, 254, 0.2);
        transform: translateY(-1px);
    }
    
    /* Status Indicators */
    .status-online {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-loading {
        color: #f59e0b;
        font-weight: 600;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1.2rem; }
        .user-message, .bot-message { max-width: 95%; }
        .chat-container { min-height: 400px; }
    }
    
    /* Override Streamlit's default white background for metrics */
    div[data-testid="stMetric"], 
    div[data-testid="metric-container"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #f0f9ff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    div[data-testid="stMetric"] label, 
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
    }
    
    div[data-testid="stMetric"] > div {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "datasets_loaded" not in st.session_state:
        st.session_state.datasets_loaded = False
    if "groq_client" not in st.session_state:
        st.session_state.groq_client = None
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""
    if "user_role" not in st.session_state:
        st.session_state.user_role = "Viewer"  # Default role
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True
    if "show_advanced" not in st.session_state:
        st.session_state.show_advanced = False

# Load environment variables
@st.cache_data
def load_environment():
    """Load environment variables and API keys"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except:
        return False

# Initialize Groq client
@st.cache_resource
def initialize_groq_client():
    """Initialize Groq client with API key"""
    try:
        # Try to get API key from Streamlit secrets first (for deployment)
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            # Fallback to environment variable (for local development)
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            st.error("❌ GROQ_API_KEY not found. Please set it in Streamlit secrets or environment variables.")
            st.info("🔑 Get your API key from: https://console.groq.com/")
            return None
        
        try:
            client = Groq(api_key=api_key)
            # Test the client with a minimal API call
            model_name = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=model_name,
                max_tokens=10
            )
            st.success("✅ Successfully connected to Groq API")
            return client
        except Exception as e:
            st.error(f"❌ Error connecting to Groq API: {str(e)}")
            st.info("🔧 Please check your API key and internet connection")
            return None
    except Exception as e:
        st.error(f"❌ Error initializing Groq client: {str(e)}")
        return None

# Load datasets
@st.cache_data
def load_datasets():
    """Load all CSV datasets with caching"""
    datasets = {}
    data_folder = "data"
    
    try:
        # Create data folder if it doesn't exist
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            
        # Dataset filenames
        dataset_files = {
            "aqi": "aqi.csv",
            "idsp": "idsp.csv", 
            "population": "population_projection.csv",
            "vahan": "vahan.csv"
        }
        
        for key, filename in dataset_files.items():
            filepath = os.path.join(data_folder, filename)
            if os.path.exists(filepath):
                try:
                    # Try different encodings if utf-8 fails
                    try:
                        datasets[key] = pd.read_csv(filepath, encoding='utf-8')
                    except UnicodeDecodeError:
                        # Try with common alternative encodings
                        encodings = ['latin1', 'ISO-8859-1', 'cp1252']
                        for encoding in encodings:
                            try:
                                datasets[key] = pd.read_csv(filepath, encoding=encoding)
                                print(f"Successfully loaded {filename} with {encoding} encoding")
                                break
                            except UnicodeDecodeError:
                                continue
                        else:
                            raise UnicodeDecodeError(f"Failed to decode {filename} with any encoding")
                    st.sidebar.success(f"✅ {filename} loaded successfully")
                except Exception as e:
                    st.sidebar.error(f"❌ Error loading {filename}: {str(e)}")
                    # Create sample data for demonstration
                    datasets[key] = create_sample_data(key)
            else:
                st.sidebar.warning(f"⚠️ {filename} not found. Using sample data.")
                datasets[key] = create_sample_data(key)
        
        # Load metadata
        meta_file = os.path.join(data_folder, "meta_data.txt")
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                datasets["metadata"] = f.read()
        else:
            datasets["metadata"] = "Metadata file not found."
            
        return datasets
        
    except Exception as e:
        st.error(f"❌ Error loading datasets: {str(e)}")
        return {}

# Create sample data for demonstration
def create_sample_data(dataset_type):
    """Create sample data when CSV files are not available"""
    if dataset_type == "aqi":
        return pd.DataFrame({
            'City': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata'],
            'State': ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'West Bengal'],
            'AQI': [156, 142, 98, 87, 134],
            'PM2.5': [89, 78, 45, 38, 72],
            'PM10': [145, 128, 82, 76, 119],
            'Year': [2025, 2025, 2025, 2025, 2025],
            'Date': ['2025-01-15', '2025-01-15', '2025-01-15', '2025-01-15', '2025-01-15']
        })
    elif dataset_type == "idsp":
        return pd.DataFrame({
            'State': ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Uttar Pradesh', 'Gujarat'],
            'District': ['Mumbai', 'Chennai', 'Bangalore', 'Lucknow', 'Ahmedabad'],
            'Disease': ['Dengue', 'Chikungunya', 'Malaria', 'Typhoid', 'Hepatitis'],
            'Cases': [234, 156, 89, 167, 123],
            'Date': ['2025-01-10', '2025-01-08', '2025-01-12', '2025-01-09', '2025-01-11']
        })
    elif dataset_type == "population":
        return pd.DataFrame({
            'State': ['Uttar Pradesh', 'Maharashtra', 'Bihar', 'West Bengal', 'Madhya Pradesh'],
            'Year': [2025, 2025, 2025, 2025, 2025],
            'Male_Population': [12000000, 6200000, 5800000, 4900000, 4100000],
            'Female_Population': [11500000, 5800000, 5400000, 4700000, 3900000],
            'Total_Population': [23500000, 12000000, 11200000, 9600000, 8000000]
        })
    elif dataset_type == "vahan":
        return pd.DataFrame({
            'State': ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Uttar Pradesh', 'Gujarat'],
            'Vehicle_Class': ['Two Wheeler', 'Four Wheeler', 'Two Wheeler', 'Four Wheeler', 'Two Wheeler'],
            'Fuel_Type': ['Petrol', 'Petrol', 'Electric', 'Diesel', 'CNG'],
            'Registrations': [150000, 45000, 12000, 67000, 89000],
            'Year': [2024, 2024, 2024, 2024, 2024]
        })
    else:
        return pd.DataFrame()

# Query classification and processing
def classify_query(query: str) -> List[str]:
    """Classify which datasets are relevant for the query"""
    query_lower = query.lower()
    relevant_datasets = []
    
    # Air quality keywords
    if any(keyword in query_lower for keyword in ['air quality', 'aqi', 'pollution', 'pm2.5', 'pm10', 'pollutant']):
        relevant_datasets.append('aqi')
    
    # Health/disease keywords
    if any(keyword in query_lower for keyword in ['disease', 'outbreak', 'health', 'dengue', 'malaria', 'illness']):
        relevant_datasets.append('idsp')
    
    # Population keywords
    if any(keyword in query_lower for keyword in ['population', 'demographic', 'people', 'growth']):
        relevant_datasets.append('population')
    
    # Vehicle keywords
    if any(keyword in query_lower for keyword in ['vehicle', 'car', 'bike', 'transport', 'registration', 'electric']):
        relevant_datasets.append('vahan')
    
    # If no specific dataset identified, include all
    if not relevant_datasets:
        relevant_datasets = ['aqi', 'idsp', 'population', 'vahan']
    
    return relevant_datasets

# Build context for AI
def build_context(query: str, datasets: Dict) -> str:
    """Build context from relevant datasets for AI processing"""
    relevant_datasets = classify_query(query)
    context_parts = []
    
    context_parts.append(f"User Query: {query}\n")
    context_parts.append("Available Data:\n")
    
    for dataset_name in relevant_datasets:
        if dataset_name in datasets:
            df = datasets[dataset_name]
            context_parts.append(f"\n{dataset_name.upper()} Dataset:")
            context_parts.append(f"Shape: {df.shape}")
            context_parts.append(f"Columns: {list(df.columns)}")
            
            # Add sample data (first few rows)
            if len(df) > 0:
                context_parts.append("Sample data:")
                context_parts.append(df.head(3).to_string())
            
            # Add summary statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                context_parts.append("\nSummary Statistics:")
                context_parts.append(df[numeric_cols].describe().to_string())
    
    return "\n".join(context_parts)

# Generate AI response
def generate_ai_response(query: str, context: str, groq_client) -> str:
    """Generate AI response using Groq API"""
    try:
        # Get model from environment or use default
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        
        system_prompt = """You are an AI assistant specialized in analyzing air quality, health, population, and vehicle data for India. 

        Guidelines:
        1. Provide accurate, data-driven insights based ONLY on the provided datasets
        2. Include specific numbers, trends, and comparisons when available
        3. Cite data sources clearly (mention which dataset)
        4. If data is insufficient, clearly state limitations
        5. Suggest relevant follow-up questions
        6. Format responses clearly with bullet points or sections when appropriate
        7. Never make up or hallucinate data not present in the provided context
        8. DO NOT include any code snippets in your responses - focus only on the analysis and insights
        9. Structure your response in clear sections with headings, bullet points, and numerical data
        
        Always ground your responses in the actual data provided and include source citations."""
        
        user_prompt = f"""Context Data:\n{context}\n\nPlease analyze this data and provide insights to answer the user's question. Be specific and cite the data sources. DO NOT include any code snippets in your response. Just focus on explaining the insights from the data in a clear, easy-to-understand way with bullet points and data citations."""
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=model_name,
            temperature=0.1,
            max_tokens=1000,
            stream=False
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error generating response: {str(e)}. Please check your API key and try again."

# Create visualizations
def create_visualization(datasets: Dict, query: str):
    """Create relevant visualizations based on query and data"""
    query_lower = query.lower()
    st.markdown("### 📊 Data Visualizations")
    st.markdown("Here are some visual insights related to your query:")
    
    # Create a visualization counter to track if any were created
    visualizations_created = 0
    
    # Air Quality Visualization - Always show if data is available
    if 'aqi' in datasets:
        df = datasets['aqi']
        if 'AQI' in df.columns and 'City' in df.columns:
            st.markdown("#### 🌬️ Air Quality Analysis")
            fig = px.bar(
                df.head(10), 
                x='City', 
                y='AQI',
                title='Air Quality Index by City',
                color='AQI',
                color_continuous_scale='Reds',
                text='AQI'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f0f9ff',
                height=450
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.info("💡 **Understanding AQI**: 0-50 Good, 51-100 Moderate, 101-150 Unhealthy for Sensitive Groups, 151+ Unhealthy")
            visualizations_created += 1
    
    # Population Visualization - Always show if data is available
    if 'population' in datasets:
        df = datasets['population']
        if 'Total_Population' in df.columns and 'State' in df.columns:
            st.markdown("#### 👥 Population Analysis")
            
            # Create two visualizations for population data
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart for distribution
                fig1 = px.pie(
                    df.head(8),
                    values='Total_Population',
                    names='State',
                    title='Population Distribution by State',
                    hole=0.4
                )
                fig1.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f0f9ff'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Bar chart for easier comparison
                fig2 = px.bar(
                    df.head(8).sort_values('Total_Population', ascending=False),
                    x='State',
                    y='Total_Population',
                    title='Population by State (Ranked)',
                    text='Total_Population'
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f0f9ff',
                    xaxis={'categoryorder': 'total descending'}
                )
                fig2.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                st.plotly_chart(fig2, use_container_width=True)
            
            visualizations_created += 1
    
    # Vehicle Registration Visualization - Always show if data is available
    if 'vahan' in datasets:
        df = datasets['vahan']
        if 'Registrations' in df.columns and 'State' in df.columns:
            st.markdown("#### 🚗 Vehicle Registration Analysis")
            
            # Scatter plot
            fig = px.scatter(
                df,
                x='State',
                y='Registrations',
                size='Registrations',
                color='Fuel_Type',
                title='Vehicle Registrations by State and Fuel Type',
                hover_name='State'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f0f9ff',
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Add a bar chart showing registrations by fuel type
            fuel_data = df.groupby('Fuel_Type')['Registrations'].sum().reset_index()
            fig2 = px.bar(
                fuel_data,
                x='Fuel_Type',
                y='Registrations',
                title='Vehicle Registrations by Fuel Type',
                color='Fuel_Type'
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f0f9ff'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            visualizations_created += 1
            
    # Health/Disease Visualization - Always show if data is available
    if 'idsp' in datasets:
        df = datasets['idsp']
        if 'Disease' in df.columns and 'Cases' in df.columns:
            st.markdown("#### 🏥 Health & Disease Analysis")
            
            # Group by disease
            disease_data = df.groupby('Disease')['Cases'].sum().reset_index().sort_values('Cases', ascending=False)
            
            # Create disease distribution chart
            fig = px.bar(
                disease_data,
                x='Disease',
                y='Cases',
                title='Disease Cases Distribution',
                color='Cases',
                text='Cases'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f0f9ff',
                height=400
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # If 'State' column exists, show state-wise distribution
            if 'State' in df.columns:
                # Create state-wise distribution chart
                state_data = df.groupby('State')['Cases'].sum().reset_index().sort_values('Cases', ascending=False)
                fig2 = px.pie(
                    state_data.head(6),
                    values='Cases',
                    names='State',
                    title='Disease Cases by State'
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#f0f9ff'
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            visualizations_created += 1
            
    # Show a message if no visualizations were created
    if visualizations_created == 0:
        st.warning("No data available to create visualizations. Please check your datasets.")
        
    # Add a note about the visualizations
    st.markdown("**Note**: These visualizations are generated automatically to help you understand the data better.")

# Main app
def main():
    # Display Available Data section
    st.markdown("## 📊 Available Data")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌬️ Air Quality")
        st.markdown("**235,785**")
        st.caption("Records Available")
        st.caption("AQI levels across cities")

        st.markdown("### 👥 Demographics")
        st.markdown("**8,893**")
        st.caption("Records Available")
        st.caption("Population statistics")

    with col2:
        st.markdown("### 🏥 Health Surveillance")
        st.markdown("**6,477**")
        st.caption("Records Available")
        st.caption("Disease tracking data (updated)")
        # Add a debugging indicator
        st.text("Debug: App.py is displaying 6,477")

        st.markdown("### 🚗 Vehicle Registry")
        st.markdown("**64,841**")
        st.caption("Records Available")
        st.caption("Transportation data")
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Load environment
    load_environment()
    
    # Initialize Groq client
    if not st.session_state.groq_client:
        st.session_state.groq_client = initialize_groq_client()
    
    # Hero Header - Enterprise Edition
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">Clean Air Enterprise</h1>
        <p class="hero-subtitle">AI-Powered Health & Environment Intelligence Platform</p>
        <div class="enterprise-badge">Enterprise Edition</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load datasets
    datasets = load_datasets()
    st.session_state.datasets_loaded = bool(datasets)
    
    # Sidebar
    with st.sidebar:
        colored_header(
            label="🌬️ Clean Air Assistant",
            description="Your AI companion for environmental insights",
            color_name="blue-70"
        )
        
        # Dataset Status
        st.subheader("📊 Dataset Status")
        if datasets:
            for name, df in datasets.items():
                if isinstance(df, pd.DataFrame):
                    st.metric(
                        label=f"{name.upper()} Dataset",
                        value=f"{len(df)} records",
                        delta=f"{df.shape[1]} columns"
                    )
        
        add_vertical_space(2)
        
        # Quick Query Buttons
        st.subheader("🚀 Quick Queries")
        quick_queries = [
            "Which cities have the worst air quality?",
            "Show disease outbreaks by state",
            "Compare electric vehicle adoption",
            "Population growth trends",
            "Air quality vs vehicle registrations"
        ]
        
        for query in quick_queries:
            if st.button(query, key=f"quick_{query[:10]}"):
                st.session_state.current_query = query
        
        add_vertical_space(2)
        
        # Enterprise Features
        st.subheader("🏢 Enterprise Features")
        
        # User Role Selector
        user_roles = ["Executive", "Analyst", "Operations", "Viewer"]
        selected_role = st.selectbox("User Role", user_roles, index=user_roles.index(st.session_state.user_role) if st.session_state.user_role in user_roles else 3)
        if selected_role != st.session_state.user_role:
            st.session_state.user_role = selected_role
            st.rerun()
        
        # Advanced Features Toggle
        st.checkbox("Show Advanced Features", key="show_advanced")
        
        # Display Mode
        st.checkbox("Dark Mode", key="dark_mode")
            
        add_vertical_space(2)
        
        # Settings
        st.subheader("⚙️ Settings")
        
        # API Status
        if st.session_state.groq_client:
            st.success("🟢 Groq API Connected")
        else:
            st.error("🔴 Groq API Not Connected")
        
        # Dataset refresh
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
            
        # Documentation Link
        st.markdown("[📄 Enterprise Documentation](https://github.com/your-repo/clean-air-assistant)")
    
    # Main Chat Interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat Messages Container
        chat_container = st.container()
        
        with chat_container:
            # Welcome message
            if not st.session_state.messages:
                st.markdown("""
                <div class="bot-message">
                    <h4>👋 Welcome to Clean Air Assistant!</h4>
                    <p>I can help you analyze:</p>
                    <ul>
                        <li>🌬️ Air Quality Index data across cities</li>
                        <li>🏥 Disease outbreak patterns by region</li>
                        <li>🚗 Vehicle registration trends</li>
                        <li>👥 Population demographics and projections</li>
                    </ul>
                    <p><em>Try asking: "Which cities have the worst air quality?" or "Show me disease outbreaks in Maharashtra"</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display chat messages
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat Input
        query = st.chat_input("Ask me about air quality, health data, or population trends...")
        
        # Handle quick query selection
        if st.session_state.current_query:
            query = st.session_state.current_query
            st.session_state.current_query = ""
        
        # Process query
        if query:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Display user message immediately
            st.markdown(f'<div class="user-message">{query}</div>', unsafe_allow_html=True)
            
            # Generate response
            if st.session_state.groq_client and datasets:
                with st.spinner("🤖 AI is thinking..."):
                    # Build context
                    context = build_context(query, datasets)
                    
                    # Generate AI response
                    response = generate_ai_response(query, context, st.session_state.groq_client)
                    
                    # Add bot response
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Display bot response with text analysis
                    st.markdown(f'<div class="bot-message">{response}</div>', unsafe_allow_html=True)
                    
                    # Always create visualizations for every query
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    create_visualization(datasets, query)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            else:
                error_msg = "❌ Please check your API connection and ensure datasets are loaded."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.error(error_msg)
            
            # Rerun to update chat
            st.rerun()
    
    with col2:
        # Show different dashboard based on user role
        if st.session_state.user_role == "Executive":
            # Executive Dashboard
            st.subheader("📊 Executive Dashboard")
            
            if datasets:
                # Key Performance Indicators
                st.metric("Critical Air Quality Alerts", "3", delta="-2")
                st.metric("Disease Outbreaks", "5", delta="0")
                st.metric("Environmental Compliance", "92%", delta="4%")
                
                # Air Quality Risk Score
                risk_score = 67
                st.progress(risk_score/100, text=f"Risk Score: {risk_score}/100")
                
                # Quick Reports
                st.subheader("📑 Quick Reports")
                report_col1, report_col2 = st.columns(2)
                with report_col1:
                    if st.button("📊 Executive Summary"):
                        st.session_state.current_query = "Generate an executive summary of air quality and health risks"
                        st.rerun()
                with report_col2:
                    if st.button("🚨 Risk Assessment"):
                        st.session_state.current_query = "Show highest environmental risk areas"
                        st.rerun()
                        
        elif st.session_state.user_role == "Analyst":
            # Analyst Dashboard
            st.subheader("� Analysis Tools")
            
            if datasets:
                # Analysis Options
                analysis_options = ["Trend Analysis", "Correlation Study", "Geographic Distribution", "Custom Query"]
                selected_analysis = st.selectbox("Analysis Type", analysis_options)
                
                if selected_analysis == "Custom Query":
                    st.text_area("SQL Query", "SELECT * FROM air_quality\nWHERE AQI > 150\nORDER BY AQI DESC\nLIMIT 10", height=100)
                    st.button("Run Analysis")
                
                # Export Options
                st.subheader("📤 Export Options")
                export_col1, export_col2 = st.columns(2)
                with export_col1:
                    st.button("Export to CSV")
                with export_col2:
                    st.button("Export to Excel")
                    
                # Advanced Filtering
                if st.session_state.show_advanced:
                    st.subheader("🔧 Advanced Filters")
                    st.slider("Confidence Threshold", 0, 100, 75)
                    st.multiselect("Data Sources", ["Sensors", "Satellites", "Stations", "Models"])
                
        elif st.session_state.user_role == "Operations":
            # Operations Dashboard
            st.subheader("🔔 Alerts & Monitoring")
            
            if datasets:
                # Alert Status
                st.metric("Active Alerts", "3", delta="-1")
                
                # Alert List
                st.info("🚨 Delhi AQI exceeds threshold (245)")
                st.warning("⚠️ Mumbai disease cases rising (23%)")
                st.success("✅ Chennai air quality improving (33%)")
                
                # Action Items
                st.subheader("📋 Action Items")
                st.checkbox("Review Delhi monitoring stations", value=True)
                st.checkbox("Dispatch mobile testing units", value=False)
                st.checkbox("Update regional compliance reports", value=False)
                
                # Equipment Status
                if st.session_state.show_advanced:
                    st.subheader("🔌 Equipment Status")
                    st.progress(0.92, text="Monitoring Network: 92% Online")
                    st.progress(0.87, text="Data Pipeline: 87% Capacity")
        
        else:
            # Standard Dashboard (Viewer)
            st.subheader("�📈 Data Overview")
            
            if datasets:
                # Total records across all datasets
                total_records = sum(len(df) for df in datasets.values() if isinstance(df, pd.DataFrame))
                st.metric("Total Records", f"{total_records:,}")
                
                # Recent activity (mock data)
                st.metric("Queries Today", "47", delta="12")
                st.metric("Active Users", "156", delta="23")
                
                # Dataset health indicators
                st.subheader("🏥 System Health")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("API Status", "🟢 Online")
                with col_b:
                    st.metric("Data Fresh", "🟢 Current")

# Style metric cards
style_metric_cards()

if __name__ == "__main__":
    main()
