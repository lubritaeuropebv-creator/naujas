# Lithuanian Promo Cart Analyzer - Complete Project Structure

## 📁 File Organization

```
lt-promo-analyzer/
│
├── 📄 Core Application Files
│   ├── streamlit_app.py                    # Main Streamlit web application
│   └── lt_promo_analyzer_enhanced.py       # Backend analysis engine with PDF parsing
│
├── 📋 Configuration Files
│   ├── requirements_streamlit.txt          # Python dependencies for Streamlit
│   ├── packages.txt                        # System dependencies (Tesseract, Poppler)
│   ├── .streamlit/
│   │   └── config.toml                    # Streamlit configuration (theme, server)
│   └── .gitignore                         # Git ignore patterns
│
├── 📚 Documentation
│   ├── README_STREAMLIT.md                # Complete usage documentation
│   ├── DEPLOYMENT_GUIDE.md                # Step-by-step deployment instructions
│   ├── QUICKSTART.md                      # Quick start guide (this file)
│   └── PROJECT_STRUCTURE.md               # This file
│
├── 🗂️ Additional Files (from original package)
│   ├── requirements_enhanced.txt          # Full dependencies (includes web scraping)
│   ├── README_ENHANCED.md                 # Original CLI tool documentation
│   └── examples.py                        # Python usage examples
│
└── 📦 Optional Directories (created at runtime)
    ├── flyers/                           # Downloaded PDF flyers (gitignored)
    ├── analysis_results/                 # Exported analysis results (gitignored)
    └── tmp/                              # Temporary upload files (gitignored)
```

## 📄 File Descriptions

### Core Application Files

#### `streamlit_app.py` (Main Web App)
**Purpose**: Interactive web interface for the promo analyzer

**Key Features**:
- 5 main tabs: Overview, Best Deals, Price Comparison, Cart Optimizer, Export
- Demo data generator for testing
- PDF upload and parsing interface
- CSV data upload support
- Interactive Plotly visualizations
- Export to CSV and TXT

**Size**: ~25KB, 800+ lines
**Dependencies**: streamlit, plotly, pandas, numpy

**Usage**:
```bash
streamlit run streamlit_app.py
```

---

#### `lt_promo_analyzer_enhanced.py` (Backend Engine)
**Purpose**: Core analysis logic and PDF parsing

**Key Components**:
- `PromoFlyerScraper`: Web scraping and PDF parsing
- `LTPromoCartAnalyzer`: Data analysis and optimization

**Key Features**:
- Automatic flyer URL discovery
- PDF text extraction (pdfplumber, PyPDF2)
- OCR support for scanned PDFs (Tesseract)
- Lithuanian pattern recognition (prices, discounts)
- Product categorization
- Shopping cart optimization algorithms

**Size**: ~40KB, 1200+ lines
**Dependencies**: pandas, requests, PyPDF2, pdfplumber, pytesseract

---

### Configuration Files

#### `requirements_streamlit.txt`
**Purpose**: Python packages for Streamlit deployment

**Contents**:
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
requests>=2.31.0
beautifulsoup4>=4.12.0
PyPDF2>=3.0.0
pdfplumber>=0.10.0
pdf2image>=1.16.0
pytesseract>=0.3.10
Pillow>=10.0.0
```

**When to modify**: Add new Python dependencies

---

#### `packages.txt`
**Purpose**: System-level dependencies for Streamlit Cloud

**Contents**:
```
tesseract-ocr
tesseract-ocr-lit
tesseract-ocr-eng
poppler-utils
libpoppler-cpp-dev
```

**When to modify**: Add new system packages

---

#### `.streamlit/config.toml`
**Purpose**: Streamlit app configuration

**Key Settings**:
- Theme colors (primary, background, text)
- Server settings (upload size, CORS)
- Browser settings (stats collection)

**Customization**: Edit theme colors, upload limits

---

#### `.gitignore`
**Purpose**: Exclude files from Git repository

**Excludes**:
- Python cache files (`__pycache__`)
- Virtual environments (`venv/`)
- Data files (`.pdf`, `.csv`)
- IDE files (`.vscode/`, `.idea/`)
- Streamlit secrets

---

### Documentation Files

#### `README_STREAMLIT.md` (Main Documentation)
**Sections**:
1. Quick Start (local & cloud)
2. Features overview
3. Usage guide (demo, PDF, CSV)
4. CSV format examples
5. Supported retailers & categories
6. Troubleshooting
7. Customization options
8. Mobile support
9. Privacy & security
10. Future enhancements

**Audience**: End users, deployers

---

#### `DEPLOYMENT_GUIDE.md` (Deployment Manual)
**Sections**:
1. Pre-deployment checklist
2. Step-by-step Streamlit Cloud deployment
3. Configuration options
4. Troubleshooting deployment issues
5. Monitoring & analytics
6. Security best practices
7. Cost considerations
8. Post-deployment checklist

**Audience**: Developers, DevOps

---

#### `QUICKSTART.md` (Quick Reference)
**Sections**:
1. 3 ways to use (local, cloud, Docker)
2. First steps after launch
3. Sample use cases
4. Interface overview
5. Common issues & solutions
6. Pro tips
7. Verification checklist

**Audience**: New users

---

#### `PROJECT_STRUCTURE.md` (This File)
**Purpose**: Complete project documentation

**Sections**:
1. File organization
2. Detailed file descriptions
3. Deployment workflows
4. Development guide
5. Architecture overview

**Audience**: Developers, contributors

---

## 🚀 Deployment Workflows

### Workflow 1: Streamlit Cloud (Recommended)

```
1. Create GitHub Repository
   └─> Upload all files

