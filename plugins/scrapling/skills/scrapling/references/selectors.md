# Scrapling Selector Reference

Scrapling uses Scrapy/Parsel-compatible selector syntax.

## CSS Selectors

```python
# Text content (::text pseudo-element)
page.css('h1::text').get()                    # first match
page.css('h1::text').getall()                 # all matches

# Attribute value (::attr pseudo-element)
page.css('a::attr(href)').getall()            # all links
page.css('img::attr(src)').get()              # first image src

# Multiple selectors
page.css('h1, h2, h3::text').getall()

# Descendant
page.css('.article p::text').getall()

# Direct child
page.css('ul > li::text').getall()

# Attribute filter
page.css('a[href^="https"]::attr(href)').getall()   # href starts with https
page.css('input[type="submit"]').get()

# Class and ID
page.css('.product-title::text').getall()
page.css('#main-content p::text').getall()
```

## XPath Selectors

```python
# Text content
page.xpath('//h1/text()').get()
page.xpath('//p/text()').getall()

# Attribute
page.xpath('//a/@href').getall()
page.xpath('//img/@src').getall()

# Contains text
page.xpath('//*[contains(text(), "keyword")]').getall()

# Descendant
page.xpath('//article//p/text()').getall()

# Conditional
page.xpath('//div[@class="product"]//span[@class="price"]/text()').getall()
```

## Selector Chaining

Apply selectors to sub-elements:

```python
# Get all product cards, then extract fields from each
products = page.css('.product-card')
for product in products:
    name  = product.css('.name::text').get()
    price = product.css('.price::text').get()
    url   = product.css('a::attr(href)').get()
    print(name, price, url)
```

## Text Extraction Methods

```python
# Full page text (strips scripts/styles)
page.get_all_text(ignore_tags=('script', 'style', 'nav', 'footer'))

# Single element text (normalized whitespace)
element = page.css('.article-body').get()

# Regex extraction
page.css('.price::text').re(r'\d+\.\d+')         # extract numbers
page.css('.date::text').re_first(r'\d{4}-\d{2}-\d{2}')  # first match
```

## Adaptive Selectors (site redesign protection)

```python
# First run: save fingerprint of found elements
items = page.css('.product-item', auto_save=True)

# Later runs: if CSS breaks, find by fingerprint
items = page.css('.product-item', adaptive=True)

# Force adaptive (skip CSS attempt)
items = page.css('.product-item', auto_match=True)
```

## Offline HTML Parsing

Parse raw HTML without fetching:

```python
from scrapling.parser import Selector

html = "<html><body><h1>Hello</h1></body></html>"
page = Selector(html)
title = page.css('h1::text').get()  # "Hello"
```

Useful for processing already-fetched HTML strings.

## Common Patterns

```python
# Product listing
products = []
for card in page.css('.product-card'):
    products.append({
        'title':  card.css('h2::text').get(''),
        'price':  card.css('.price::text').get(''),
        'url':    card.css('a::attr(href)').get(''),
        'image':  card.css('img::attr(src)').get(''),
    })

# Pagination
next_page = page.css('.pagination .next a::attr(href)').get()

# Table data
rows = []
for tr in page.css('table tbody tr'):
    cols = tr.css('td::text').getall()
    rows.append(cols)

# Article content (clean text)
paragraphs = page.css('article p::text').getall()
content = '\n\n'.join(p.strip() for p in paragraphs if p.strip())
```
