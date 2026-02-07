# Lithuanian Promo Cart Analyzer - Streamlit Web Application

## 🌐 Live Demo

Deploy this application to Streamlit Cloud for free!

## 📋 Quick Start

### Local Deployment

1. **Install dependencies:**
```bash
pip install -r requirements_streamlit.txt
```

2. **Install system dependencies (for PDF parsing):**

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-lit tesseract-ocr-eng poppler-utils
```

**macOS:**
```bash
brew install tesseract tesseract-lang poppler
```

**Windows:**
- Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases/

3. **Run the app:**
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Deploy with these settings:**
   - Repository: `your-username/your-repo-name`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Wait for deployment** (usually 2-3 minutes)

5. **Your app is live!** Share the URL with others

## 📁 Required Files for Streamlit Cloud

Make sure your repository contains:

```
your-repo/
│
├── streamlit_app.py              # Main Streamlit application
├── lt_promo_analyzer_enhanced.py # Backend analyzer
├── requirements_streamlit.txt     # Python dependencies
├── packages.txt                   # System dependencies
├── .streamlit/
│   └── config.toml               # Streamlit configuration
└── README_STREAMLIT.md           # This file
```

## 🎯 Features

### 📊 Overview Dashboard
- Real-time statistics and metrics
- Interactive charts and visualizations
- Retailer comparison analysis
- Category breakdown

### 🏆 Best Deals Finder
- Top promotional offers across all retailers
- Filter by category
- Sort by discount percentage or savings amount
- Visual deal cards

### 🔍 Price Comparison
- Search for specific products
- Compare prices across retailers
- Interactive price comparison charts
- Identify best deals

### 🛒 Cart Optimization
- Define your shopping needs
- Set budget constraints
- Choose optimization strategy:
  - **Maximum Savings**: Prioritize highest discounts
  - **Variety**: Maximize product variety
  - **Single Store**: Minimize shopping trips
- Get optimized shopping cart

### 📥 Data Export
- Export to CSV for further analysis
- Generate text reports
- Download best deals lists

## 💡 Usage Guide

### Option 1: Demo Data (Recommended for First Use)

1. Click **"Įkelti demo duomenis"** in the sidebar
2. Explore all features with sample data
3. Get familiar with the interface

### Option 2: Upload PDF Flyer

1. Select **"Įkelti PDF"** in the sidebar
2. Choose retailer from dropdown
3. Upload promotional PDF flyer
4. Enable OCR if needed (for scanned PDFs)
5. Click **"Analizuoti PDF"**
6. Wait for processing (may take 30-60 seconds)

### Option 3: Upload CSV Data

1. Select **"Įkelti CSV"** in the sidebar
2. Upload CSV file with columns:
   - `retailer`: Store name
   - `product_name`: Product name
   - `category`: Product category
   - `base_price`: Original price
   - `final_price`: Discounted price
   - `discount_pct`: Discount percentage (optional)
3. Click **"Įkelti CSV"**

## 📊 CSV Format Example

```csv
retailer,product_name,category,base_price,final_price,discount_pct
Maxima,Pienas 2.5% 1L,Pieno produktai,1.39,0.99,29
Rimi,Duona juoda 500g,Duona ir konditerija,1.25,0.89,29
IKI,Vištienos filė 1kg,Mėsa ir mėsos gaminiai,5.99,3.99,33
```

## 🏪 Supported Retailers

- **Maxima** - Lithuania's largest supermarket chain
- **Rimi** - Baltic supermarket chain
- **IKI** - Lithuanian supermarket chain
- **Lidl** - International discount chain
- **Norfa** - Regional supermarket chain
- **Barbora** - Online grocery platform

## 📂 Supported Categories

- **Pieno produktai** (Dairy products)
- **Mėsa ir mėsos gaminiai** (Meat and meat products)
- **Duona ir konditerija** (Bread and bakery)
- **Vaisiai ir daržovės** (Fruits and vegetables)
- **Gėrimai** (Beverages)
- **Konservai** (Canned goods)
- **Užšaldyti produktai** (Frozen products)
- **Sausainiai ir saldumynai** (Cookies and sweets)
- **Makaronai ir kruopos** (Pasta and grains)
- **Kosmetika ir higiena** (Cosmetics and hygiene)

## 🔧 Troubleshooting

### PDF Upload Not Working

**Issue**: PDF processing fails or returns no results

**Solutions**:
1. Enable OCR checkbox for scanned PDFs
2. Check PDF quality (prefer high-resolution scans)
3. Try converting PDF to images first
4. Use CSV upload as alternative

### Slow Performance

**Issue**: App is slow to respond

**Solutions**:
1. Use demo data for testing (much faster)
2. Reduce number of products in uploaded data
3. Clear browser cache
4. Refresh the page

### Charts Not Displaying

**Issue**: Visualizations don't show

**Solutions**:
1. Check that data is loaded (sidebar status)
2. Try different browser (Chrome recommended)
3. Disable ad blockers
4. Check browser console for errors

### Deployment Errors on Streamlit Cloud

**Issue**: App fails to deploy

**Solutions**:
1. Verify all required files are in repository
2. Check `requirements_streamlit.txt` for syntax errors
3. Ensure `packages.txt` exists for system dependencies
4. Check Streamlit Cloud logs for specific errors
5. Reduce dependencies if deployment timeout occurs

## 🎨 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#your_color_here"
backgroundColor = "#your_color_here"
```