2. Connect to Streamlit Cloud
   └─> share.streamlit.io

3. Configure Deployment
   ├─> Repository: your-repo
   ├─> Branch: main
   └─> Main file: streamlit_app.py

4. Deploy
   └─> Auto-builds on push

5. Share URL
   └─> your-app.streamlit.app
```

**Time**: 10 minutes
**Cost**: Free
**Best for**: Sharing, demos, MVPs

---

### Workflow 2: Local Development

```
1. Clone Repository
   └─> git clone your-repo

2. Install Dependencies
   ├─> pip install -r requirements_streamlit.txt
   └─> Install system packages (Tesseract, Poppler)

3. Run Application
   └─> streamlit run streamlit_app.py

4. Access Locally
   └─> http://localhost:8501
```

**Time**: 5 minutes
**Cost**: Free
**Best for**: Development, testing

---

### Workflow 3: Docker Deployment

```
1. Create Dockerfile
   └─> See example in QUICKSTART.md

2. Build Image
   └─> docker build -t lt-promo-analyzer .

3. Run Container
   └─> docker run -p 8501:8501 lt-promo-analyzer

4. Access Application
   └─> http://localhost:8501
```

**Time**: 15 minutes
**Cost**: Server costs
**Best for**: Production, self-hosting

---

## 🛠️ Development Guide

### Adding New Features

#### 1. Add New Tab to Streamlit App

**File**: `streamlit_app.py`

```python
# Add to tabs list
tab1, tab2, ..., tab_new = st.tabs([..., "New Tab"])

# Implement tab content
with tab_new:
    st.markdown("### New Feature")
    # Your code here
```

#### 2. Add New Analysis Method

**File**: `lt_promo_analyzer_enhanced.py`

```python
class LTPromoCartAnalyzer:
    def new_analysis_method(self, params):
        """
        New analysis method
        """
        # Your logic here
        return results
```

#### 3. Add New Visualization

**File**: `streamlit_app.py`

```python
import plotly.express as px

def create_new_chart(df):
    fig = px.bar(df, x='column', y='value', title='New Chart')
    return fig

# Use in tab
st.plotly_chart(create_new_chart(data))
```

#### 4. Add New Product Category

**File**: `lt_promo_analyzer_enhanced.py`

```python
self.category_keywords = {
    # Existing categories...
    'New Category': ['keyword1', 'keyword2', 'keyword3']
}
```

---

### Testing Workflow

```
1. Make Changes
   └─> Edit code locally

2. Test Locally
   └─> streamlit run streamlit_app.py

3. Verify Functionality
   ├─> Load demo data
   ├─> Test new feature
   └─> Check for errors

4. Commit Changes
   └─> git commit -m "Add feature X"

5. Push to GitHub
   └─> git push origin main

6. Verify Deployment
   └─> Check Streamlit Cloud auto-deploy
```

---

## 🏗️ Architecture Overview

### Data Flow

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Streamlit Frontend            │
│   (streamlit_app.py)            │
│                                 │
│   ├─ UI Components             │
│   ├─ User Interactions          │
│   └─ Visualizations (Plotly)    │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Backend Analyzer              │
│   (lt_promo_analyzer_enhanced.py)│
│                                 │
│   ├─ PromoFlyerScraper          │
│   │   ├─ Web Scraping           │
│   │   ├─ PDF Parsing            │
│   │   └─ OCR Processing         │
│   │                             │
│   └─ LTPromoCartAnalyzer        │
│       ├─ Data Analysis          │
│       ├─ Price Comparison       │
│       └─ Cart Optimization      │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Data Storage (Runtime)        │
│   ├─ Session State (Streamlit)  │
│   ├─ Pandas DataFrames          │
│   └─ Temporary Files            │
└─────────────────────────────────┘
```

### Component Dependencies

