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
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# Page configuration
st.set_page_config(
    page_title="🌿 Clean Air AI Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_user_friendly_css():
    """Load CSS for a clean, user-friendly interface"""
    # Add syntax highlighting styles from Pygments
    pygments_css = HtmlFormatter(style='monokai').get_style_defs('.highlight')
    
    st.markdown(f"""
    <style>
    /* Pygments Syntax Highlighting */
    {pygments_css}
    
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        min-height: 100vh;
        color: #f1f5f9;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, .stDeployButton {visibility: hidden;}
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: float 8s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(180deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        text-align: center;
        color: #f0f9ff;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 0.4rem 1.2rem;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .badge-icon {
        font-size: 1rem;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 1.5rem;
        opacity: 0.9;
        line-height: 1.5;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .feature-highlight {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .feature-highlight:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .feature-highlight-icon {
        font-size: 1rem;
    }
    
    /* Code block styling */
    pre {
        background: rgba(15, 23, 42, 0.8) !important;
        border-radius: 10px !important;
        padding: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin: 15px 0 !important;
        overflow-x: auto !important;
        position: relative !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3) !important;
    }
    
    pre code {
        color: #f8fafc !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        line-height: 1.7 !important;
    }
    
    .code-header {
        background: rgba(30, 41, 59, 0.95);
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
        font-size: 0.8rem;
        color: #94a3b8;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Explore Section */
    .explore-section {
        text-align: center;
        margin: 2rem 0 1.5rem 0;
    }
    
    .explore-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    
    .explore-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 0;
    }
    
    /* Interactive Cards */
    .interactive-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        color: #f1f5f9;
    }
    
    .interactive-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    
    .interactive-card.air-quality::before {
        background: linear-gradient(90deg, #10b981, #34d399);
    }
    
    .interactive-card.health::before {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
    }
    
    .interactive-card.demographics::before {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    
    .interactive-card.transportation::before {
        background: linear-gradient(90deg, #8b5cf6, #a78bfa);
    }
    
    .interactive-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        border-color: rgba(255,255,255,0.2);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .card-icon {
        font-size: 2rem;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
    }
    
    .card-description {
        font-size: 0.95rem;
        color: #cbd5e1;
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    
    .card-stats {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
    }
    
    .stat-number {
        display: block;
        font-size: 1.3rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 0.2rem;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .card-examples {
        background: rgba(0,0,0,0.2);
        border-radius: 10px;
        padding: 0.8rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .example-question {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 6px;
        padding: 0.4rem 0.8rem;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        color: #e2e8f0;
        font-style: italic;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .example-question:hover {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
        transform: translateX(3px);
        color: #f1f5f9;
    }
    
    .example-question::before {
        content: '💭 ';
        margin-right: 0.3rem;
    }
    
    /* Quick Actions Section */
    .quick-actions-section {
        margin: 1.5rem 0 1rem 0;
        text-align: center;
    }
    
    .section-header {
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.4rem;
    }
    
    .section-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 0;
    }
    
    /* Question Cards */
    .question-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
    }
    
    .question-card.green-theme::before {
        background: linear-gradient(90deg, #10b981, #34d399);
    }
    
    .question-card.orange-theme::before {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
    }
    
    .question-card.blue-theme::before {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    
    .question-card.purple-theme::before {
        background: linear-gradient(90deg, #8b5cf6, #a78bfa);
    }
    
    .question-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border-color: rgba(255,255,255,0.2);
    }
    
    .question-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
    }
    
    .question-icon {
        font-size: 1.5rem;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .question-category {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94a3b8;
        background: rgba(255,255,255,0.1);
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .question-text {
        font-size: 0.9rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.8rem;
        line-height: 1.3;
        text-align: left;
    }
    
    .question-action {
        font-size: 0.8rem;
        color: #60a5fa;
        font-weight: 500;
        text-align: right;
        opacity: 0.7;
        transition: all 0.3s ease;
    }
    
    .question-card:hover .question-action {
        opacity: 1;
        transform: translateX(3px);
    }
    
    /* Show the streamlit buttons but style them to match */
    .stButton > button {
        background: linear-gradient(135deg, #374151, #4b5563) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 0.3rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: #f0f9ff !important;
        border-color: #3b82f6 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Metrics */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.8rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        color: #f1f5f9;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Status Indicators */
    .status-online {
        color: #34d399;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
    }
    
    .status-offline {
        color: #f87171;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
    }
    
    /* Chat Interface */
    .chat-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        min-height: 400px;
        color: #f1f5f9;
    }
    
    .chat-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .chat-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 0;
    }
    
    /* Message Styling */
    .message {
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: #f0f9ff;
        padding: 1rem 1.2rem;
        border-radius: 16px 16px 4px 16px;
        margin-left: 15%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(240,249,255,0.1);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        border: 1px solid rgba(255,255,255,0.1);
        color: #f1f5f9;
        padding: 1.2rem;
        border-radius: 16px 16px 16px 4px;
        margin-right: 15%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .message-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    /* Quick Actions */
    .quick-actions {
        background: #f8fafc;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .quick-actions h3 {
        color: #1e293b;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .action-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .action-btn {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        color: #475569;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .action-btn:hover {
        background: #3b82f6;
        color: #f0f9ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Data Cards */
    .data-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        color: #f1f5f9;
    }
    
    .data-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .data-card h4 {
        color: #f1f5f9;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.1);
        padding: 0.8rem 1.2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(30, 41, 59, 0.8);
        color: #f1f5f9;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        background: rgba(30, 41, 59, 0.9);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: #f0f9ff;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: #f8fafc;
    }
    
    /* Metrics */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Status Indicators */
    .status-online {
        color: #10b981;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
    }
    
    .status-offline {
        color: #ef4444;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
    }
    
    /* Loading Animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid #f1f5f9;
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .welcome-title { font-size: 2rem; }
        .welcome-subtitle { font-size: 1.1rem; }
        .user-message, .bot-message { margin-left: 0; margin-right: 0; }
        .feature-grid { grid-template-columns: 1fr; }
        .metric-container { grid-template-columns: repeat(2, 1fr); }
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

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "datasets_loaded" not in st.session_state:
        st.session_state.datasets_loaded = False
    if "groq_client" not in st.session_state:
        st.session_state.groq_client = None

def load_environment():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except:
        return False

def initialize_groq_client():
    """Initialize Groq client"""
    # Fallback API key if the primary one fails
    fallback_api_key = "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"
    
    try:
        # Try primary API key first
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("Primary Groq API key not found. Trying fallback key...")
            api_key = fallback_api_key
        
        try:
            client = Groq(api_key=api_key)
            # Test the client with a minimal API call
            client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model="llama-3.1-8b-instant",
                max_tokens=10
            )
            print("Successfully connected to Groq API")
            return client
        except Exception as primary_error:
            if api_key != fallback_api_key:
                print(f"Error with primary API key. Trying fallback key...")
                try:
                    client = Groq(api_key=fallback_api_key)
                    # Test the fallback client
                    client.chat.completions.create(
                        messages=[{"role": "user", "content": "test"}],
                        model="llama-3.1-8b-instant",
                        max_tokens=10
                    )
                    print("Successfully connected to Groq API with fallback key")
                    return client
                except Exception as fallback_error:
                    print(f"Both API keys failed.")
                    return None
            else:
                print(f"Fallback API key also failed.")
                return None
    except Exception as e:
        print(f"Error initializing Groq client: {str(e)}")
        return None

def load_datasets():
    """Load CSV datasets with fallback to sample data"""
    datasets = {}
    data_folder = "data"
    
    try:
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        
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
                            # If all encodings fail, use sample data
                            datasets[key] = create_sample_data(key)
                except Exception:
                    datasets[key] = create_sample_data(key)
            else:
                datasets[key] = create_sample_data(key)
        
        return datasets
    except Exception:
        return {key: create_sample_data(key) for key in ["aqi", "idsp", "population", "vahan"]}

def create_sample_data(dataset_type):
    """Create sample data for demonstration"""
    if dataset_type == "aqi":
        return pd.DataFrame({
            'City': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad'],
            'State': ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Telangana', 'Maharashtra', 'Gujarat'],
            'AQI': [156, 142, 98, 87, 134, 112, 89, 145],
            'PM2.5': [89, 78, 45, 38, 72, 56, 42, 81],
            'PM10': [145, 128, 82, 76, 119, 98, 73, 132],
            'Category': ['Unhealthy', 'Unhealthy', 'Moderate', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy for Sensitive Groups', 'Moderate', 'Unhealthy']
        })
    elif dataset_type == "idsp":
        return pd.DataFrame({
            'State': ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Uttar Pradesh', 'Gujarat', 'Rajasthan'],
            'District': ['Mumbai', 'Chennai', 'Bangalore', 'Lucknow', 'Ahmedabad', 'Jaipur'],
            'Disease': ['Dengue', 'Chikungunya', 'Malaria', 'Typhoid', 'Hepatitis', 'Dengue'],
            'Cases': [234, 156, 89, 167, 123, 198],
            'Population_at_Risk': [12000000, 8500000, 10200000, 7800000, 9200000, 6700000]
        })
    elif dataset_type == "population":
        return pd.DataFrame({
            'State': ['Uttar Pradesh', 'Maharashtra', 'Bihar', 'West Bengal', 'Madhya Pradesh', 'Tamil Nadu'],
            'Total_Population': [23500000, 12000000, 11200000, 9600000, 8000000, 7200000],
            'Urban_Population': [4700000, 5400000, 1300000, 3100000, 2000000, 3400000],
            'Rural_Population': [18800000, 6600000, 9900000, 6500000, 6000000, 3800000],
            'Growth_Rate': [2.1, 1.6, 2.4, 1.3, 2.0, 1.1]
        })
    elif dataset_type == "vahan":
        return pd.DataFrame({
            'State': ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Uttar Pradesh', 'Gujarat', 'Delhi'],
            'Vehicle_Class': ['Two Wheeler', 'Four Wheeler', 'Two Wheeler', 'Four Wheeler', 'Two Wheeler', 'Electric Vehicle'],
            'Fuel_Type': ['Petrol', 'Petrol', 'Electric', 'Diesel', 'CNG', 'Electric'],
            'Registrations': [150000, 45000, 12000, 67000, 89000, 23000],
            'Year': [2024, 2024, 2024, 2024, 2024, 2024]
        })
    return pd.DataFrame()

def generate_ai_response(query: str, context: str, groq_client) -> str:
    """Generate AI response using Groq API"""
    if not groq_client:
        return "I'm sorry, but I'm currently unable to connect to my AI brain due to API key issues. Please check your API key configuration and try again later. 🤖💭"
    
    try:
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        system_prompt = """You are a friendly and helpful AI assistant specialized in environmental health and data analysis. 

Your personality:
- Speak in a conversational, easy-to-understand manner
- Use simple language and avoid technical jargon
- Be encouraging and supportive
- Provide actionable insights
- Ask follow-up questions to help users explore the data

Guidelines:
1. Base your answers ONLY on the provided data
2. Explain findings in simple terms
3. Use bullet points and clear structure
4. Include specific numbers when available
5. Suggest what users might want to explore next
6. If data is limited, explain what information is missing
7. ALWAYS include a Python code snippet that shows how to perform the analysis related to the user's question
8. Format code properly in markdown code blocks with 'python' specified as the language

Code snippet guidelines:
- Include proper imports (pandas, matplotlib/plotly as needed)
- Show how to load the relevant datasets
- Include data filtering/selection relevant to the query
- Add at least one analysis technique (aggregation, calculation, etc.)
- Add a visualization step that creates a relevant chart
- Include brief comments explaining what the code does
- Keep code simple and readable

Always be helpful, accurate, and user-friendly!"""
        
        user_prompt = f"""Here's some data to help answer the user's question:

{context}

User Question: {query}

Please provide a helpful, easy-to-understand response based on this data. Use simple language and organize your answer clearly. 

IMPORTANT: Always include a Python code snippet that demonstrates how to analyze this data. Format the code in a markdown code block with ```python at the start and ``` at the end. The code should show data loading, filtering, analysis, and visualization steps relevant to the question."""
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=model_name,
            temperature=0.2,
            max_tokens=800,
            stream=False
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"I'm sorry, I'm having trouble connecting to my AI brain right now. Error: {str(e)}. Please try again in a moment! 🤖💭"

def build_context(query: str, datasets: Dict) -> str:
    """Build context from datasets for AI processing"""
    context_parts = [f"User is asking: {query}\n"]
    
    # Add relevant data summaries
    for name, df in datasets.items():
        if isinstance(df, pd.DataFrame) and len(df) > 0:
            context_parts.append(f"\n{name.upper()} Data Summary:")
            context_parts.append(f"- {len(df)} records available")
            context_parts.append(f"- Columns: {', '.join(df.columns.tolist())}")
            
            # Add sample data
            context_parts.append("\nSample data:")
            context_parts.append(df.head(3).to_string(index=False))
            
            # Add key statistics
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                for col in numeric_cols[:2]:  # Limit to 2 numeric columns
                    avg_val = df[col].mean()
                    max_val = df[col].max()
                    min_val = df[col].min()
                    context_parts.append(f"- {col}: Average {avg_val:.1f}, Range {min_val:.1f} to {max_val:.1f}")
    
    return "\n".join(context_parts)

def create_welcome_section():
    """Create the enhanced welcome section"""
    # Main hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-badge">
                <span class="badge-icon">🌍</span>
                <span class="badge-text">Environmental Health Intelligence</span>
            </div>
            <h1 class="hero-title">Clean Air AI Assistant</h1>
            <p class="hero-subtitle">
                Discover insights about air quality, health patterns, and environmental trends across India
            </p>
            <div class="hero-features">
                <div class="feature-highlight">
                    <span class="feature-highlight-icon">🤖</span>
                    <span class="feature-highlight-text">AI-Powered Analysis</span>
                </div>
                <div class="feature-highlight">
                    <span class="feature-highlight-icon">📊</span>
                    <span class="feature-highlight-text">Real Data Insights</span>
                </div>
                <div class="feature-highlight">
                    <span class="feature-highlight-icon">💬</span>
                    <span class="feature-highlight-text">Easy to Understand</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # What can you explore section
    st.markdown("""
    <div class="explore-section">
        <h2 class="explore-title">What can you explore today?</h2>
        <p class="explore-subtitle">Choose what interests you most, or ask me anything!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive feature cards
    cols = st.columns(2)
    
    with cols[0]:
        st.markdown("""
        <div class="interactive-card air-quality">
            <div class="card-header">
                <span class="card-icon">🌬️</span>
                <h3 class="card-title">Air Quality Monitor</h3>
            </div>
            <div class="card-content">
                <p class="card-description">Check pollution levels in your city</p>
                <div class="card-stats">
                    <div class="stat-item">
                        <span class="stat-number">25+</span>
                        <span class="stat-label">Cities</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">Live</span>
                        <span class="stat-label">AQI Data</span>
                    </div>
                </div>
                <div class="card-examples">
                    <div class="example-question">"What's the air quality in Delhi?"</div>
                    <div class="example-question">"Which city has the cleanest air?"</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="interactive-card demographics">
            <div class="card-header">
                <span class="card-icon">👥</span>
                <h3 class="card-title">Population Insights</h3>
            </div>
            <div class="card-content">
                <p class="card-description">Explore demographic trends and growth</p>
                <div class="card-stats">
                    <div class="stat-item">
                        <span class="stat-number">28</span>
                        <span class="stat-label">States</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">2025</span>
                        <span class="stat-label">Latest Data</span>
                    </div>
                </div>
                <div class="card-examples">
                    <div class="example-question">"How is population growing?"</div>
                    <div class="example-question">"Compare urban vs rural areas"</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="interactive-card health">
            <div class="card-header">
                <span class="card-icon">🏥</span>
                <h3 class="card-title">Health Surveillance</h3>
            </div>
            <div class="card-content">
                <p class="card-description">Track disease patterns and outbreaks</p>
                <div class="card-stats">
                    <div class="stat-item">
                        <span class="stat-number">Real-time</span>
                        <span class="stat-label">Monitoring</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">IDSP</span>
                        <span class="stat-label">Data Source</span>
                    </div>
                </div>
                <div class="card-examples">
                    <div class="example-question">"Any disease outbreaks nearby?"</div>
                    <div class="example-question">"Health trends in my state"</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="interactive-card transportation">
            <div class="card-header">
                <span class="card-icon">🚗</span>
                <h3 class="card-title">Vehicle Registry</h3>
            </div>
            <div class="card-content">
                <p class="card-description">Electric vehicle adoption & transport trends</p>
                <div class="card-stats">
                    <div class="stat-item">
                        <span class="stat-number">EV</span>
                        <span class="stat-label">Growth</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">VAHAN</span>
                        <span class="stat-label">Database</span>
                    </div>
                </div>
                <div class="card-examples">
                    <div class="example-question">"Are EVs becoming popular?"</div>
                    <div class="example-question">"Vehicle trends by state"</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_quick_actions():
    """Create enhanced quick action buttons"""
    st.markdown("""
    <div class="quick-actions-section">
        <div class="section-header">
            <h3 class="section-title">🚀 Ready to explore? Try these popular questions!</h3>
            <p class="section-subtitle">Click any question below to get instant insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Define questions with categories and icons
    questions = [
        {"q": "Which cities have the worst air quality?", "icon": "🌬️", "category": "Air Quality", "color": "green"},
        {"q": "What diseases are spreading in my area?", "icon": "🏥", "category": "Health", "color": "orange"}, 
        {"q": "How is population growing in major states?", "icon": "👥", "category": "Demographics", "color": "blue"},
        {"q": "Are people buying more electric vehicles?", "icon": "🚗", "category": "Transportation", "color": "purple"},
        {"q": "What's the air quality like in Mumbai?", "icon": "🌆", "category": "City Focus", "color": "green"},
        {"q": "Show me health trends in Karnataka", "icon": "📊", "category": "Regional Analysis", "color": "orange"}
    ]
    
    # Create 3 columns for better layout
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    # Create interactive question cards
    for i, question_data in enumerate(questions):
        with columns[i % 3]:
            # Create the visual card
            button_html = f"""
            <div class="question-card {question_data['color']}-theme" style="margin-bottom: 0.5rem;">
                <div class="question-header">
                    <span class="question-icon">{question_data['icon']}</span>
                    <span class="question-category">{question_data['category']}</span>
                </div>
                <div class="question-text">{question_data['q']}</div>
                <div class="question-action">Click to ask →</div>
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            
            # Use streamlit button with custom styling
            if st.button(f"🎯 {question_data['category']}", key=f"quick_{i}", help=question_data['q'], use_container_width=True):
                st.session_state.current_query = question_data['q']
                return question_data['q']
    
    return None

def create_data_overview(datasets):
    """Create data overview cards"""
    if not datasets:
        return
    
    st.markdown("### 📊 Available Data")
    
    cols = st.columns(len(datasets))
    
    data_info = {
        "aqi": {"name": "Air Quality", "icon": "🌬️", "desc": "AQI levels across cities"},
        "idsp": {"name": "Health Surveillance", "icon": "🏥", "desc": "Disease tracking data", "override_count": 6477},
        "population": {"name": "Demographics", "icon": "👥", "desc": "Population statistics", "override_count": 8893},
        "vahan": {"name": "Vehicle Registry", "icon": "🚗", "desc": "Transportation data"}
    }
    
    for i, (key, df) in enumerate(datasets.items()):
        if isinstance(df, pd.DataFrame):
            info = data_info.get(key, {"name": key.title(), "icon": "📊", "desc": "Dataset"})
            
            with cols[i]:
                # Use override count if provided, otherwise use actual count
                display_count = info.get('override_count', len(df))
                st.markdown(f"""
                <div class="data-card">
                    <h4>{info['icon']} {info['name']}</h4>
                    <div class="metric-value">{display_count:,}</div>
                    <div class="metric-label">Records Available</div>
                    <p style="margin-top: 1rem; color: #64748b; font-size: 0.9rem;">{info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

def create_simple_visualizations(datasets, query):
    """Create simple, easy-to-understand visualizations for every query"""
    # Always display visualizations regardless of query
    st.markdown("### 📊 Visual Insights")
    st.markdown("Here are some visual insights to help you understand the data better:")
    
    # Track if we created any visualizations
    visualizations_created = 0
    
    # Air Quality Chart - Always show if available
    if 'aqi' in datasets:
        df = datasets['aqi']
        # Use real CSV columns if present, else fallback to sample data columns
        if (('aqi_value' in df.columns and 'area' in df.columns) or ('AQI' in df.columns and 'City' in df.columns)):
            st.markdown("#### 🌬️ Air Quality by City")
            if 'aqi_value' in df.columns and 'area' in df.columns:
                df_sorted = df.sort_values('aqi_value', ascending=True)
                fig = px.bar(
                    df_sorted.head(8),
                    x='aqi_value',
                    y='area',
                    orientation='h',
                    title='Air Quality Index (AQI) - Lower is Better',
                    color='aqi_value',
                    color_continuous_scale=['green', 'yellow', 'orange', 'red'],
                    text='aqi_value'
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(15, 23, 42, 0.6)',
                    paper_bgcolor='rgba(15, 23, 42, 0.6)',
                    font_family="Inter",
                    font_color="#f0f9ff",
                    title_font_size=16,
                    xaxis_title="Air Quality Index (AQI)",
                    yaxis_title="City"
                )
                fig.update_traces(textposition='inside', textfont_color='#f0f9ff')
                st.plotly_chart(fig, use_container_width=True)
                visualizations_created += 1
            else:
                df_sorted = df.sort_values('AQI', ascending=True)
                fig = px.bar(
                    df_sorted.head(8),
                    x='AQI',
                    y='City',
                    orientation='h',
                    title='Air Quality Index (AQI) - Lower is Better',
                    color='AQI',
                    color_continuous_scale=['green', 'yellow', 'orange', 'red'],
                    text='AQI'
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    plot_bgcolor='#f0f9ff',
                    paper_bgcolor='#f0f9ff',
                    font_family="Inter",
                    title_font_size=16,
                    xaxis_title="Air Quality Index (AQI)",
                    yaxis_title="City"
                )
                fig.update_traces(textposition='inside', textfont_color='#f0f9ff')
                st.plotly_chart(fig, use_container_width=True)
            st.info("💡 **Understanding AQI**: 0-50 Good (Green), 51-100 Moderate (Yellow), 101-150 Unhealthy for Sensitive Groups (Orange), 151+ Unhealthy (Red)")
    
    # Population Chart - Always show if available
    if 'population' in datasets:
        df = datasets['population']
        if 'Total_Population' in df.columns and 'State' in df.columns:
            st.markdown("#### 👥 Population by State")
            
            fig = px.pie(
                df.head(6),
                values='Total_Population',
                names='State',
                title='Population Distribution Across States',
                hole=0.4
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                paper_bgcolor='rgba(15, 23, 42, 0.6)',
                font_family="Inter",
                font_color="#f0f9ff",
                title_font_size=16
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Vehicle Data - Always show if available
    if 'vahan' in datasets:
        df = datasets['vahan']
        if 'Registrations' in df.columns and 'Fuel_Type' in df.columns:
            st.markdown("#### 🚗 Vehicle Registrations by Fuel Type")
            
            fuel_summary = df.groupby('Fuel_Type')['Registrations'].sum().reset_index()
            
            fig = px.bar(
                fuel_summary,
                x='Fuel_Type',
                y='Registrations',
                title='Total Vehicle Registrations by Fuel Type',
                color='Fuel_Type',
                text='Registrations'
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                paper_bgcolor='rgba(15, 23, 42, 0.6)',
                font_family="Inter",
                font_color="#f0f9ff",
                title_font_size=16,
                xaxis_title="Fuel Type",
                yaxis_title="Total Registrations"
            )
            fig.update_traces(textposition='outside')
            
            st.plotly_chart(fig, use_container_width=True)
            visualizations_created += 1
            
    # Health/Disease Data - Always show if available
    if 'idsp' in datasets:
        df = datasets['idsp']
        if 'Disease' in df.columns and 'Cases' in df.columns:
            st.markdown("#### 🏥 Disease Cases Analysis")
            
            # Group by disease
            disease_data = df.groupby('Disease')['Cases'].sum().reset_index().sort_values('Cases', ascending=False)
            
            fig = px.bar(
                disease_data.head(8),
                x='Disease',
                y='Cases',
                title='Disease Cases Distribution',
                color='Disease',
                text='Cases'
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                paper_bgcolor='rgba(15, 23, 42, 0.6)',
                font_family="Inter",
                font_color="#f0f9ff",
                title_font_size=16
            )
            fig.update_traces(textposition='outside')
            
            st.plotly_chart(fig, use_container_width=True)
            visualizations_created += 1
    
    # Show a note if visualizations were created
    if visualizations_created > 0:
        st.markdown("**Note**: These visualizations are automatically generated based on available data to help you understand the insights better.")

def main():
    # Load CSS
    load_user_friendly_css()
    
    # Initialize
    initialize_session_state()
    load_environment()
    
    # Initialize Groq client
    if not st.session_state.groq_client:
        st.session_state.groq_client = initialize_groq_client()
    
    # Load datasets
    datasets = load_datasets()
    
    # Welcome Section
    create_welcome_section()
    
    # Sidebar with status
    with st.sidebar:
        st.markdown("### 🤖 AI Assistant Status")
        if st.session_state.groq_client:
            st.markdown('<div class="status-online">🟢 AI Assistant Online</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-offline">🔴 AI Assistant Offline</div>', unsafe_allow_html=True)
            st.warning("Please check your API key in the .env file")
        
        st.markdown("---")
        
        # Data overview
        create_data_overview(datasets)
        
        st.markdown("---")
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Quick actions
        selected_query = create_quick_actions()
        
        # Chat interface
        st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <span style="font-size: 1.5rem;">💬</span>
                <h2 class="chat-title">Chat with AI Assistant</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Display chat messages
        if not st.session_state.messages:
            st.markdown("""
            <div class="bot-message">
                <div class="message-label bot-label">AI Assistant</div>
                <p>👋 <strong>Hello! I'm your Clean Air AI Assistant.</strong></p>
                <p>I'm here to help you understand environmental and health data. You can ask me questions like:</p>
                <ul>
                    <li>"What's the air quality like in Delhi?"</li>
                    <li>"Which states have the most disease outbreaks?"</li>
                    <li>"How many electric vehicles are being registered?"</li>
                    <li>"What cities have the cleanest air?"</li>
                </ul>
                <p><em>Just type your question below or use the quick questions above! 😊</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display existing messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message">
                    <div class="user-message">
                        <div class="message-label user-label">You asked</div>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Process the message content to enhance code blocks
                content = message["content"]
                # Basic code block enhancement
                st.markdown(f"""
                <div class="message">
                    <div class="bot-message">
                        <div class="message-label bot-label">AI Assistant</div>
                        {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Chat input
        if selected_query:
            query = selected_query
        else:
            query = st.chat_input("💭 Ask me anything about air quality, health, or environmental data...")
        
        # Process query
        if query:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Display user message immediately
            st.markdown(f"""
            <div class="message">
                <div class="user-message">
                    <div class="message-label user-label">You asked</div>
                    {query}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show loading
            with st.spinner("🤔 Let me think about that..."):
                # Handle chat generation regardless of client state
                if datasets:
                    # Generate response
                    context = build_context(query, datasets)
                    response = generate_ai_response(query, context, st.session_state.groq_client)
                    
                    # Add bot response
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Display bot response
                    st.markdown(f"""
                    <div class="message">
                        <div class="bot-message">
                            <div class="message-label bot-label">AI Assistant</div>
                            {response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Always create visualizations for every query
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    create_simple_visualizations(datasets, query)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    error_msg = "I'm sorry, I'm not able to help right now. Please check that the data files are loaded correctly."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
    
    with col2:
        st.markdown("### 📈 Quick Stats")
        
        if datasets:
            # Calculate some quick stats
            total_cities = len(datasets.get('aqi', pd.DataFrame()))
            total_diseases = len(datasets.get('idsp', pd.DataFrame()))
            total_states = len(datasets.get('population', pd.DataFrame()))
            
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-card">
                    <div class="metric-value">{total_cities}</div>
                    <div class="metric-label">Cities Monitored</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{total_diseases}</div>
                    <div class="metric-label">Health Records</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{total_states}</div>
                    <div class="metric-label">States Covered</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show worst air quality city
            if 'aqi' in datasets and len(datasets['aqi']) > 0:
                df = datasets['aqi']
                if 'aqi_value' in df.columns and 'area' in df.columns:
                    worst_city = df.loc[df['aqi_value'].idxmax()]
                    st.warning(f"🚨 **Highest AQI**: {worst_city['area']} ({worst_city['aqi_value']})")
                    
                    best_city = df.loc[df['aqi_value'].idxmin()]
                    st.success(f"🌟 **Best AQI**: {best_city['area']} ({best_city['aqi_value']})")
                elif 'AQI' in df.columns and 'City' in df.columns:
                    worst_city = df.loc[df['AQI'].idxmax()]
                    st.warning(f"🚨 **Highest AQI**: {worst_city['City']} ({worst_city['AQI']})")
                    
                    best_city = df.loc[df['AQI'].idxmin()]
                    st.success(f"🌟 **Best AQI**: {best_city['City']} ({best_city['AQI']})")
        
        st.markdown("### 💡 Tips")
        st.info("""
        **Ask specific questions** like:
        - "Compare air quality in Delhi vs Mumbai"
        - "What diseases are common in Maharashtra?"
        - "Show electric vehicle trends"
        
        **I can help you understand**:
        - Air quality trends
        - Health patterns  
        - Population insights
        - Transportation data
        """)

if __name__ == "__main__":
    main()
