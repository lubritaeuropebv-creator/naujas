"""
Lithuanian Food Retailers Promo Cart Analysis Tool with Flyer Scraping
=======================================================================
Automatically finds, downloads, and parses promotional flyers from Lithuanian retailers
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json
import re
import requests
from pathlib import Path
import time

# PDF parsing libraries
try:
    import PyPDF2
    import pdfplumber
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    PDF_LIBS_AVAILABLE = True
except ImportError:
    PDF_LIBS_AVAILABLE = False
    print("Warning: PDF parsing libraries not available. Install: pip install PyPDF2 pdfplumber pdf2image pytesseract pillow")


class PromoFlyerScraper:
    """
    Scrapes and parses promotional flyers from Lithuanian food retailers.
    """
    
    def __init__(self, download_dir: str = "./flyers"):
        """
        Initialize the flyer scraper.
        
        Args:
            download_dir: Directory to save downloaded flyers
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Lithuanian retailer flyer URLs and patterns
        self.retailer_configs = {
            'Maxima': {
                'base_url': 'https://www.maxima.lt',
                'flyer_page': 'https://www.maxima.lt/akcijos',
                'pdf_pattern': r'\.pdf',
                'name_patterns': ['akcij', 'nuolaid', 'special'],
            },
            'Rimi': {
                'base_url': 'https://www.rimi.lt',
                'flyer_page': 'https://www.rimi.lt/akcijos',
                'pdf_pattern': r'\.pdf',
                'name_patterns': ['akcij', 'savaites', 'week'],
            },
            'IKI': {
                'base_url': 'https://www.iki.lt',
                'flyer_page': 'https://www.iki.lt/akcijos',
                'pdf_pattern': r'\.pdf',
                'name_patterns': ['akcij', 'savaitės'],
            },
            'Lidl': {
                'base_url': 'https://www.lidl.lt',
                'flyer_page': 'https://www.lidl.lt/akcijos',
                'pdf_pattern': r'\.pdf',
                'name_patterns': ['akcij', 'pasiulym'],
            },
            'Norfa': {
                'base_url': 'https://www.norfa.lt',
                'flyer_page': 'https://www.norfa.lt/akcijos',
                'pdf_pattern': r'\.pdf',
                'name_patterns': ['akcij', 'nuolaid'],
            },
        }
        
        # Price patterns for Lithuanian formats
        self.price_patterns = [
            r'(\d+)[,.](\d{2})\s*€',  # 2,99 € or 2.99 €
            r'(\d+)[,.](\d{2})\s*EUR',  # 2,99 EUR
            r'€\s*(\d+)[,.](\d{2})',  # € 2,99
            r'(\d+)\s*ct',  # cents
        ]
        
        # Discount patterns
        self.discount_patterns = [
            r'-(\d+)%',  # -30%
            r'(\d+)%\s*nuolaida',  # 30% nuolaida
            r'taupyk.*?(\d+)%',  # taupyk iki 30%
            r'iki\s*-(\d+)%',  # iki -30%
        ]
        
        # Product category keywords in Lithuanian
        self.category_keywords = {
            'Pieno produktai': ['pienas', 'jogurt', 'grietinė', 'varškė', 'sūris', 'sviestas'],
            'Mėsa ir mėsos gaminiai': ['mėsa', 'dešra', 'kumpi', 'filė', 'šonin', 'dešrel'],
            'Duona ir konditerija': ['duona', 'batonas', 'bandel', 'pyraga', 'kepalin'],
            'Vaisiai ir daržovės': ['obuol', 'banan', 'pomidor', 'agurkr', 'moliūg', 'kopūst'],
            'Gėrimai': ['sultys', 'vanduo', 'gėrim', 'limonadas', 'arbata', 'kava'],
            'Konservai': ['konserv', 'marinet', 'grybai', 'žuvies'],
            'Užšaldyti produktai': ['užšaldyt', 'ledai', 'pizza'],
            'Sausainiai ir saldumynai': ['sausain', 'šokolad', 'saldain', 'vafliai'],
            'Makaronai ir kruopos': ['makaron', 'kruopos', 'ryžiai', 'grikiai'],
            'Kosmetika ir higiena': ['šampūnas', 'muilas', 'pasta', 'dušo želė'],
        }
        
        self.parsed_flyers = []
    
    def download_flyer(self, url: str, retailer: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        Download a promotional flyer PDF.
        
        Args:
            url: URL of the PDF flyer
            retailer: Name of the retailer
            filename: Optional custom filename
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{retailer}_{timestamp}.pdf"
            
            filepath = self.download_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Downloaded: {filename} ({len(response.content) / 1024:.1f} KB)")
            return filepath
            
        except Exception as e:
            print(f"✗ Failed to download {url}: {str(e)}")
            return None
    
    def find_flyer_urls(self, retailer: str) -> List[str]:
        """
        Find promotional flyer URLs from retailer's website.
        
        Args:
            retailer: Name of the retailer
            
        Returns:
            List of PDF URLs found
        """
        if retailer not in self.retailer_configs:
            print(f"Retailer {retailer} not configured")
            return []
        
        config = self.retailer_configs[retailer]
        pdf_urls = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(config['flyer_page'], headers=headers, timeout=30)
            response.raise_for_status()
            
            # Find all PDF links
            pdf_pattern = re.compile(config['pdf_pattern'], re.IGNORECASE)
            
            # Simple regex to find href links
            href_pattern = re.compile(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', re.IGNORECASE)
            matches = href_pattern.findall(response.text)
            
            for match in matches:
                # Convert relative URLs to absolute
                if match.startswith('http'):
                    pdf_url = match
                elif match.startswith('/'):
                    pdf_url = config['base_url'] + match
                else:
                    pdf_url = config['base_url'] + '/' + match
                
                pdf_urls.append(pdf_url)
            
            print(f"Found {len(pdf_urls)} PDF flyer(s) for {retailer}")
            
        except Exception as e:
            print(f"Error finding flyers for {retailer}: {str(e)}")
        
        return pdf_urls
    
    def parse_pdf_text(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using multiple methods.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        if not PDF_LIBS_AVAILABLE:
            return ""
        
        text = ""
        
        # Try pdfplumber first (better for structured PDFs)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {str(e)}")
        
        # Fallback to PyPDF2
        if not text.strip():
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"PyPDF2 failed: {str(e)}")
        
        return text
    
    def parse_pdf_with_ocr(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using OCR (for image-based PDFs).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text via OCR
        """
        if not PDF_LIBS_AVAILABLE:
            return ""
        
        text = ""
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300, first_page=1, last_page=10)
            
            # OCR each page
            for i, image in enumerate(images):
                print(f"  OCR processing page {i+1}...")
                page_text = pytesseract.image_to_string(image, lang='lit+eng')
                text += page_text + "\n"
                
        except Exception as e:
            print(f"OCR failed: {str(e)}")
        
        return text
    
    def extract_prices_from_text(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract prices from text.
        
        Args:
            text: Text to parse
            
        Returns:
            List of (context, price) tuples
        """
        prices = []
        
        for pattern in self.price_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    if 'ct' in match.group(0).lower():
                        price = float(match.group(1)) / 100
                    else:
                        euros = match.group(1)
                        cents = match.group(2) if len(match.groups()) > 1 else '00'
                        price = float(f"{euros}.{cents}")
                    
                    # Get context (surrounding text)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    prices.append((context, price))
                except:
                    continue
        
        return prices
    
    def extract_discounts_from_text(self, text: str) -> List[Tuple[str, int]]:
        """
        Extract discount percentages from text.
        
        Args:
            text: Text to parse
            
        Returns:
            List of (context, discount_pct) tuples
        """
        discounts = []
        
        for pattern in self.discount_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    discount = int(match.group(1))
                    
                    # Get context
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    discounts.append((context, discount))
                except:
                    continue
        
        return discounts
    
    def categorize_product(self, text: str) -> Optional[str]:
        """
        Categorize a product based on text keywords.
        
        Args:
            text: Product description text
            
        Returns:
            Category name or None
        """
        text_lower = text.lower()
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return None
    
    def parse_flyer(self, pdf_path: Path, retailer: str, use_ocr: bool = False) -> pd.DataFrame:
        """
        Parse a promotional flyer PDF and extract product information.
        
        Args:
            pdf_path: Path to PDF file
            retailer: Name of retailer
            use_ocr: Whether to use OCR for image-based PDFs
            
        Returns:
            DataFrame with parsed products
        """
        print(f"\nParsing flyer: {pdf_path.name}")
        
        # Extract text
        if use_ocr:
            text = self.parse_pdf_with_ocr(pdf_path)
        else:
            text = self.parse_pdf_text(pdf_path)
        
        if not text.strip():
            print("  ⚠ No text extracted. Try with use_ocr=True")
            return pd.DataFrame()
        
        # Extract prices and discounts
        prices = self.extract_prices_from_text(text)
        discounts = self.extract_discounts_from_text(text)
        
        print(f"  Found {len(prices)} prices and {len(discounts)} discounts")
        
        # Create products dataframe
        products = []
        
        for context, price in prices:
            # Try to find associated discount
            discount_pct = 0
            for disc_context, disc in discounts:
                # Simple matching: if contexts overlap
                if any(word in context.lower() for word in disc_context.lower().split()[:5]):
                    discount_pct = disc
                    break
            
            # Categorize product
            category = self.categorize_product(context)
            
            # Extract product name (simplified - take first meaningful words)
            words = context.split()
            product_name = ' '.join(words[:5]) if words else "Unknown Product"
            
            # Calculate prices
            if discount_pct > 0:
                final_price = price
                base_price = round(price / (1 - discount_pct/100), 2)
            else:
                final_price = price
                base_price = price
            
            products.append({
                'retailer': retailer,
                'product_name': product_name,
                'category': category if category else 'Kita',
                'base_price': base_price,
                'final_price': final_price,
                'discount_pct': discount_pct,
                'is_promo': discount_pct > 0,
                'source_file': pdf_path.name,
                'parsed_date': datetime.now()
            })
        
        df = pd.DataFrame(products)
        
        if not df.empty:
            # Remove duplicates based on product name and price
            df = df.drop_duplicates(subset=['product_name', 'final_price'])
            print(f"  ✓ Extracted {len(df)} unique products")
        
        return df
    
    def scrape_all_retailers(self, retailers: Optional[List[str]] = None, 
                            use_ocr: bool = False, max_flyers_per_retailer: int = 2) -> pd.DataFrame:
        """
        Scrape promotional flyers from all configured retailers.
        
        Args:
            retailers: List of retailer names to scrape (None for all)
            use_ocr: Whether to use OCR for image-based PDFs
            max_flyers_per_retailer: Maximum number of flyers to download per retailer
            
        Returns:
            Combined DataFrame with all products
        """
        if retailers is None:
            retailers = list(self.retailer_configs.keys())
        
        all_products = []
        
        for retailer in retailers:
            print(f"\n{'='*70}")
            print(f"Processing {retailer}")
            print('='*70)
            
            # Find flyer URLs
            flyer_urls = self.find_flyer_urls(retailer)
            
            # Download and parse flyers
            for i, url in enumerate(flyer_urls[:max_flyers_per_retailer]):
                print(f"\nFlyer {i+1}/{min(len(flyer_urls), max_flyers_per_retailer)}")
                
                # Download
                pdf_path = self.download_flyer(url, retailer)
                
                if pdf_path:
                    # Parse
                    products_df = self.parse_flyer(pdf_path, retailer, use_ocr=use_ocr)
                    
                    if not products_df.empty:
                        all_products.append(products_df)
                    
                    # Rate limiting
                    time.sleep(2)
        
        # Combine all products
        if all_products:
            combined_df = pd.concat(all_products, ignore_index=True)
            print(f"\n{'='*70}")
            print(f"TOTAL: Scraped {len(combined_df)} products from {len(all_products)} flyers")
            print('='*70)
            return combined_df
        else:
            print("\n⚠ No products extracted")
            return pd.DataFrame()
    
    def manual_flyer_input(self, retailer: str, flyer_path: str, use_ocr: bool = False) -> pd.DataFrame:
        """
        Parse a manually provided flyer PDF.
        
        Args:
            retailer: Name of retailer
            flyer_path: Path to PDF file
            use_ocr: Whether to use OCR
            
        Returns:
            DataFrame with parsed products
        """
        pdf_path = Path(flyer_path)
        
        if not pdf_path.exists():
            print(f"File not found: {flyer_path}")
            return pd.DataFrame()
        
        return self.parse_flyer(pdf_path, retailer, use_ocr=use_ocr)


class LTPromoCartAnalyzer:
    """
    Enhanced analyzer with automatic flyer scraping capabilities.
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.retailers = {
            'Maxima': {'category': 'Supermarket', 'chain_size': 'Large'},
            'Rimi': {'category': 'Supermarket', 'chain_size': 'Large'},
            'IKI': {'category': 'Supermarket', 'chain_size': 'Large'},
            'Lidl': {'category': 'Discount', 'chain_size': 'Large'},
            'Norfa': {'category': 'Supermarket', 'chain_size': 'Medium'},
            'Barbora': {'category': 'Online', 'chain_size': 'Large'}
        }
        
        self.data = None
        self.promo_products = None
        self.scraper = PromoFlyerScraper()
    
    def load_from_flyers(self, retailers: Optional[List[str]] = None, 
                        use_ocr: bool = False) -> pd.DataFrame:
        """
        Load promotional data by scraping flyers from retailers.
        
        Args:
            retailers: List of retailers to scrape
            use_ocr: Whether to use OCR for image-based PDFs
            
        Returns:
            DataFrame with scraped products
        """
        self.promo_products = self.scraper.scrape_all_retailers(
            retailers=retailers,
            use_ocr=use_ocr
        )
        
        return self.promo_products
    
    def load_manual_flyer(self, retailer: str, flyer_path: str, use_ocr: bool = False) -> pd.DataFrame:
        """
        Load and parse a manual flyer PDF.
        
        Args:
            retailer: Retailer name
            flyer_path: Path to PDF
            use_ocr: Whether to use OCR
            
        Returns:
            DataFrame with products
        """
        products = self.scraper.manual_flyer_input(retailer, flyer_path, use_ocr)
        
        if self.promo_products is None:
            self.promo_products = products
        else:
            self.promo_products = pd.concat([self.promo_products, products], ignore_index=True)
        
        return products
    
    def analyze_current_promos(self) -> pd.DataFrame:
        """
        Analyze currently available promotions from scraped flyers.
        
        Returns:
            Analysis summary
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded. Run load_from_flyers() first.")
        
        analysis = self.promo_products.groupby('retailer').agg({
            'product_name': 'count',
            'discount_pct': 'mean',
            'final_price': ['mean', 'min', 'max'],
            'is_promo': 'sum'
        }).round(2)
        
        analysis.columns = ['total_products', 'avg_discount', 'avg_price', 'min_price', 'max_price', 'promo_count']
        
        return analysis.sort_values('promo_count', ascending=False)
    
    def find_best_deals(self, category: Optional[str] = None, top_n: int = 10) -> pd.DataFrame:
        """
        Find the best deals from scraped flyers.
        
        Args:
            category: Optional category filter
            top_n: Number of top deals to return
            
        Returns:
            DataFrame with best deals
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded.")
        
        df = self.promo_products[self.promo_products['is_promo'] == True].copy()
        
        if category:
            df = df[df['category'] == category]
        
        # Calculate savings
        df['savings'] = df['base_price'] - df['final_price']
        
        # Sort by discount percentage and savings
        df['deal_score'] = df['discount_pct'] * 0.7 + (df['savings'] / df['base_price'] * 100) * 0.3
        
        best_deals = df.nlargest(top_n, 'deal_score')[
            ['retailer', 'product_name', 'category', 'base_price', 'final_price', 'discount_pct', 'savings']
        ]
        
        return best_deals
    
    def compare_prices_across_retailers(self, search_term: str) -> pd.DataFrame:
        """
        Compare prices for similar products across retailers.
        
        Args:
            search_term: Product search term
            
        Returns:
            Price comparison DataFrame
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded.")
        
        # Find products matching search term
        mask = self.promo_products['product_name'].str.contains(search_term, case=False, na=False)
        matches = self.promo_products[mask][
            ['retailer', 'product_name', 'final_price', 'discount_pct', 'is_promo']
        ].sort_values('final_price')
        
        return matches
    
    def optimize_shopping_cart(self, desired_products: Dict[str, int], 
                              budget: Optional[float] = None) -> Dict:
        """
        Optimize shopping cart based on available promotions.
        
        Args:
            desired_products: Dict of {category: quantity}
            budget: Optional budget constraint
            
        Returns:
            Optimized cart with retailer recommendations
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded.")
        
        cart = []
        total_cost = 0
        total_savings = 0
        
        for category, qty in desired_products.items():
            # Find best deals in this category
            category_products = self.promo_products[
                self.promo_products['category'] == category
            ].copy()
            
            if category_products.empty:
                continue
            
            # Sort by price (prefer promos)
            category_products['sort_key'] = category_products['final_price'] - (
                category_products['is_promo'].astype(int) * 0.01
            )
            best_products = category_products.nsmallest(qty, 'sort_key')
            
            for _, product in best_products.iterrows():
                item_cost = product['final_price']
                
                if budget and (total_cost + item_cost) > budget:
                    continue
                
                cart.append({
                    'retailer': product['retailer'],
                    'product': product['product_name'],
                    'category': category,
                    'price': item_cost,
                    'original_price': product['base_price'],
                    'discount': product['discount_pct'],
                    'is_promo': product['is_promo']
                })
                
                total_cost += item_cost
                total_savings += (product['base_price'] - item_cost)
        
        return {
            'cart': pd.DataFrame(cart),
            'total_cost': round(total_cost, 2),
            'total_savings': round(total_savings, 2),
            'items_count': len(cart),
            'retailers': list(set([item['retailer'] for item in cart]))
        }
    
    def generate_shopping_list(self, budget: float, optimize_for: str = 'savings') -> pd.DataFrame:
        """
        Generate optimized shopping list based on budget and strategy.
        
        Args:
            budget: Shopping budget in EUR
            optimize_for: 'savings', 'variety', or 'single_retailer'
            
        Returns:
            Shopping list DataFrame
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded.")
        
        promo_items = self.promo_products[self.promo_products['is_promo'] == True].copy()
        
        if optimize_for == 'savings':
            # Prioritize highest discount percentages
            promo_items = promo_items.sort_values('discount_pct', ascending=False)
        elif optimize_for == 'variety':
            # Maximize category variety
            promo_items = promo_items.groupby('category').apply(
                lambda x: x.nsmallest(2, 'final_price')
            ).reset_index(drop=True)
        elif optimize_for == 'single_retailer':
            # Find retailer with most promos
            best_retailer = promo_items['retailer'].value_counts().idxmax()
            promo_items = promo_items[promo_items['retailer'] == best_retailer]
        
        # Build shopping list within budget
        shopping_list = []
        current_total = 0
        
        for _, item in promo_items.iterrows():
            if current_total + item['final_price'] <= budget:
                shopping_list.append(item)
                current_total += item['final_price']
            
            if current_total >= budget * 0.95:  # Stop at 95% of budget
                break
        
        return pd.DataFrame(shopping_list)
    
    def visualize_promo_comparison(self, save_path: Optional[str] = None):
        """
        Visualize promotional comparisons across retailers.
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded.")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Products per retailer
        retailer_counts = self.promo_products['retailer'].value_counts()
        retailer_counts.plot(kind='bar', ax=axes[0, 0], color='steelblue')
        axes[0, 0].set_title('Produktų skaičius pagal parduotuvę', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Parduotuvė')
        axes[0, 0].set_ylabel('Produktų skaičius')
        
        # 2. Average discount by retailer
        avg_discounts = self.promo_products[self.promo_products['is_promo'] == True].groupby('retailer')['discount_pct'].mean()
        avg_discounts.plot(kind='barh', ax=axes[0, 1], color='coral')
        axes[0, 1].set_title('Vidutinė nuolaida pagal parduotuvę (%)', fontsize=12, fontweight='bold')
        axes[0, 1].set_xlabel('Vidutinė nuolaida (%)')
        
        # 3. Category distribution
        category_counts = self.promo_products['category'].value_counts().head(10)
        category_counts.plot(kind='barh', ax=axes[1, 0], color='lightgreen')
        axes[1, 0].set_title('Top 10 kategorijų', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Produktų skaičius')
        
        # 4. Price distribution
        self.promo_products['final_price'].hist(bins=30, ax=axes[1, 1], color='lightblue', edgecolor='black')
        axes[1, 1].set_title('Kainų pasiskirstymas', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Kaina (EUR)')
        axes[1, 1].set_ylabel('Dažnumas')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        plt.show()
    
    def export_shopping_guide(self, output_path: str = './shopping_guide.txt'):
        """
        Export a comprehensive shopping guide based on scraped promos.
        """
        if self.promo_products is None or self.promo_products.empty:
            raise ValueError("No promo data loaded.")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("LIETUVOS MAISTO PREKYBOS APSIPIRKIMO VADOVAS\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Sugeneruota: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            # Best deals overall
            f.write("GERIAUSI PASIŪLYMAI:\n")
            f.write("-"*70 + "\n")
            best_deals = self.find_best_deals(top_n=15)
            for i, (_, deal) in enumerate(best_deals.iterrows(), 1):
                f.write(f"{i}. {deal['product_name']}\n")
                f.write(f"   {deal['retailer']} | {deal['final_price']:.2f}€ (buvo {deal['base_price']:.2f}€)\n")
                f.write(f"   Nuolaida: {deal['discount_pct']}% | Sutaupoma: {deal['savings']:.2f}€\n\n")
            
            # Best deals by category
            f.write("\n" + "="*70 + "\n")
            f.write("GERIAUSI PASIŪLYMAI PAGAL KATEGORIJAS:\n")
            f.write("="*70 + "\n\n")
            
            categories = self.promo_products['category'].unique()
            for category in sorted(categories):
                if category == 'Kita':
                    continue
                    
                f.write(f"\n{category}:\n")
                f.write("-"*70 + "\n")
                
                cat_deals = self.find_best_deals(category=category, top_n=5)
                for _, deal in cat_deals.iterrows():
                    f.write(f"• {deal['product_name']}\n")
                    f.write(f"  {deal['retailer']}: {deal['final_price']:.2f}€ (-{deal['discount_pct']}%)\n")
            
            f.write("\n" + "="*70 + "\n")
        
        print(f"Shopping guide exported to {output_path}")


def main():
    """
    Demo of enhanced analyzer with flyer scraping.
    """
    print("Lietuvos maisto prekybos nuolaidų analizės įrankis")
    print("su automatiniu akcijų bukleto nuskaitymu")
    print("="*70)
    print()
    
    analyzer = LTPromoCartAnalyzer()
    
    # OPTION 1: Try to scrape from websites (may fail due to network restrictions)
    print("PASTABA: Dėl tinklo apribojimų, automatinis nuskaitymas gali neveikti.")
    print("Demonstracijai naudokite load_manual_flyer() funkciją su savo PDF failais.\n")
    
    # OPTION 2: Manual flyer input (recommended for demo)
    print("Demonstracija su rankiniu PDF failu:")
    print("analyzer.load_manual_flyer('Maxima', 'path/to/flyer.pdf', use_ocr=True)")
    print()
    
    # OPTION 3: Use sample data for demonstration
    print("Generuojami demonstraciniai duomenys...")
    
    # Create sample promo data
    sample_promos = []
    retailers = ['Maxima', 'Rimi', 'IKI', 'Lidl', 'Norfa']
    categories = ['Pieno produktai', 'Mėsa ir mėsos gaminiai', 'Duona ir konditerija',
                  'Vaisiai ir daržovės', 'Gėrimai']
    
    np.random.seed(42)
    for i in range(100):
        retailer = np.random.choice(retailers)
        category = np.random.choice(categories)
        base_price = np.random.uniform(1.0, 15.0)
        discount = np.random.choice([10, 20, 25, 30, 50])
        final_price = base_price * (1 - discount/100)
        
        sample_promos.append({
            'retailer': retailer,
            'product_name': f'{category} produktas {i}',
            'category': category,
            'base_price': round(base_price, 2),
            'final_price': round(final_price, 2),
            'discount_pct': discount,
            'is_promo': True,
            'source_file': 'demo_data',
            'parsed_date': datetime.now()
        })
    
    analyzer.promo_products = pd.DataFrame(sample_promos)
    print(f"✓ Įkelta {len(analyzer.promo_products)} demonstracinių produktų\n")
    
    # Analyze current promos
    print("DABARTINĖS AKCIJOS:")
    print(analyzer.analyze_current_promos())
    print()
    
    # Find best deals
    print("\nGERIAUSI PASIŪLYMAI:")
    print(analyzer.find_best_deals(top_n=5))
    print()
    
    # Optimize shopping cart
    print("\nOPTIMALUS KREPŠELIS (50 EUR biudžetas):")
    desired_products = {
        'Pieno produktai': 3,
        'Mėsa ir mėsos gaminiai': 2,
        'Duona ir konditerija': 2,
        'Gėrimai': 2
    }
    cart_result = analyzer.optimize_shopping_cart(desired_products, budget=50)
    print(f"Produktų: {cart_result['items_count']}")
    print(f"Suma: {cart_result['total_cost']} EUR")
    print(f"Sutaupyta: {cart_result['total_savings']} EUR")
    print(f"Parduotuvės: {', '.join(cart_result['retailers'])}")
    print()
    
    # Visualize
    print("Generuojami grafikai...")
    analyzer.visualize_promo_comparison(save_path='/home/claude/promo_comparison.png')
    
    # Export guide
    analyzer.export_shopping_guide(output_path='/home/claude/shopping_guide.txt')
    
    print("\n✓ Demonstracija baigta!")
    print("\nKaip naudoti su tikrais duomenimis:")
    print("1. Atsisiųskite akcijų bukletą PDF formatu")
    print("2. analyzer.load_manual_flyer('Maxima', 'kelias/iki/failo.pdf', use_ocr=True)")
    print("3. Analizuokite su analyzer.find_best_deals()")


if __name__ == "__main__":
    main()