```
streamlit_app.py
    │
    ├─> lt_promo_analyzer_enhanced.py
    │       │
    │       ├─> pandas (data manipulation)
    │       ├─> numpy (numerical operations)
    │       ├─> requests (HTTP requests)
    │       ├─> beautifulsoup4 (HTML parsing)
    │       ├─> PyPDF2 (PDF text extraction)
    │       ├─> pdfplumber (PDF parsing)
    │       ├─> pytesseract (OCR)
    │       └─> Pillow (image processing)
    │
    ├─> plotly (interactive charts)
    └─> streamlit (web framework)
```

---

## 📊 Data Models

### Product Data Structure

```python
{
    'retailer': str,          # Store name (e.g., 'Maxima')
    'product_name': str,      # Product description
    'category': str,          # Product category
    'base_price': float,      # Original price in EUR
    'final_price': float,     # Discounted price in EUR
    'discount_pct': int,      # Discount percentage
    'is_promo': bool,         # Is on promotion
    'savings': float,         # Amount saved
    'source_file': str,       # Source PDF filename
    'parsed_date': datetime   # When parsed
}
```

### Cart Optimization Result

```python
{
    'cart': DataFrame,           # Products in cart
    'total_cost': float,         # Total price
    'total_savings': float,      # Total saved
    'items_count': int,          # Number of items
    'retailers': List[str]       # Stores to visit
}
```

---

## 🔧 Customization Points

### UI Customization

**Colors** (`.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#1f77b4"      # Change primary color
backgroundColor = "#ffffff"    # Change background
```

**Layout** (`streamlit_app.py`):
```python
st.set_page_config(
    layout="wide",             # "centered" or "wide"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

### Analysis Customization

**Price Patterns** (`lt_promo_analyzer_enhanced.py`):
```python
self.price_patterns = [
    r'(\d+)[,.](\d{2})\s*€',   # Add your pattern
]
```

**Categories** (`lt_promo_analyzer_enhanced.py`):
```python
self.category_keywords = {
    'Your Category': ['keyword1', 'keyword2']
}
```

---

## 📦 Packaging for Distribution

### For Streamlit Cloud
**Required files**:
- streamlit_app.py
- lt_promo_analyzer_enhanced.py
- requirements_streamlit.txt
- packages.txt
- .streamlit/config.toml

### For PyPI (Future)
```
setup.py
├─ name: lt-promo-analyzer
├─ version: 1.0.0
├─ packages: find_packages()
└─ entry_points: {'console_scripts': [...]}
```

### For Executable (PyInstaller)
```bash
pyinstaller --onefile \
    --add-data "lt_promo_analyzer_enhanced.py:." \
    streamlit_app.py
```

---

## 🔐 Security Considerations

1. **Input Validation**
   - File size limits (200MB)
   - File type validation
   - SQL injection prevention (not applicable)

2. **Secrets Management**
   - Use Streamlit secrets for API keys
   - Never commit secrets to Git

3. **Data Privacy**
   - No permanent storage
   - Temp files deleted after use
   - No user tracking (configurable)

---

## 🚀 Performance Optimization

1. **Caching** (Streamlit):
```python
@st.cache_data
def expensive_operation(data):
    # Results cached
    return processed_data
```

2. **Data Optimization**:
   - Limit demo data size
   - Use efficient pandas operations
   - Paginate large tables

3. **Resource Management**:
   - Delete temp files
   - Clear unused DataFrames
   - Optimize PDF parsing

---

## 📈 Monitoring & Analytics

### Built-in Streamlit Metrics
- Active users
- Session duration
- Error rates
- Resource usage

### Custom Logging
```python
import logging
logging.info(f"User action: {action}")
```

### Analytics Integration (Optional)
- Google Analytics
- Mixpanel
- Custom event tracking

---

## 🔄 Version Control

### Git Workflow
```
main (production)
  │
  ├─ develop (staging)
  │    │
  │    ├─ feature/new-chart
  │    ├─ feature/better-parsing
  │    └─ bugfix/pdf-upload
  │
  └─ hotfix/critical-bug
```

### Release Process
1. Develop in feature branch
2. Merge to develop
3. Test on staging
4. Merge to main
5. Auto-deploy to production

---

## 📝 Contributing Guidelines

1. Fork repository
2. Create feature branch
3. Make changes
4. Write tests (if applicable)
5. Update documentation
6. Submit pull request

---

## 🆘 Support & Resources

- **Documentation**: All .md files
- **Code**: Inline comments
- **Streamlit Docs**: https://docs.streamlit.io
- **Community**: https://discuss.streamlit.io
- **Issues**: GitHub Issues

---

**Last Updated**: 2024
**Version**: 1.0.0
**Maintainer**: Project Team
