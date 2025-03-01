# Import necessary modules
from django.utils import timezone  # For handling timezone-aware dates
from rest_framework import serializers  # For creating serializers in Django REST Framework
from viewer.models import Task  # Import the Task model from the viewer app


# Define a serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Handles serialization (converting model instances to JSON) and
    deserialization (converting JSON to model instances).
    """

    class Meta:
        """
        Meta class to define metadata for the serializer.
        Specifies the model and fields to include in the serialization.
        """
        model = Task  # The model to serialize
        fields = ['id', 'title', 'owner', 'description', 'status', 'creation_date']  # Fields to include
        read_only_fields = ['owner', 'creation_date']  # Fields that cannot be edited by the user

    def create(self, validated_data):
        """
        Override the default create method to set the owner and creation date.
        This method is called when creating a new Task instance from validated data.
        """
        # Get the request object from the serializer context
        request = self.context.get('request')

        # Ensure the request and user are available
        if not request or not request.user:
            raise serializers.ValidationError("User must be authenticated to create a task.")

        # Set the creation date to the current date if not provided
        validated_data['creation_date'] = validated_data.get('creation_date', timezone.now().date())

        # Set the owner to the authenticated user
        validated_data['owner'] = request.user

        # Create and return the new Task instance using the validated data
        return Task.objects.create(**validated_data)