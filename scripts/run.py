import requests
import csv
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import numpy as np

PERCENTAGE_REDUCTION = 8.5 # Reduce Wayback Machine total size by 8.5%
REDUCTION_BYTES_HTML = 800 # Subtract bytes from HTML Documents to account for Wayback Machine
REDUCTION_BYTES_STYLESHEETS = 800 # Subtract bytes from Stylesheets to account for Wayback Machine
REDUCTION_BYTES_SCRIPTS = 1500 # Subtract bytes Scripts to account for Wayback Machine

# Function to modify the Wayback Machine URL using the API by adding 'if_' to hide the Wayback Machine toolbar
def modify_wayback_machine_url(url):
  if "web.archive.org" in url:
    parts = url.split('/web/')
    timestamp = parts[1].split('/')[0]
    if 'if_' not in timestamp:
      new_url = url.replace(f"web/{timestamp}/", f"web/{timestamp}if_/")
      return new_url
  return url

# Function to get CO₂e and Ratings based on total page size using the Website Carbon API (https://api.websitecarbon.com)
def get_co2_emissions(total_size_bytes):
  api_url = f"https://api.websitecarbon.com/data?bytes={total_size_bytes}&green=0"
  response = requests.get(api_url)
  data = response.json()
  co2_grid_grams = data['statistics']['co2']['grid']['grams']
  rating = data.get('rating', 'N/A')
  return co2_grid_grams, rating

# Function to intercept responses added by Wayback Machine
def intercept_response(response, seen_urls, resource_sizes):
  if response.status != 200:
    return
  if response.url in seen_urls:
    return
  seen_urls.add(response.url)

  resource_domain = urlparse(response.url).netloc
  if "web-static.archive.org" in resource_domain:
    return

  content_type = response.headers.get("content-type", "").lower()
  content_length = response.headers.get("content-length")

  if content_length:
    size = int(content_length)
  else:
    try:
      body = response.body()
      size = len(body) if body else 0
    except Exception:
      return

  if "text/html" in content_type:
    resource_sizes["Document"] += size
  elif "application/javascript" in content_type or "application/x-javascript" in content_type:
    resource_sizes["Script"] += size
  elif "text/css" in content_type:
    resource_sizes["Stylesheet"] += size
  elif "image" in content_type:
    resource_sizes["Image"] += size
  elif "font" in content_type:
    resource_sizes["Font"] += size
  else:
    resource_sizes["Other"] += size

# Function to get full page size
def get_full_page_size(url, percentage_reduction=PERCENTAGE_REDUCTION, reduction_bytes_html=REDUCTION_BYTES_HTML, reduction_bytes_stylesheets=REDUCTION_BYTES_STYLESHEETS, reduction_bytes_scripts=REDUCTION_BYTES_SCRIPTS):
  url = modify_wayback_machine_url(url)

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    resource_sizes = {
      "Document": 0,
      "Script": 0,
      "Stylesheet": 0,
      "Image": 0,
      "Font": 0,
      "Other": 0
    }
    seen_urls = set()

    page.on("response", lambda response: intercept_response(response, seen_urls, resource_sizes))

    try:
      page.goto(url, wait_until="networkidle", timeout=60000)
    except Exception as e:
      print(f"Error during page load: {e}")
    finally:
      browser.close()

    total_size = sum(resource_sizes.values())

    # Apply percentage reduction for Wayback Machine URLs in the dataset
    if "web.archive.org" in url and percentage_reduction > 0:
      total_size *= (1 - percentage_reduction / 100)

      # Subtract bytes from Document, Script, and Stylesheet
      resource_sizes["Document"] = max(0, resource_sizes["Document"] - reduction_bytes_html)
      resource_sizes["Script"] = max(0, resource_sizes["Script"] - reduction_bytes_scripts)
      resource_sizes["Stylesheet"] = max(0, resource_sizes["Stylesheet"] - reduction_bytes_stylesheets)

  return total_size, resource_sizes

# Function to convert numeric rating to Website Carbon rating
def numeric_to_letter_rating(numeric_rating):
  rating_scale = {
    1: "A+", 2: "A", 3: "B", 4: "C", 5: "D", 6: "E", 7: "F"
  }
  return rating_scale.get(numeric_rating, "F")

# Function to display progress bar
def display_progress_bar(processed_pages, total_pages, page_url):
  progress = int((processed_pages / total_pages) * 40)
  bar = f"[{'█' * progress}{'-' * (40 - progress)}] {int((processed_pages / total_pages) * 100)}% Completed | Analysising '{page_url}' webpages" 
  print(bar, end='\r')

# Function to plot CO2 emissions chart
def plot_co2_chart(website_co2_data):
  websites = list(website_co2_data.keys())
  min_co2 = [website_co2_data[website]["min"] for website in websites]
  max_co2 = [website_co2_data[website]["max"] for website in websites]
  avg_co2 = [website_co2_data[website]["avg"] for website in websites]

  x = np.arange(len(websites))

  plt.figure(figsize=(10, 6))

  for i in range(len(websites)):
    if min_co2[i] is not None and max_co2[i] is not None and avg_co2[i] is not None:
      plt.plot([x[i], x[i]], [min_co2[i], max_co2[i]], color='black', lw=1)
      plt.plot(x[i], avg_co2[i], 's', markersize=10, color='grey', label='Avg')
      plt.plot(x[i], min_co2[i], 'o', markersize=4, color='black', label='Min/Max')
      plt.plot(x[i], max_co2[i], 'o', markersize=4, color='black')

  plt.xticks(x, websites, rotation=45, ha='right')
  plt.ylabel('CO₂e (grams)')
  plt.legend()
  plt.tight_layout()
  plt.show()

