# Import necessary modules from Django REST Framework and Django's auth models
from rest_framework import serializers
from django.contrib.auth.models import User


# Define a serializer class for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    # Add an additional field `password2` to confirm the password during registration
    # `write_only=True` ensures this field is only used for input and not included in the output
    password2 = serializers.CharField(write_only=True)

    # Meta class to define metadata for the serializer
    class Meta:
        # Specify the Django model to be used (in this case, the built-in User model)
        model = User
        # Define the fields to be included in the serializer
        # These fields will be used for both input and output (except `password2`, which is write-only)
        fields = ['username', 'email', 'password', 'password2']

    # Custom validation method for the `username` field
    def validate_username(self, value):
        """
        Check if the username already exists in the database.
        If it exists, raise a validation error to prevent duplicate usernames.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        # If the username is unique, return the value
        return value

    # Custom validation method for the entire serializer
    def validate(self, data):
        """
        Validate that the `password` and `password2` fields match.
        If they don't match, raise a validation error.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        # If the passwords match, return the validated data
        return data

    # Method to create a new user instance
    def create(self, validated_data):
        """
        Create a new User instance using the validated data.
        The `create_user` method from Django's User model is used to handle password hashing.
        """
        # Create a new user with the provided username, email, and password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        # Return the newly created user instance
        return user
