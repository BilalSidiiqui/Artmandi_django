from .models import Listing, Comment, User, Bid, Watchlist
from rest_framework import serializers
from rest_framework import permissions


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Passwords Must Match',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirmPassword = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Passwords Must Match',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class ListingSerializer(serializers.ModelSerializer):
    winner_username = serializers.CharField(
        source="bider.user.username", read_only=True)
    winner_bidprice = serializers.CharField(
        source="bider.bid_price", read_only=True)

    class Meta:
        PRODUCT_CHOICES = (
            ('E', "ELECTRONICS"),
            ('H', "HOME"),
            ('T', "TOY"),
            ('E', "EDUCATION")
        )

        category = serializers.ChoiceField(choices=PRODUCT_CHOICES)
        model = Listing
        fields = ["id", 'title', 'description', 'image', 'category', 'start_price', 'created_by',
                  "created_at", "end_date", "completed", "winner_username", "winner_bidprice"]

        def create(self, validated_data):
            request = self.context.get('request')
            listing = Listing(
                title=validated_data['title'],
                description=validated_data['description'],
                image=request.FILES.get('image', default=''),
                start_price=validated_data['start_price'],
                created_by=validated_data['created_by'],
                created_at=validated_data['created_at'],
                end_date=validated_data['end_date'],
                completed=validated_data['completed'],
                winner_username=validated_data['winner_username'],
                winner_bidprice=validated_data['winner_bidprice'],
            )
            listing.save()
            return listing


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["listing", "user", 'comment', "username"]


class BidSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Bid
        fields = ['listing', "user", 'bid_price', 'username']


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["listing", "user"]
