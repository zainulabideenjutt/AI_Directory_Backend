from rest_framework import serializers
from .models import Tool, Category, Type, Hashtag,Subscriber


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'message']
        read_only_fields = ['message']



class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class ToolSerializer(serializers.ModelSerializer):
    # Read-only nested relationships
    category = CategorySerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)

    # Write-only foreign key fields
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), source='type', write_only=True
    )
    hashtag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Hashtag.objects.all(), source='hashtags', write_only=True
    )

    class Meta:
        model = Tool
        fields = [
            'id', 'name', 'image_url', 'logo_url', 'description',
            'upvote_count', 'trend_count', 'rating', 'is_verified', 'url',
            'rank_in_category', 'category', 'type', 'hashtags',
            'category_id', 'type_id', 'hashtag_ids',
            'date_added', 'date_updated'
        ]