### Modify Upload Limits

Edit `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 200  # Size in MB
```

### Add Custom Categories

Edit `streamlit_app.py` in the `load_demo_data()` function to add your categories.

## 📱 Mobile Support

The app is responsive and works on mobile devices, but for best experience use:
- Tablet or larger screen
- Latest browser version
- Landscape orientation for charts

## 🔒 Privacy & Security

- All data processing happens on the server
- Uploaded files are temporary and deleted after processing
- No data is stored permanently
- No user tracking or analytics (when `gatherUsageStats = false`)

## 🚀 Performance Tips

1. **Use Demo Data First**: Test all features with demo data before uploading
2. **CSV is Faster**: CSV upload is much faster than PDF parsing
3. **Limit PDF Pages**: Extract only promotional pages before uploading
4. **Cache Results**: Download CSV after parsing to avoid re-processing
5. **Batch Processing**: Upload multiple flyers as separate files

## 📈 Future Enhancements

- [ ] Multi-language support (English, Polish, Latvian)
- [ ] Historical price tracking
- [ ] Weekly meal planning integration
- [ ] Barcode scanning from images
- [ ] Price alert notifications
- [ ] Recipe suggestions based on deals
- [ ] Nutrition information display

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit pull request with description

## 📄 License

This application is provided as-is for personal use.

## 🆘 Support

For issues or questions:
1. Check this README
2. Review troubleshooting section
3. Check Streamlit documentation: https://docs.streamlit.io
4. Submit GitHub issue with details

## 🎯 Use Cases

### For Shoppers
- Find weekly best deals
- Plan grocery shopping within budget
- Compare prices across stores
- Maximize savings

### For Analysts
- Market research on pricing strategies
- Competitive analysis
- Promotional effectiveness tracking
- Consumer behavior insights

### For Developers
- Learn Streamlit development
- PDF parsing techniques
- Data visualization with Plotly
- Web scraping methods

## ⚡ Pro Tips

1. **Download Reports**: Export CSV for Excel analysis
2. **Compare Weekly**: Track price changes over time
3. **Plan Routes**: Use single-store optimization to minimize trips
4. **Share Finds**: Export best deals to share with family
5. **Budget Tracking**: Use cart optimization to stay within budget

## 🌟 Demo Scenarios

Try these with demo data:

1. **Best Dairy Deals**: 
   - Go to "Geriausi pasiūlymai"
   - Filter: "Pieno produktai"
   - Find top 10 deals

2. **50€ Shopping Cart**:
   - Go to "Krepšelio optimizavimas"
   - Set budget: 50€
   - Add categories: Pieno (3), Mėsa (2), Duona (2)
   - Optimize: "Maksimalūs sutaupymai"

3. **Price Comparison**:
   - Go to "Kainų palyginimas"
   - Search: "pienas"
   - Compare across retailers

## 📞 Contact

For business inquiries or custom development:
- GitHub Issues: [Create an issue]
- Email: [Your email if you want to add]

---

**Made with ❤️ for Lithuanian shoppers**

**Powered by Streamlit 🎈**
