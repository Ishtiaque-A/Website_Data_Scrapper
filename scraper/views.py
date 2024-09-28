from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ScrapedData
from .serializers import ScrapedDataSerializer
from .utils import scrape_title
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_description(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    try:
        title = scrape_title(url)
        description = driver.find_element(By.XPATH, '//meta[@name="description"]').get_attribute('content')
    except Exception as e:
        title = None
        description = None
    
    driver.quit()
    return title, description

@api_view(['POST'])
def submit_link(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the URL is already scraped
    if ScrapedData.objects.filter(url=url).exists():
        return Response({'message': 'URL already exists.'}, status=status.HTTP_200_OK)

    # Scrape the data
    title, description = scrape_description(url)
    if title is None:
        return Response({'error': 'Failed to scrape the URL.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Save to the database
    scraped_data = ScrapedData.objects.create(url=url, title=title, description=description)
    serializer = ScrapedDataSerializer(scraped_data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_scraped_data(request):
    data = ScrapedData.objects.all().order_by('-scraped_at')
    serializer = ScrapedDataSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
