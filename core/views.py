from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_html_content(min_price, max_price):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    url = session.get(f'https://superbipt.store/all/?orderby=popularity').text
    return url

def home(request):
    product_data = None

    if 'min_price' in request.GET and 'max_price' in request.GET:
        orderby = request.GET.get('orderby')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        html_content = get_html_content(min_price, max_price)
        soup = BeautifulSoup(html_content, 'html.parser')

        product_data = []

        # Find all product list items
        product_items = soup.find_all('li', class_='ast-grid-common-col')

        for item in product_items:
            product_info = {}
            product_info['title'] = item.find('h2', class_='woocommerce-loop-product__title').text.strip()

            # Extract category information
            category_span = item.find('span', class_='ast-woo-product-category')
            product_info['category'] = category_span.text.strip() if category_span else ''

            # Extract price information
            product_info['price']=soup.find('span',class_='price').text

            # Extract image URL
            img_tag = item.find('img', class_='attachment-woocommerce_thumbnail')
            product_info['image_url'] = img_tag['src'] if img_tag else ''

            product_data.append(product_info)

    return render(request, 'core/home.html', {'product': product_data})
