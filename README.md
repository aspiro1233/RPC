# 🌬️ Clean Air AI Chatbot

An AI-powered chatbot that provides insights on air quality, health data, and environmental trends using the Groq API.

## 🚀 Live Demo

[Deploy to Streamlit Cloud](https://share.streamlit.io/)

## 📋 Features

- **AI-Powered Insights**: Uses Groq's LLM for intelligent responses
- **Data Visualization**: Interactive charts and graphs
- **Multi-Dataset Analysis**: Air quality, health, population, and vehicle data
- **Real-time Processing**: Dynamic query classification and response generation
- **Beautiful UI**: Modern, responsive design with enterprise-grade styling

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: Groq API (LLaMA 3.1 70B)
- **Data Processing**: Pandas
- **Visualization**: Plotly, Altair
- **Styling**: Custom CSS with Google Fonts

## 📊 Data Sources

- Air Quality Index (AQI) data
- Integrated Disease Surveillance Programme (IDSP) data
- Population projection data
- Vehicle registration data

## 🔧 Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Connect your GitHub repository
   - Set environment variables in the Streamlit Cloud dashboard
   - Deploy!

## 🔑 Environment Variables

Set these in Streamlit Cloud's secrets management:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── app_friendly.py        # Alternative UI version
├── launch.py             # Smart launcher script
├── requirements.txt      # Python dependencies
├── .streamlit/           # Streamlit configuration
│   └── config.toml
├── data/                 # Data files
│   ├── aqi.csv
│   ├── idsp.csv
│   ├── population_projection.csv
│   └── vahan.csv
└── README.md
```

## 🎯 Usage

1. **Ask Questions**: Type natural language queries about air quality, health trends, or environmental data
2. **View Visualizations**: Interactive charts are automatically generated based on your queries
3. **Explore Data**: Browse through different datasets and insights
4. **Get AI Insights**: Receive intelligent analysis and recommendations

## 🔒 Security

- API keys are stored securely in environment variables
- No sensitive data is exposed in the frontend
- CORS protection enabled for production

## 📈 Performance

- Cached data loading for faster response times
- Optimized queries for large datasets
- Efficient memory usage with Streamlit caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Review the [Groq API documentation](https://console.groq.com/docs)
- Open an issue in this repository

---

**Made with ❤️ for environmental awareness and public health** 