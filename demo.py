"""
Clean Air AI Chatbot - Demo Script
Demonstrates key features and functionality
"""

import streamlit as st
import time

def run_demo():
    """Run an interactive demo of the application"""
    
    st.markdown("""
    # 🚀 Welcome to Clean Air AI Chatbot Demo!
    
    This interactive demo will show you all the amazing features of our application.
    """)
    
    # Demo sections
    demo_sections = {
        "🌟 Key Features": show_features_demo,
        "💬 Chat Interface": show_chat_demo,
        "📊 Data Visualizations": show_visualization_demo,
        "🔍 Query Examples": show_query_examples,
        "⚡ Performance": show_performance_demo
    }
    
    # Create tabs for demo sections
    tabs = st.tabs(list(demo_sections.keys()))
    
    for i, (section_name, demo_function) in enumerate(demo_sections.items()):
        with tabs[i]:
            demo_function()

def show_features_demo():
    """Demonstrate key features"""
    st.markdown("""
    ## ✨ Amazing Features
    
    Our AI chatbot comes packed with powerful capabilities:
    """)
    
    features = [
        {
            "icon": "🌬️",
            "title": "Air Quality Analysis",
            "description": "Real-time AQI data analysis across major Indian cities with pollutant breakdowns and health recommendations."
        },
        {
            "icon": "🏥", 
            "title": "Health Insights",
            "description": "Disease outbreak tracking, epidemiological trends, and public health alerts from IDSP data."
        },
        {
            "icon": "👥",
            "title": "Demographics",
            "description": "Population projections, demographic analysis, and growth trend forecasting."
        },
        {
            "icon": "🚗",
            "title": "Vehicle Data",
            "description": "Transportation trends, fuel type adoption, and vehicle registration analytics."
        },
        {
            "icon": "🤖",
            "title": "AI-Powered",
            "description": "Powered by Groq's LLaMA 3.2 70B model for intelligent, context-aware responses."
        },
        {
            "icon": "📱",
            "title": "Responsive Design",
            "description": "Beautiful, mobile-first design with glassmorphism effects and smooth animations."
        }
    ]
    
    # Display features in a grid
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="padding: 1rem; margin: 0.5rem 0; background: rgba(15, 23, 42, 0.6); 
                        border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4>{feature['icon']} {feature['title']}</h4>
                <p style="color: #cbd5e1;">{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_chat_demo():
    """Demonstrate chat interface"""
    st.markdown("""
    ## 💬 Intelligent Chat Interface
    
    Our chat interface provides natural language interaction with your data:
    """)
    
    # Simulated chat conversation
    chat_examples = [
        {
            "role": "user",
            "content": "Which cities have the worst air quality in India?"
        },
        {
            "role": "assistant", 
            "content": """Based on the latest AQI data, here are the cities with the worst air quality:

**Top 5 Most Polluted Cities:**
1. **Kanpur, UP** - AQI: 167 (Severe)
2. **Lucknow, UP** - AQI: 159 (Severe) 
3. **Delhi** - AQI: 156 (Severe)
4. **Patna, Bihar** - AQI: 152 (Severe)
5. **Meerut, UP** - AQI: 151 (Severe)

**Key Insights:**
- Uttar Pradesh has 3 cities in the top 5
- Average PM2.5 levels are 2-3x higher than WHO guidelines
- Winter months show increased pollution due to crop burning

*Source: AQI Dataset (January 2025)*"""
        },
        {
            "role": "user",
            "content": "What diseases are spreading in Maharashtra?"
        },
        {
            "role": "assistant",
            "content": """Here's the current disease surveillance data for Maharashtra:

**Active Outbreaks:**
- **Dengue**: 234 cases in Mumbai (High severity)
- **Thane**: 138 cases with moderate spread

**Risk Assessment:**
- 🔴 High risk areas: Mumbai metropolitan region
- 🟡 Moderate risk: Pune, Nashik districts
- Population at risk: 12.5M+ people

**Recommendations:**
- Eliminate stagnant water sources
- Use mosquito repellents
- Seek medical attention for fever symptoms

*Source: IDSP Dataset (January 2025)*"""
        }
    ]
    
    # Display simulated chat
    for message in chat_examples:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                           padding: 1rem 1.5rem; border-radius: 20px 20px 8px 20px; max-width: 80%;">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1);
                           color: #f8fafc; padding: 1rem 1.5rem; border-radius: 20px 20px 20px 8px; 
                           max-width: 85%; backdrop-filter: blur(10px);">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_visualization_demo():
    """Demonstrate data visualizations"""
    st.markdown("""
    ## 📊 Beautiful Data Visualizations
    
    Our app automatically creates relevant charts and graphs based on your queries:
    """)
    
    # Sample visualization descriptions
    viz_types = [
        {
            "title": "📈 Air Quality Trends",
            "description": "Interactive bar charts showing AQI levels across cities with color coding for severity levels.",
            "features": ["Color-coded severity", "Hover details", "Responsive design"]
        },
        {
            "title": "🗺️ Geographic Disease Maps", 
            "description": "Heat maps showing disease outbreak patterns across states and districts.",
            "features": ["State-wise breakdown", "Severity indicators", "Population risk data"]
        },
        {
            "title": "📊 Population Demographics",
            "description": "Pie charts and treemaps for population distribution and growth patterns.",
            "features": ["Urban vs Rural", "Gender distribution", "Growth projections"]
        },
        {
            "title": "🚗 Vehicle Analytics",
            "description": "Scatter plots and trend lines for vehicle registration and fuel type adoption.",
            "features": ["Fuel type trends", "State comparisons", "Electric vehicle growth"]
        }
    ]
    
    for viz in viz_types:
        with st.expander(viz["title"]):
            st.write(viz["description"])
            st.write("**Key Features:**")
            for feature in viz["features"]:
                st.write(f"• {feature}")

def show_query_examples():
    """Show example queries users can try"""
    st.markdown("""
    ## 🔍 Try These Sample Queries
    
    Here are some example questions you can ask our AI assistant:
    """)
    
    query_categories = {
        "🌬️ Air Quality Queries": [
            "Which cities have the worst air quality?",
            "Show me PM2.5 levels across major cities",
            "How does Delhi's air quality compare to Mumbai?",
            "What are the main pollutants in Bangalore?",
            "Which states have the cleanest air?"
        ],
        "🏥 Health & Disease Queries": [
            "Show recent disease outbreaks in Maharashtra",
            "Which diseases are most common in India?",
            "What's the mortality rate for dengue outbreaks?",
            "Compare disease patterns across northern states",
            "Show me health risks in high-pollution areas"
        ],
        "👥 Population Queries": [
            "What's the population growth trend in southern India?",
            "Compare urban vs rural population by state",
            "Which states have the highest population density?",
            "Show me gender distribution across states",
            "What are the population projections for 2025?"
        ],
        "🚗 Vehicle & Transportation": [
            "Compare electric vehicle adoption across states",
            "Which fuel types are most popular?",
            "Show vehicle registration trends",
            "How many electric vehicles were registered?",
            "Compare transportation patterns between states"
        ]
    }
    
    for category, queries in query_categories.items():
        with st.expander(category):
            for query in queries:
                st.markdown(f"• *{query}*")

def show_performance_demo():
    """Demonstrate performance capabilities"""
    st.markdown("""
    ## ⚡ Performance & Capabilities
    
    Our application is built for speed and scalability:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Speed Metrics
        - **Response Time**: < 3 seconds average
        - **Data Loading**: Cached for instant access
        - **Chart Rendering**: Sub-second visualization
        - **API Calls**: Optimized for minimal latency
        """)
        
        # Mock performance metrics
        st.metric("Average Response Time", "2.1s", "-0.3s")
        st.metric("Queries Processed", "1,247", "+89")
        st.metric("Success Rate", "99.2%", "+0.1%")
    
    with col2:
        st.markdown("""
        ### 💾 Data Capabilities
        - **Dataset Size**: Handles millions of records
        - **Memory Usage**: Optimized caching
        - **Concurrent Users**: Multi-user support
        - **Real-time Updates**: Live data refresh
        """)
        
        # Mock data metrics
        st.metric("Records Processed", "2.1M", "+150K")
        st.metric("Cache Hit Rate", "94%", "+2%") 
        st.metric("Memory Usage", "145MB", "-12MB")
    
    st.markdown("""
    ### 🔧 Technical Features
    - **AI Model**: Groq LLaMA 3.2 70B Versatile
    - **Framework**: Streamlit with custom styling
    - **Visualizations**: Plotly & Altair integration
    - **Caching**: Intelligent data caching system
    - **Security**: API key encryption and validation
    """)

if __name__ == "__main__":
    run_demo()
