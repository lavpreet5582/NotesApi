from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Note
from .serializers import UserSerializer, NoteSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def user_signup(request):
    """
    A view that handles user signup using POST method.
    """

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registration successful"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    """
    This function handles user login by authenticating the username and password provided in the request data.
    It accepts a POST request and returns a token if the authentication is successful, or an error message if the credentials are invalid.
    """

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def create_note(request):
    """
    Create a note using the data from the request. 
    """

    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Note created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_note(request, id):
    """
    Function to handle GET request for retrieving a note by its ID.
    
    Parameters:
        request (Request): The request object containing metadata about the request.
        id (int): The unique identifier of the note to retrieve.
        
    Returns:
        Response: The HTTP response containing the requested note data or an error message.
    """

    note = Note.objects.filter(id=id, user=request.user).first()
    if note:
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "Note not found or you don't have permission to access"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def share_note(request):
    """
    API view for sharing a note. Accepts a POST request and expects 'note_id' and 'users' in the request data.
    Returns a response indicating success or failure of the note sharing process.
    """

    note_id = request.data.get('note_id')
    users = request.data.get('users')
    note = Note.objects.filter(id=note_id, user=request.user).first()
    if note:
        note.shared_users.add(*users)
        return Response({"message": "Note shared successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Note not found or you don't have permission to share"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_note(request, id):
    """
    Updates a note based on the provided ID. 
    If the requesting user is the owner of the note or one of the shared users, the note's content is updated with the new data provided in the request, and the updated note is saved with the current timestamp. 
    If the requesting user does not have permission to update the note, an error message is returned.
    """

    note = get_object_or_404(Note, pk=id)
    if request.user == note.user or request.user in note.shared_users.all():
        note.content += request.data.get('content')
        note.updated_at = datetime.now()
        note.save()
        return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You don't have permission to update this note"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def note_version_history(request, id):
    """
    Retrieve the version history of a note.

    Parameters:
        request (Request): The request object.
        id (int): The ID of the note.

    Returns:
        Response: The version history data with HTTP status.
    """

    note = Note.objects.filter(id=id, user=request.user).first()
    if note:
        versions = note.noteversion_set.all()
        data = [{"timestamp": version.created_at, "user": version.user.username, "content": version.content} for version in versions]
        return Response(data, status=status.HTTP_200_OK)
    return Response({"error": "Note not found or you don't have permission to access"}, status=status.HTTP_404_NOT_FOUND)
