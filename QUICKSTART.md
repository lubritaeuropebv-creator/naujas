# 🚀 Quick Start Guide - Lithuanian Promo Cart Analyzer

## 📦 What You Get

This package contains a complete web application for analyzing promotional flyers from Lithuanian food retailers.

### Files Included:

1. **streamlit_app.py** - Main web application
2. **lt_promo_analyzer_enhanced.py** - Backend analysis engine
3. **requirements_streamlit.txt** - Python dependencies
4. **packages.txt** - System dependencies (for Streamlit Cloud)
5. **.streamlit/config.toml** - App configuration
6. **README_STREAMLIT.md** - Full documentation
7. **DEPLOYMENT_GUIDE.md** - Step-by-step deployment guide

## ⚡ 3 Ways to Use

### Option 1: Run Locally (5 minutes)

**Perfect for testing and development**

```bash
# 1. Install dependencies
pip install -r requirements_streamlit.txt

# 2. Run the app
streamlit run streamlit_app.py

# 3. Open browser at http://localhost:8501
```

### Option 2: Deploy to Streamlit Cloud (10 minutes)

**Perfect for sharing with others - FREE!**

1. Create GitHub repository
2. Upload all files
3. Go to https://share.streamlit.io
4. Click "New app"
5. Select your repository
6. Deploy!

**Detailed steps**: See `DEPLOYMENT_GUIDE.md`

### Option 3: Docker (Advanced)

**Perfect for production deployment**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

## 🎯 First Steps After Launch

### 1. Load Demo Data (Recommended)

- Click sidebar: **"Įkelti demo duomenis"**
- Explore 150 sample products
- Test all features without uploading files

### 2. Try All Tabs

- **📊 Apžvalga** - Overview & statistics
- **🏆 Geriausi pasiūlymai** - Best deals finder
- **🔍 Kainų palyginimas** - Price comparison
- **🛒 Krepšelio optimizavimas** - Cart optimizer
- **📥 Eksportas** - Export data

### 3. Upload Your Data

**Option A: PDF Flyer**
1. Select "Įkelti PDF"
2. Choose retailer
3. Upload PDF file
4. Click "Analizuoti PDF"

**Option B: CSV File**
1. Select "Įkelti CSV"
2. Upload CSV with columns: retailer, product_name, category, base_price, final_price
3. Click "Įkelti CSV"

## 📊 Sample Use Cases

### Use Case 1: Find Weekly Best Deals

```
1. Load demo data or upload flyers
2. Go to "Geriausi pasiūlymai" tab
3. Select category (e.g., "Pieno produktai")
4. View top 20 deals
5. Export to CSV
```

### Use Case 2: Compare Milk Prices

```
1. Load data
2. Go to "Kainų palyginimas" tab
3. Search: "pienas"
4. View price comparison chart
5. Identify cheapest option
```

### Use Case 3: Plan 50€ Shopping Trip

```
1. Load data
2. Go to "Krepšelio optimizavimas" tab
3. Set budget: 50€
4. Select categories & quantities
5. Choose strategy: "Maksimalūs sutaupymai"
6. Get optimized cart
7. Export shopping list
```

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────┐
│  🛒 Lietuvos Prekybos Nuolaidų Analizatorius   │
├─────────────┬───────────────────────────────────┤
│             │                                   │
│  SIDEBAR    │     MAIN CONTENT AREA            │
│             │                                   │
│  📁 Data    │  📊 Tabs:                        │
│  Source     │  - Apžvalga (Overview)           │
│             │  - Geriausi pasiūlymai (Deals)   │
│  - Demo     │  - Kainų palyginimas (Compare)   │
│  - PDF      │  - Krepšelis (Cart)              │
│  - CSV      │  - Eksportas (Export)            │
│             │                                   │
│  ℹ️ About   │  [Charts, tables, controls]      │
│             │                                   │
└─────────────┴───────────────────────────────────┘
```

## 🐛 Common Issues & Solutions

### Issue: "Analyzer not available"
**Solution**: Ensure `lt_promo_analyzer_enhanced.py` is in same directory

### Issue: PDF parsing fails
**Solutions**:
- Enable "Naudoti OCR" checkbox
- Check PDF file size (<200MB)
- Try CSV upload instead

### Issue: Charts not showing
**Solutions**:
- Ensure data is loaded (check sidebar)
- Refresh browser
- Try Chrome/Firefox

### Issue: Slow performance
**Solutions**:
- Use demo data for testing
- Reduce uploaded file size
- Close other tabs

## 💡 Pro Tips

1. **Start with demo data** to learn the interface
2. **Export CSV** after parsing PDF to avoid re-processing
3. **Use filters** to narrow down large datasets
4. **Try different optimization strategies** for your cart
5. **Download reports** for offline analysis
6. **Share the link** if deployed to Streamlit Cloud

## 📱 Device Compatibility

- ✅ **Desktop**: Full features, best experience
- ✅ **Tablet**: Good, use landscape mode
- ⚠️ **Mobile**: Limited, charts may be hard to read

**Recommended**: Desktop with screen ≥1280px wide

## 🔐 Privacy & Data

- All processing happens on the server
- Uploaded files are temporary
- No data stored permanently
- No tracking (when configured)

## 📚 Learn More

- **Full Documentation**: `README_STREAMLIT.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **Streamlit Docs**: https://docs.streamlit.io
- **Python Code**: `streamlit_app.py` (commented)

## 🆘 Need Help?

1. Check `README_STREAMLIT.md` troubleshooting section
2. Review `DEPLOYMENT_GUIDE.md` for deployment issues
3. Check Streamlit forum: https://discuss.streamlit.io
4. Create GitHub issue with error details

## ✅ Verification Checklist

Before deploying:

- [ ] All files present
- [ ] Tested locally
- [ ] Demo data works
- [ ] All tabs accessible
- [ ] Charts display correctly
- [ ] Export functions work
- [ ] No errors in console

## 🎯 Next Steps

### For Local Development:
1. Run `streamlit run streamlit_app.py`
2. Test with demo data
3. Customize as needed
4. Deploy when ready

### For Streamlit Cloud:
1. Create GitHub repo
2. Upload all files
3. Follow `DEPLOYMENT_GUIDE.md`
4. Share your app!

### For Custom Deployment:
1. Review Docker option
2. Configure production settings
3. Set up SSL/domain
4. Deploy to your server

## 🌟 Features Highlight

### Interactive Visualizations
- Plotly charts (zoom, pan, hover)
- Real-time filtering
- Responsive design

### Smart Analysis
- Auto-categorization
- Deal scoring algorithm
- Multi-strategy optimization

### User-Friendly
- Lithuanian interface
- Intuitive navigation
- Clear metrics
- Export options

## 📞 Support

For questions or issues:
- **Technical**: Check documentation files
- **Bugs**: Create GitHub issue
- **Features**: Submit feature request
- **General**: Streamlit community forum

---

## 🎉 Ready to Start!

Choose your path:
1. **Quick Test**: Run locally with demo data
2. **Full Deploy**: Upload to Streamlit Cloud
3. **Production**: Docker deployment

**Time to get started: 5-10 minutes**

---

**Made with ❤️ for Lithuanian shoppers**

**Powered by Streamlit 🎈 & Python 🐍**
