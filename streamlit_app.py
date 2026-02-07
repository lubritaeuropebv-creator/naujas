"""
Lithuanian Food Retailers Promo Cart Analyzer - Streamlit App
==============================================================
Web-based application for analyzing promotional flyers and optimizing shopping
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import base64
from pathlib import Path

# Import plotly (optional - will fall back to matplotlib if not available)
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Install with: pip install plotly")
    # Fallback to matplotlib
    try:
        import matplotlib.pyplot as plt
        MATPLOTLIB_AVAILABLE = True
    except ImportError:
        MATPLOTLIB_AVAILABLE = False

# Import our analyzer (will be in the same directory)
try:
    from lt_promo_analyzer_enhanced import LTPromoCartAnalyzer, PromoFlyerScraper
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    st.error("⚠️ Backend analyzer not available. Make sure lt_promo_analyzer_enhanced.py is in the same directory.")

# Page configuration
st.set_page_config(
    page_title="LT Promo Analyzer",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .deal-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2ecc71;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = LTPromoCartAnalyzer() if ANALYZER_AVAILABLE else None
if 'products_loaded' not in st.session_state:
    st.session_state.products_loaded = False
if 'demo_data' not in st.session_state:
    st.session_state.demo_data = None


def load_demo_data():
    """Load demo data for testing"""
    np.random.seed(42)
    demo_data = []
    retailers = ['Maxima', 'Rimi', 'IKI', 'Lidl', 'Norfa']
    categories = ['Pieno produktai', 'Mėsa ir mėsos gaminiai', 'Duona ir konditerija',
                  'Vaisiai ir daržovės', 'Gėrimai', 'Konservai', 'Užšaldyti produktai',
                  'Sausainiai ir saldumynai', 'Makaronai ir kruopos']
    
    product_examples = {
        'Pieno produktai': ['Pienas 2.5%', 'Jogurtas', 'Grietinė', 'Varškė', 'Sūris'],
        'Mėsa ir mėsos gaminiai': ['Kiauliena', 'Vištiena', 'Dešra', 'Kumpis'],
        'Duona ir konditerija': ['Duona juoda', 'Batonas', 'Bandelės', 'Pyragas'],
        'Vaisiai ir daržovės': ['Obuoliai', 'Bananai', 'Pomidorai', 'Agurkai'],
        'Gėrimai': ['Sultys', 'Vanduo', 'Arbata', 'Kava'],
        'Konservai': ['Konservuoti agurkai', 'Pomidorų padažas', 'Žuvis'],
        'Užšaldyti produktai': ['Ledai', 'Pizza', 'Daržovės'],
        'Sausainiai ir saldumynai': ['Sausainiai', 'Šokoladas', 'Saldainiai'],
        'Makaronai ir kruopos': ['Makaronai', 'Ryžiai', 'Grikiai'],
    }
    
    for i in range(150):
        retailer = np.random.choice(retailers)
        category = np.random.choice(categories)
        product_base = np.random.choice(product_examples.get(category, ['Produktas']))
        base_price = np.random.uniform(0.5, 20.0)
        discount = np.random.choice([10, 15, 20, 25, 30, 40, 50])
        
        demo_data.append({
            'retailer': retailer,
            'product_name': f'{product_base} {np.random.randint(100, 999)}g',
            'category': category,
            'base_price': round(base_price, 2),
            'final_price': round(base_price * (1 - discount/100), 2),
            'discount_pct': discount,
            'is_promo': True,
            'source_file': 'demo_data',
            'parsed_date': datetime.now()
        })
    
    df = pd.DataFrame(demo_data)
    df['savings'] = df['base_price'] - df['final_price']
    return df


def create_summary_metrics(df):
    """Create summary metrics display"""
    total_products = len(df)
    avg_discount = df[df['is_promo']]['discount_pct'].mean()
    total_savings = df['savings'].sum()
    num_retailers = df['retailer'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Produktų", f"{total_products:,}")
    with col2:
        st.metric("Vidut. nuolaida", f"{avg_discount:.1f}%")
    with col3:
        st.metric("Galimi sutaupymai", f"{total_savings:.2f} €")
    with col4:
        st.metric("Parduotuvių", num_retailers)


def create_retailer_comparison_chart(df):
    """Create retailer comparison chart"""
    retailer_stats = df.groupby('retailer').agg({
        'product_name': 'count',
        'discount_pct': 'mean',
        'final_price': 'mean'
    }).reset_index()
    retailer_stats.columns = ['Retailer', 'Products', 'Avg Discount %', 'Avg Price €']
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Produktų skaičius',
            x=retailer_stats['Retailer'],
            y=retailer_stats['Products'],
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title='Produktų skaičius pagal parduotuvę',
            xaxis_title='Parduotuvė',
            yaxis_title='Produktų skaičius',
            height=400
        )
        
        return fig
    else:
        # Fallback: return dataframe for table display
        return retailer_stats


def create_discount_distribution_chart(df):
    """Create discount distribution chart"""
    if PLOTLY_AVAILABLE:
        fig = px.histogram(
            df[df['is_promo']], 
            x='discount_pct',
            nbins=20,
            title='Nuolaidų pasiskirstymas',
            labels={'discount_pct': 'Nuolaidos dydis (%)', 'count': 'Dažnumas'},
            color_discrete_sequence=['#2ecc71']
        )
        
        fig.update_layout(height=400)
        return fig
    else:
        # Fallback: return summary stats
        return df[df['is_promo']]['discount_pct'].describe()


def create_category_chart(df):
    """Create category analysis chart"""
    category_stats = df.groupby('category').agg({
        'savings': 'sum',
        'product_name': 'count'
    }).reset_index().sort_values('savings', ascending=False).head(10)
    category_stats.columns = ['Category', 'Total Savings', 'Count']
    
    if PLOTLY_AVAILABLE:
        fig = px.bar(
            category_stats,
            x='Total Savings',
            y='Category',
            orientation='h',
            title='Top 10 kategorijos pagal sutaupymus',
            labels={'Total Savings': 'Sutaupymai (€)', 'Category': 'Kategorija'},
            color='Total Savings',
            color_continuous_scale='Greens'
        )
        
        fig.update_layout(height=500)
        return fig
    else:
        # Fallback: return dataframe
        return category_stats


def create_price_comparison_chart(df, search_term):
    """Create price comparison chart for similar products"""
    mask = df['product_name'].str.contains(search_term, case=False, na=False)
    filtered = df[mask].sort_values('final_price').head(10)
    
    if filtered.empty:
        return None
    
    if PLOTLY_AVAILABLE:
        fig = px.bar(
            filtered,
            x='final_price',
            y='product_name',
            color='retailer',
            orientation='h',
            title=f'Kainų palyginimas: {search_term}',
            labels={'final_price': 'Kaina (€)', 'product_name': 'Produktas', 'retailer': 'Parduotuvė'},
            text='final_price'
        )
        
        fig.update_traces(texttemplate='%{text:.2f}€', textposition='outside')
        fig.update_layout(height=400)
        return fig
    else:
        # Fallback: return dataframe
        return filtered[['product_name', 'retailer', 'final_price']]


def main():
    """Main application"""
    
    # Header
    st.markdown('<p class="main-header">🛒 Lietuvos Prekybos Nuolaidų Analizatorius</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=LT+Promo+Analyzer", use_container_width=True)
        st.markdown("### 📁 Duomenų įkėlimas")
        
        data_source = st.radio(
            "Pasirinkite duomenų šaltinį:",
            ["Demo duomenys", "Įkelti PDF", "Įkelti CSV"]
        )
        
        if data_source == "Demo duomenys":
            if st.button("Įkelti demo duomenis", type="primary"):
                with st.spinner("Generuojami demo duomenys..."):
                    demo_df = load_demo_data()
                    if st.session_state.analyzer:
                        st.session_state.analyzer.promo_products = demo_df
                    st.session_state.demo_data = demo_df
                    st.session_state.products_loaded = True
                    st.success(f"✓ Įkelta {len(demo_df)} produktų!")
                    st.rerun()
        
        elif data_source == "Įkelti PDF":
            st.info("📄 Įkelkite akcijų bukletą PDF formatu")
            
            retailer = st.selectbox(
                "Parduotuvė:",
                ["Maxima", "Rimi", "IKI", "Lidl", "Norfa", "Barbora"]
            )
            
            uploaded_file = st.file_uploader(
                "Pasirinkite PDF failą",
                type=['pdf'],
                help="Įkelkite akcijų bukleto PDF failą"
            )
            
            use_ocr = st.checkbox("Naudoti OCR (skenavotiems PDF)", value=True)
            
            if uploaded_file and st.button("Analizuoti PDF", type="primary"):
                with st.spinner("Analizuojamas PDF..."):
                    try:
                        # Save uploaded file temporarily
                        temp_path = Path(f"/tmp/{uploaded_file.name}")
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Parse the PDF
                        if st.session_state.analyzer:
                            products = st.session_state.analyzer.load_manual_flyer(
                                retailer=retailer,
                                flyer_path=str(temp_path),
                                use_ocr=use_ocr
                            )
                            
                            if not products.empty:
                                st.session_state.products_loaded = True
                                st.success(f"✓ Išanalizuota {len(products)} produktų!")
                                st.rerun()
                            else:
                                st.error("Nepavyko išgauti produktų iš PDF")
                        else:
                            st.error("Analizatorius neprieinamas")
                    except Exception as e:
                        st.error(f"Klaida: {str(e)}")
        
        elif data_source == "Įkelti CSV":
            st.info("📊 Įkelkite CSV failą su produktų duomenimis")
            
            uploaded_csv = st.file_uploader(
                "Pasirinkite CSV failą",
                type=['csv'],
                help="CSV su stulpeliais: retailer, product_name, category, base_price, final_price, discount_pct"
            )
            
            if uploaded_csv and st.button("Įkelti CSV", type="primary"):
                with st.spinner("Įkeliami duomenys..."):
                    try:
                        df = pd.read_csv(uploaded_csv)
                        required_cols = ['retailer', 'product_name', 'category', 'base_price', 'final_price']
                        
                        if all(col in df.columns for col in required_cols):
                            if 'discount_pct' not in df.columns:
                                df['discount_pct'] = ((df['base_price'] - df['final_price']) / df['base_price'] * 100).round(0)
                            if 'is_promo' not in df.columns:
                                df['is_promo'] = df['discount_pct'] > 0
                            if 'savings' not in df.columns:
                                df['savings'] = df['base_price'] - df['final_price']
                            
                            if st.session_state.analyzer:
                                st.session_state.analyzer.promo_products = df
                            st.session_state.demo_data = df
                            st.session_state.products_loaded = True
                            st.success(f"✓ Įkelta {len(df)} produktų!")
                            st.rerun()
                        else:
                            st.error(f"CSV turi turėti stulpelius: {', '.join(required_cols)}")
                    except Exception as e:
                        st.error(f"Klaida: {str(e)}")
        
        st.markdown("---")
        st.markdown("### ℹ️ Apie programą")
        st.markdown("""
        Ši programa padeda:
        - 📊 Analizuoti akcijų bukletus
        - 💰 Rasti geriausius pasiūlymus
        - 🛒 Optimizuoti pirkimo krepšelį
        - 📈 Palyginti kainas
        """)
    
    # Main content
    if not st.session_state.products_loaded:
        # Welcome screen
        st.info("👈 Pradėkite pasirinkdami duomenų šaltinį kairėje pusėje")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Pagrindinės funkcijos")
            st.markdown("""
            - Automatinis PDF analizavimas
            - Kainų palyginimas
            - Sutaupymų skaičiavimas
            - Krepšelio optimizavimas
            """)
        
        with col2:
            st.markdown("### 🏪 Palaikomi prekybos tinklai")
            st.markdown("""
            - Maxima
            - Rimi
            - IKI
            - Lidl
            - Norfa
            - Barbora
            """)
        
        with col3:
            st.markdown("### 📋 Kaip naudotis?")
            st.markdown("""
            1. Įkelkite demo duomenis arba PDF
            2. Peržiūrėkite analizę
            3. Raskite geriausius pasiūlymus
            4. Sukurkite pirkimų sąrašą
            """)
        
        st.markdown("---")
        st.markdown("### 🚀 Greitas startas")
        st.markdown("Paspauskite **'Įkelti demo duomenis'** kairėje, kad išbandytumėte programą!")
        
    else:
        # Get data
        df = st.session_state.demo_data
        if df is None and st.session_state.analyzer and st.session_state.analyzer.promo_products is not None:
            df = st.session_state.analyzer.promo_products
        
        if df is None or df.empty:
            st.error("Nėra įkeltų duomenų")
            return
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Apžvalga", 
            "🏆 Geriausi pasiūlymai", 
            "🔍 Kainų palyginimas",
            "🛒 Krepšelio optimizavimas",
            "📥 Eksportas"
        ])
        
        with tab1:
            st.markdown("### 📊 Bendroji statistika")
            create_summary_metrics(df)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                chart1 = create_retailer_comparison_chart(df)
                if PLOTLY_AVAILABLE:
                    st.plotly_chart(chart1, use_container_width=True)
                else:
                    st.dataframe(chart1, use_container_width=True)
            
            with col2:
                chart2 = create_discount_distribution_chart(df)
                if PLOTLY_AVAILABLE:
                    st.plotly_chart(chart2, use_container_width=True)
                else:
                    st.write("**Discount Statistics:**")
                    st.write(chart2)
            
            chart3 = create_category_chart(df)
            if PLOTLY_AVAILABLE:
                st.plotly_chart(chart3, use_container_width=True)
            else:
                st.dataframe(chart3, use_container_width=True)
            
            # Retailer details
            st.markdown("### 🏪 Detalesnė parduotuvių analizė")
            
            retailer_details = df.groupby('retailer').agg({
                'product_name': 'count',
                'discount_pct': 'mean',
                'final_price': 'mean',
                'savings': 'sum'
            }).round(2)
            retailer_details.columns = ['Produktų', 'Vidut. nuolaida %', 'Vidut. kaina €', 'Viso sutaupymų €']
            
            st.dataframe(retailer_details, use_container_width=True)
        
        with tab2:
            st.markdown("### 🏆 Geriausi pasiūlymai")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                filter_category = st.selectbox(
                    "Filtruoti pagal kategoriją:",
                    ["Visos"] + sorted(df['category'].unique().tolist())
                )
                
                top_n = st.slider("Rodyti top N pasiūlymų:", 5, 50, 20)
            
            with col2:
                # Filter and calculate deal score
                filtered_df = df.copy()
                if filter_category != "Visos":
                    filtered_df = filtered_df[filtered_df['category'] == filter_category]
                
                filtered_df['deal_score'] = (
                    filtered_df['discount_pct'] * 0.5 + 
                    (filtered_df['savings'] / filtered_df['base_price'] * 100) * 0.5
                )
                
                best_deals = filtered_df.nlargest(top_n, 'deal_score')[
                    ['retailer', 'product_name', 'category', 'base_price', 'final_price', 'discount_pct', 'savings']
                ].reset_index(drop=True)
                
                st.markdown(f"**Rodoma {len(best_deals)} pasiūlymų**")
                
                # Display deals as cards
                for idx, deal in best_deals.iterrows():
                    with st.container():
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        
                        with col_a:
                            st.markdown(f"**{deal['product_name']}**")
                            st.caption(f"🏪 {deal['retailer']} | 📂 {deal['category']}")
                        
                        with col_b:
                            st.metric("Kaina", f"{deal['final_price']:.2f} €", 
                                     delta=f"-{deal['discount_pct']:.0f}%",
                                     delta_color="inverse")
                        
                        with col_c:
                            st.metric("Sutaupoma", f"{deal['savings']:.2f} €")
                        
                        st.markdown("---")
        
        with tab3:
            st.markdown("### 🔍 Kainų palyginimas")
            
            search_term = st.text_input(
                "Ieškoti produkto (pvz., 'pienas', 'duona', 'mėsa'):",
                placeholder="Įveskite produkto pavadinimą..."
            )
            
            if search_term:
                mask = df['product_name'].str.contains(search_term, case=False, na=False)
                results = df[mask].sort_values('final_price')
                
                if not results.empty:
                    st.success(f"Rasta {len(results)} produktų")
                    
                    # Chart
                    fig = create_price_comparison_chart(df, search_term)
                    if fig is not None:
                        if PLOTLY_AVAILABLE:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.markdown("#### Kainų palyginimas")
                            st.dataframe(fig, use_container_width=True)
                    
                    # Table
                    st.markdown("#### Detali lentelė")
                    comparison_table = results[
                        ['retailer', 'product_name', 'final_price', 'base_price', 'discount_pct', 'savings']
                    ].head(20)
                    st.dataframe(comparison_table, use_container_width=True)
                    
                    # Best deal highlight
                    best = results.iloc[0]
                    st.success(f"🏆 **Geriausias pasiūlymas:** {best['product_name']} - {best['retailer']} už {best['final_price']:.2f} € (-{best['discount_pct']:.0f}%)")
                else:
                    st.warning(f"Nerasta produktų pagal '{search_term}'")
        
        with tab4:
            st.markdown("### 🛒 Krepšelio optimizavimas")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Jūsų poreikiai")
                
                budget = st.number_input("Biudžetas (€):", min_value=10.0, max_value=500.0, value=50.0, step=5.0)
                
                st.markdown("**Pasirinkite kategorijas ir kiekius:**")
                
                categories = sorted(df['category'].unique())
                selected_needs = {}
                
                for cat in categories:
                    qty = st.number_input(f"{cat}:", min_value=0, max_value=20, value=0, key=f"cat_{cat}")
                    if qty > 0:
                        selected_needs[cat] = qty
            
            with col2:
                st.markdown("#### Optimizavimo strategija")
                
                strategy = st.radio(
                    "Pasirinkite strategiją:",
                    ["Maksimalūs sutaupymai", "Įvairovė", "Viena parduotuvė"]
                )
                
                if st.button("Optimizuoti krepšelį", type="primary"):
                    if not selected_needs:
                        st.warning("Pasirinkite bent vieną kategoriją")
                    else:
                        with st.spinner("Optimizuojamas krepšelis..."):
                            # Simple optimization logic
                            cart_items = []
                            current_total = 0
                            
                            for category, qty in selected_needs.items():
                                cat_products = df[df['category'] == category].copy()
                                
                                if strategy == "Maksimalūs sutaupymai":
                                    cat_products = cat_products.sort_values('discount_pct', ascending=False)
                                elif strategy == "Įvairovė":
                                    cat_products = cat_products.sample(frac=1)
                                elif strategy == "Viena parduotuvė":
                                    # Find retailer with most products
                                    best_retailer = df['retailer'].value_counts().idxmax()
                                    cat_products = cat_products[cat_products['retailer'] == best_retailer]
                                
                                for _, product in cat_products.head(qty).iterrows():
                                    if current_total + product['final_price'] <= budget:
                                        cart_items.append(product)
                                        current_total += product['final_price']
                            
                            if cart_items:
                                cart_df = pd.DataFrame(cart_items)
                                
                                st.success("✓ Krepšelis optimizuotas!")
                                
                                # Summary metrics
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("Produktų", len(cart_df))
                                with col_b:
                                    st.metric("Suma", f"{cart_df['final_price'].sum():.2f} €")
                                with col_c:
                                    st.metric("Sutaupyta", f"{cart_df['savings'].sum():.2f} €")
                                
                                # Cart details
                                st.markdown("#### Krepšelio turinys")
                                cart_display = cart_df[['retailer', 'product_name', 'category', 'final_price', 'discount_pct']]
                                st.dataframe(cart_display, use_container_width=True)
                                
                                # By retailer
                                st.markdown("#### Paskirstymas pagal parduotuves")
                                retailer_summary = cart_df.groupby('retailer').agg({
                                    'product_name': 'count',
                                    'final_price': 'sum'
                                }).round(2)
                                retailer_summary.columns = ['Produktų', 'Suma €']
                                st.dataframe(retailer_summary, use_container_width=True)
                            else:
                                st.warning("Nepavyko sudaryti krepšelio su nurodytu biudžetu")
        
        with tab5:
            st.markdown("### 📥 Duomenų eksportavimas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Eksportuoti CSV")
                
                export_data = df[['retailer', 'product_name', 'category', 'base_price', 
                                 'final_price', 'discount_pct', 'savings']]
                
                csv = export_data.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="⬇️ Atsisiųsti visus duomenis (CSV)",
                    data=csv,
                    file_name=f"promo_products_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
                # Best deals only
                best_deals_export = df.nlargest(50, 'discount_pct')[
                    ['retailer', 'product_name', 'category', 'base_price', 'final_price', 'discount_pct']
                ]
                csv_best = best_deals_export.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="⬇️ Atsisiųsti geriausius pasiūlymus (CSV)",
                    data=csv_best,
                    file_name=f"best_deals_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                st.markdown("#### Ataskaita")
                
                # Generate report
                report_lines = [
                    "LIETUVOS PREKYBOS NUOLAIDŲ ATASKAITA",
                    "=" * 60,
                    f"Sugeneruota: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    "",
                    "BENDROJI STATISTIKA:",
                    f"  Produktų: {len(df)}",
                    f"  Parduotuvių: {df['retailer'].nunique()}",
                    f"  Kategorijų: {df['category'].nunique()}",
                    f"  Vidutinė nuolaida: {df['discount_pct'].mean():.1f}%",
                    f"  Bendri sutaupymai: {df['savings'].sum():.2f} €",
                    "",
                    "TOP 10 PASIŪLYMŲ:",
                    "-" * 60
                ]
                
                best = df.nlargest(10, 'discount_pct')
                for i, (_, deal) in enumerate(best.iterrows(), 1):
                    report_lines.append(f"{i}. {deal['product_name']}")
                    report_lines.append(f"   {deal['retailer']} - {deal['final_price']:.2f}€ (-{deal['discount_pct']:.0f}%)")
                
                report_text = "\n".join(report_lines)
                
                st.download_button(
                    label="📄 Atsisiųsti ataskaitą (TXT)",
                    data=report_text.encode('utf-8'),
                    file_name=f"promo_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            st.markdown("---")
            st.info("💡 Patarimas: Naudokite CSV failus tolesnei analizei Excel ar kitose programose")


if __name__ == "__main__":
    if not ANALYZER_AVAILABLE:
        st.error("⚠️ Analizatorius neprieinamas. Įsitikinkite, kad lt_promo_analyzer_enhanced.py yra tame pačiame kataloge.")
    else:
        main()
