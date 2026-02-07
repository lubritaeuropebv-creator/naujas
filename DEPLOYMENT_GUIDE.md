# Streamlit Cloud Deployment Guide
## Lithuanian Promo Cart Analyzer

### 📋 Pre-Deployment Checklist

Before deploying to Streamlit Cloud, ensure you have:

- [x] GitHub account
- [x] Streamlit Cloud account (free at share.streamlit.io)
- [x] All required files in your repository
- [x] Files tested locally

### 📁 Required Files

Your GitHub repository must contain:

```
repository-root/
│
├── streamlit_app.py                  # ✅ Main application
├── lt_promo_analyzer_enhanced.py     # ✅ Backend logic
├── requirements_streamlit.txt         # ✅ Python dependencies
├── packages.txt                       # ✅ System dependencies
├── .streamlit/
│   └── config.toml                   # ✅ App configuration
├── .gitignore                        # ✅ Git ignore rules
└── README_STREAMLIT.md               # ✅ Documentation
```

### 🚀 Step-by-Step Deployment

#### Step 1: Prepare Your Repository

1. **Create a new GitHub repository** or use existing one

2. **Upload all files** listed above to your repository

3. **Verify file structure** matches the layout above

4. **Commit and push** all changes:
```bash
git add .
git commit -m "Initial Streamlit app deployment"
git push origin main
```

#### Step 2: Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account

3. **Click** "New app" button

4. **Configure deployment:**
   - **Repository**: Select your repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose a custom URL (optional)

5. **Click** "Deploy!"

6. **Wait** for deployment (usually 2-5 minutes)
   - You'll see build logs
   - Green checkmark means success

7. **Access your app** at the provided URL

#### Step 3: Test Your Deployed App

1. **Open the app URL** in your browser

2. **Test basic functionality:**
   - Click "Įkelti demo duomenis"
   - Navigate through all tabs
   - Try filtering and searching
   - Test data export

3. **Test PDF upload** (if needed):
   - Upload a sample PDF
   - Verify parsing works
   - Check results display

### ⚙️ Configuration Options

#### Custom Domain (Optional)

To use a custom domain:

1. Go to app settings in Streamlit Cloud
2. Add custom domain under "Sharing"
3. Update DNS settings per instructions

#### Secrets Management

For API keys or sensitive data:

1. Go to app settings
2. Click "Secrets"
3. Add secrets in TOML format:
```toml
[api_keys]
example_key = "your_secret_key"
```

4. Access in code:
```python
import streamlit as st
api_key = st.secrets["api_keys"]["example_key"]
```

#### Resource Limits

Free tier limits:
- **RAM**: 1 GB
- **CPU**: 0.5 cores (shared)
- **Concurrent users**: Limited by resources
- **Apps**: Unlimited public apps

For higher limits, consider Streamlit Cloud Teams or Community Cloud.

### 🐛 Troubleshooting

#### Build Fails

**Error**: "ModuleNotFoundError"
```
Solution: Add missing package to requirements_streamlit.txt
```

**Error**: "System package not found"
```
Solution: Add package to packages.txt
```

**Error**: "Memory limit exceeded"
```
Solution: Reduce data size or optimize code
```

#### Runtime Issues

**Error**: "App is too slow"
```
Solutions:
- Use st.cache_data for expensive operations
- Reduce demo data size
- Optimize pandas operations
```

**Error**: "PDF parsing fails"
```
Solutions:
- Verify packages.txt includes tesseract
- Check PDF file size (<200MB)
- Enable OCR checkbox
- Try with different PDF
```

**Error**: "Charts not displaying"
```
Solutions:
- Check Plotly version in requirements
- Verify data format
- Clear browser cache
```

### 🔄 Updating Your App

1. **Make changes** to your code locally

2. **Test locally**:
```bash
streamlit run streamlit_app.py
```

3. **Commit and push**:
```bash
git add .
git commit -m "Update feature X"
git push origin main
```

4. **Streamlit Cloud auto-deploys** on push to main branch

5. **Watch build logs** in Streamlit Cloud dashboard

### 📊 Monitoring

#### View Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "Logs" tab
4. View real-time application logs

#### Analytics

Check app metrics:
- Total visitors
- Active sessions
- Resource usage
- Error rates

### 🔒 Security Best Practices

1. **Don't commit secrets** to repository
   - Use Streamlit secrets for sensitive data
   - Add to .gitignore

2. **Validate uploads**
   - Check file types
   - Limit file sizes
   - Sanitize inputs

3. **Enable XSRF protection**
   - Already enabled in config.toml

4. **Keep dependencies updated**
   - Regularly update requirements
   - Monitor for security advisories

### 💰 Cost Considerations

**Free Tier**:
- ✅ Unlimited public apps
- ✅ Community support
- ❌ Limited resources
- ❌ Apps sleep after inactivity

**Paid Tiers**:
- More resources (RAM/CPU)
- Private apps
- Custom authentication
- Priority support
- No sleep mode

### 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Deployment Guide**: https://docs.streamlit.io/streamlit-community-cloud
- **Forum**: https://discuss.streamlit.io
- **GitHub**: https://github.com/streamlit/streamlit

### ✅ Post-Deployment Checklist

After successful deployment:

- [ ] App loads without errors
- [ ] All tabs are accessible
- [ ] Demo data works
- [ ] PDF upload works (if configured)
- [ ] CSV upload works
- [ ] Charts display correctly
- [ ] Export functions work
- [ ] Mobile view is acceptable
- [ ] URL is shareable
- [ ] Documentation is updated

### 🎉 You're Live!

Share your app:
- Copy the app URL
- Share on social media
- Add to your portfolio
- Include in documentation

### 📝 Example Repository Structure

```
your-repo/
│
├── .streamlit/
│   └── config.toml
│
├── .gitignore
├── streamlit_app.py
├── lt_promo_analyzer_enhanced.py
├── requirements_streamlit.txt
├── packages.txt
├── README.md
├── README_STREAMLIT.md
└── DEPLOYMENT_GUIDE.md (this file)
```

### 🆘 Getting Help

If you encounter issues:

1. **Check logs** in Streamlit Cloud dashboard
2. **Review documentation** above
3. **Search Streamlit forum**: discuss.streamlit.io
4. **Create GitHub issue** with:
   - Error message
   - Build logs
   - Steps to reproduce
   - Expected vs actual behavior

### 🚀 Next Steps

After deployment:

1. **Gather feedback** from users
2. **Monitor usage** patterns
3. **Optimize performance** based on analytics
4. **Add new features** based on requests
5. **Keep dependencies updated**
6. **Document changes** in changelog

---

**Happy Deploying! 🎈**

Questions? Issues? Check the Streamlit Community Forum!