def main(dataset_file="./data/dataset.csv", output_file="./data/results.csv", percentage_reduction=PERCENTAGE_REDUCTION):
  with open(dataset_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    websites = [row for row in reader]

  results = []
  website_co2_data = {}

  total_websites = len(websites)
  processed_websites = 0

  # Loop over each website
  for website_data in websites:
    website = website_data["Website"]
    co2_sum = 0
    size_sum = 0
    ratings = []
    html_size_sum = 0
    html_percentage_sum = 0
    stylesheet_size_sum = 0
    stylesheet_percentage_sum = 0
    script_size_sum = 0
    script_percentage_sum = 0
    image_size_sum = 0
    image_percentage_sum = 0
    other_size_sum = 0
    other_percentage_sum = 0

    processed_pages = 0
    total_pages = 0

    min_co2 = float('inf')
    max_co2 = float('-inf')

    # Count the total number of pages for the website (Pages 1 to 20)
    for page_num in range(1, 21):
      if website_data.get(f"Page {page_num}"):
        total_pages += 1

    # Process the pages for this particular website
    for page_num in range(1, 21):
      page_url = website_data.get(f"Page {page_num}")
      if page_url:
        total_size, resource_sizes = get_full_page_size(page_url, percentage_reduction)
        co2e, rating = get_co2_emissions(total_size)
        
        min_co2 = min(min_co2, co2e)
        max_co2 = max(max_co2, co2e)

        # Breakdown of resource sizes
        html_size_kb = round(resource_sizes["Document"] / 1024, 2)
        stylesheet_size_kb = round(resource_sizes["Stylesheet"] / 1024, 2)
        script_size_kb = round(resource_sizes["Script"] / 1024, 2)
        image_size_kb = round(resource_sizes["Image"] / 1024, 2)
        other_size_kb = round(resource_sizes["Other"] / 1024, 2)

        # Percentage breakdowns
        total_kb = total_size / 1024
        html_percentage = round(html_size_kb / total_kb * 100, 1)
        stylesheet_percentage = round(stylesheet_size_kb / total_kb * 100, 1)
        script_percentage = round(script_size_kb / total_kb * 100, 1)
        image_percentage = round(image_size_kb / total_kb * 100, 1)
        other_percentage = round(other_size_kb / total_kb * 100, 1)

        # Add page data to results
        results.append([
          website,
          page_url,
          round(total_size / 1024, 2),
          round(co2e, 3),
          rating,
          html_size_kb,
          html_percentage,
          stylesheet_size_kb,
          stylesheet_percentage,
          script_size_kb,
          script_percentage,
          image_size_kb,
          image_percentage,
          other_size_kb,
          other_percentage
        ])

        # Aggregate values for averages
        co2_sum += co2e
        size_sum += total_size
        ratings.append(rating)
        html_size_sum += html_size_kb
        html_percentage_sum += html_percentage
        stylesheet_size_sum += stylesheet_size_kb
        stylesheet_percentage_sum += stylesheet_percentage
        script_size_sum += script_size_kb
        script_percentage_sum += script_percentage
        image_size_sum += image_size_kb
        image_percentage_sum += image_percentage
        other_size_sum += other_size_kb
        other_percentage_sum += other_percentage

        processed_pages += 1

    # Calculate averages for this website
    if processed_pages > 0:
      average_size = round(size_sum / processed_pages / 1024, 2)
      average_co2e = round(co2_sum / processed_pages, 3)

      average_html_size = round(html_size_sum / processed_pages, 2)
      average_html_percentage = round(html_percentage_sum / processed_pages, 1)
      average_stylesheet_size = round(stylesheet_size_sum / processed_pages, 2)
      average_stylesheet_percentage = round(stylesheet_percentage_sum / processed_pages, 1)
      average_script_size = round(script_size_sum / processed_pages, 2)
      average_script_percentage = round(script_percentage_sum / processed_pages, 1)
      average_image_size = round(image_size_sum / processed_pages, 2)
      average_image_percentage = round(image_percentage_sum / processed_pages, 1)
      average_other_size = round(other_size_sum / processed_pages, 2)
      average_other_percentage = round(other_percentage_sum / processed_pages, 1)

      average_numeric_rating = round(sum([{
        "A+": 1, "A": 2, "B": 3, "C": 4, "D": 5, "E": 6, "F": 7
      }.get(r, 0) for r in ratings]) / processed_pages)

      average_rating = numeric_to_letter_rating(average_numeric_rating)

      results.append([
        f"{website} Averages", "", average_size, average_co2e, average_rating,
        average_html_size, average_html_percentage, average_stylesheet_size, average_stylesheet_percentage,
        average_script_size, average_script_percentage, average_image_size, average_image_percentage,
        average_other_size, average_other_percentage
      ])
      
      results.append([])

      website_co2_data[website] = {
        "min": min_co2,
        "max": max_co2,
        "avg": average_co2e
      }

    processed_websites += 1
    display_progress_bar(processed_websites, total_websites, website)

  # Write to CSV file
  with open(output_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
      "Website", "Page URL", "Total Size (KB)", "CO₂e (grams)", "Rating", "HTML (KB)", "HTML (%)",
      "Stylesheets (KB)", "Stylesheets (%)", "Scripts (KB)", "Scripts (%)", "Images (KB)", "Images (%)",
      "Other (KB)", "Other (%)"
    ])
    for row in results:
      writer.writerow(row)

  print(f"Analysis complete. Results saved to {output_file}")

  # Plot the chart
  plot_co2_chart(website_co2_data)

main()