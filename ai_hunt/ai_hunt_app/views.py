# views.py

import os
import requests
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Tool, Category, Type, Hashtag
from .serializers import ToolSerializer, CategorySerializer, TypeSerializer, HashtagSerializer, SubscriberSerializer

from .utils import download_and_save_image  
from django.core.mail import send_mail
from .models import Subscriber

@api_view(['POST'])
def subscribe_user(request):
    serializer = SubscriberSerializer(data=request.data)
    print("Received data for subscription:", request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        message = "Thank you for subscribing to our service!"

        try:
            # Send confirmation email
            send_mail(
                subject="Subscription Confirmation",
                message=message,
                from_email="your_email@example.com",  # Use your SMTP configured sender
                recipient_list=[email],
                fail_silently=False,
            )

            # Save to DB with message
            Subscriber.objects.create(email=email, message=message)

            return Response(
                {"message": "An email has been sent to your address and you are successfully subscribed."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all().order_by('rank_in_category')
    serializer_class = ToolSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Tool.objects.all().order_by('rank_in_category')
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        
        # Filter by type
        type_id = self.request.query_params.get('type', None)
        if type_id is not None:
            queryset = queryset.filter(type__id=type_id)
        
        # Filter by hashtag
        hashtag = self.request.query_params.get('hashtag', None)
        if hashtag is not None:
            queryset = queryset.filter(hashtags__id=hashtag)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset

    def _delete_file_from_instance(self, url_field_value):
        """
        Given a stored URL (e.g. "http://.../media/tools/images/abc.png"),
        strip out MEDIA_URL and delete the corresponding file from MEDIA_ROOT.
        """
        if not url_field_value:
            return

        # Parse the URL to get the path part ("/media/tools/images/abc.png")
        try:
            parsed = urlparse(url_field_value)
            relative_path = parsed.path
        except Exception:
            relative_path = url_field_value

        media_url = settings.MEDIA_URL  # e.g. "/media/"
        if relative_path.startswith(media_url):
            # Remove leading slash and MEDIA_URL prefix
            file_relative = relative_path.replace(media_url, "").lstrip("/")
            file_path = os.path.join(settings.MEDIA_ROOT, file_relative)
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

    def create(self, request, *args, **kwargs):
        """
        On POST: if `image_url` or `logo_url` is provided as an external URL,
        download the image, save it under MEDIA_ROOT/tools/images/ or tools/logos/,
        then replace the field with the new absolute media URL before saving.
        """
        data = request.data.copy()
        image_url_raw = data.get('image_url')
        logo_url_raw = data.get('logo_url')

        if image_url_raw:
            saved_image_rel = download_and_save_image(image_url_raw, 'tools/images/')
            if saved_image_rel:
                data['image_url'] = request.build_absolute_uri(saved_image_rel)

        if logo_url_raw:
            saved_logo_rel = download_and_save_image(logo_url_raw, 'tools/logos/')
            if saved_logo_rel:
                data['logo_url'] = request.build_absolute_uri(saved_logo_rel)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        On PUT: if a new `image_url` or `logo_url` is provided, delete the old file,
        download the new one, save it, and update the field. Then update other fields.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        new_image_url = data.get('image_url')
        new_logo_url = data.get('logo_url')

        if new_image_url:
            # Delete the old image file
            self._delete_file_from_instance(instance.image_url)
            # Download & save the new image
            saved_image_rel = download_and_save_image(new_image_url, 'tools/images/')
            if saved_image_rel:
                data['image_url'] = request.build_absolute_uri(saved_image_rel)

        if new_logo_url:
            self._delete_file_from_instance(instance.logo_url)
            saved_logo_rel = download_and_save_image(new_logo_url, 'tools/logos/')
            if saved_logo_rel:
                data['logo_url'] = request.build_absolute_uri(saved_logo_rel)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        On PATCH: same logic as update() but only modifies provided fields.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        On DELETE: remove both `image_url` and `logo_url` files from disk,
        then delete the database record.
        """
        instance = self.get_object()

        # Delete related files first
        self._delete_file_from_instance(instance.image_url)
        self._delete_file_from_instance(instance.logo_url)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
