# Import necessary modules from Django REST Framework
from rest_framework.permissions import IsAuthenticated  # Ensures only authenticated users can access the view
from rest_framework.response import Response  # Used to return HTTP responses
from rest_framework.views import APIView  # Base class for creating API views
from rest_framework import status  # Provides HTTP status codes
from rest_framework.throttling import UserRateThrottle  # Rate limiting to prevent abuse
from rest_framework_simplejwt.authentication import JWTAuthentication  # JWT-based authentication for secure token hand
from viewer.models import Task  # Import the Task model
from .serializers import TaskSerializer  # Import the TaskSerializer for serializing/deserializing Task objects


class TaskCreateView(APIView):
    """
    View for creating a new task.
    Only authenticated users can access this view.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    authentication_classes = [JWTAuthentication]  # Use JWT authentication for secure token handling
    throttle_classes = [UserRateThrottle]  # Apply rate limiting to prevent abuse

    def post(self, request, *args, **kwargs):
        """
        Handle the creation of a task.
        - Validate the incoming data using the TaskSerializer.
        - Save the task if the data is valid.
        - Return the created task data or validation errors.
        """
        # Pass the request context to the serializer for additional context (e.g., user information)
        serializer = TaskSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Save the task using the serializer's `create` method
            serializer.save()
            # Return the serialized task data with a 201 Created status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the data is invalid, return the validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTasksView(APIView):
    """
    View for retrieving, updating, and deleting tasks for the logged-in user.
    Only authenticated users can access this view.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    authentication_classes = [JWTAuthentication]  # Use JWT authentication for secure token handling
    throttle_classes = [UserRateThrottle]  # Apply rate limiting to prevent abuse

    def get(self, request):
        """
        Retrieve all tasks owned by the logged-in user.
        - Filter tasks by the `owner` field (which should be the logged-in user).
        - Serialize the tasks and return them in the response.
        """
        # Fetch tasks owned by the logged-in user
        tasks = Task.objects.filter(owner=request.user)
        # Serialize the tasks (many=True indicates a list of tasks)
        serializer = TaskSerializer(tasks, many=True)
        # Return the serialized task data with a 200 OK status
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Allow partial updates to a task.
        - Fetch the task by ID and ensure it belongs to the logged-in user.
        - Validate the incoming data and update the task if valid.
        - Return the updated task data or validation errors.
        """
        # Fetch the task by ID and ensure it belongs to the logged-in user
        task = Task.objects.filter(id=pk, owner=request.user).first()

        if not task:
            # If the task is not found or does not belong to the user, return a 404 Not Found error
            return Response({"error": "Task not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the task with the incoming data, allowing partial updates
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            # Save the updated task
            serializer.save()
            # Return the updated task data with a 200 OK status
            return Response(serializer.data)

        # If the data is invalid, return the validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Allow full updates to a task.
        - Fetch the task by ID and ensure it belongs to the logged-in user.
        - Validate the incoming data and update the task if valid.
        - Return the updated task data or validation errors.
        """
        # Fetch the task by ID and ensure it belongs to the logged-in user
        task = Task.objects.filter(id=pk, owner=request.user).first()

        if not task:
            # If the task is not found or does not belong to the user, return a 404 Not Found error
            return Response({"error": "Task not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the task with the incoming data for a full update
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            # Save the updated task
            serializer.save()
            # Return the updated task data with a 200 OK status
            return Response(serializer.data)

        # If the data is invalid, return the validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a task.
        - Fetch the task by ID and ensure it belongs to the logged-in user.
        - Delete the task if found and authorized.
        - Return a success message or an error if the task is not found.
        """
        # Fetch the task by ID and ensure it belongs to the logged-in user
        task = Task.objects.filter(id=pk, owner=request.user).first()

        if not task:
            # If the task is not found or does not belong to the user, return a 404 Not Found error
            return Response({"error": "Task not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the task
        task.delete()
        # Return a success message with a 204 No Content status
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)