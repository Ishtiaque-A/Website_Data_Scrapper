# scraper/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ScrapedData
from .serializers import ScrapedDataSerializer
from .utils import scrape_title

@api_view(['POST'])
def submit_link(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the URL is already scraped
    if ScrapedData.objects.filter(url=url).exists():
        return Response({'message': 'URL already exists.'}, status=status.HTTP_200_OK)

    # Scrape the data
    title = scrape_title(url)
    if not title:
        return Response({'error': 'Failed to scrape the URL.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Save to the database
    scraped_data = ScrapedData.objects.create(url=url, title=title)
    serializer = ScrapedDataSerializer(scraped_data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_scraped_data(request):
    data = ScrapedData.objects.all().order_by('-scraped_at')
    serializer = ScrapedDataSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
