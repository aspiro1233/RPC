# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io/)
3. **Groq API Key**: Get your API key from [console.groq.com](https://console.groq.com/)

## Step-by-Step Deployment

### 1. Prepare Your Repository

First, ensure your project is ready for deployment:

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit for Streamlit deployment"

# Create a new repository on GitHub and push
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

### 2. Environment Variables Setup

Create a `.env.example` file in your project root:

```bash
# Clean Air AI Chatbot Environment Variables
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
DEBUG=False
LOG_LEVEL=INFO
```

### 3. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io/)

2. **Sign in with GitHub**: Connect your GitHub account

3. **New App**: Click "New app"

4. **Configure App**:
   - **Repository**: Select your GitHub repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (optional)

5. **Advanced Settings**:
   - Click "Advanced settings"
   - Add your secrets in TOML format:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
GROQ_MODEL = "llama-3.1-70b-versatile"
DEBUG = false
LOG_LEVEL = "INFO"
```

6. **Deploy**: Click "Deploy!"

### 4. Post-Deployment

After deployment:

1. **Test Your App**: Visit your app URL and test all features
2. **Monitor Logs**: Check the logs in Streamlit Cloud dashboard
3. **Update Secrets**: If you need to change API keys, update them in the secrets section

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all packages in `requirements.txt` are compatible
   - Check for version conflicts

2. **API Key Issues**:
   - Verify your Groq API key is correct
   - Check if the key has sufficient credits
   - Ensure the key is properly set in Streamlit secrets

3. **Data Loading Issues**:
   - Verify all data files are in the `data/` directory
   - Check file permissions and formats

4. **Memory Issues**:
   - Large datasets might cause memory problems
   - Consider optimizing data loading with caching

### Performance Optimization

1. **Enable Caching**: Your app already uses `@st.cache_data` and `@st.cache_resource`
2. **Optimize Data Loading**: Load only necessary data
3. **Reduce API Calls**: Cache API responses where possible

## Security Best Practices

1. **Never commit API keys**: Always use environment variables
2. **Use Streamlit Secrets**: Store sensitive data in Streamlit Cloud secrets
3. **Validate Input**: Sanitize user inputs
4. **Rate Limiting**: Implement rate limiting for API calls

## Monitoring and Maintenance

1. **Regular Updates**: Keep dependencies updated
2. **Monitor Usage**: Track API usage and costs
3. **Backup Data**: Regularly backup your data files
4. **Performance Monitoring**: Monitor app performance and response times

## Support Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Guide](https://docs.streamlit.io/streamlit-community-cloud)
- [Groq API Documentation](https://console.groq.com/docs)
- [GitHub Issues](https://github.com/your-repo/issues)

## Quick Commands

```bash
# Local testing
streamlit run app.py

# Check requirements
pip list | grep -E "(streamlit|pandas|plotly|groq)"

# Update dependencies
pip install -r requirements.txt --upgrade

# Git workflow
git add .
git commit -m "Update for deployment"
git push origin main
```

---

**Your app will be live at**: `https://your-app-name.streamlit.app`

**Remember**: Always test locally before deploying! 