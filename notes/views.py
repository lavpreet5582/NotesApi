from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import Note, NoteVersion
from .serializers import NoteVersionSerializer, UserSerializer, NoteSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_note(request, id):
    """
    Function to handle GET request for retrieving a note by its ID.
    """
    note = get_object_or_404(Note, id=id, user=request.user)
    serializer = NoteSerializer(note)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    """
    API view for sharing a note.
    """
    note_id = request.data.get('note_id')
    users = request.data.get('users')
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.shared_users.add(*users)
    return Response({"message": "Note shared successfully"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, id):
    """
    Updates a note based on the provided ID.
    """
    note = get_object_or_404(Note, pk=id)
    if request.user == note.user or request.user in note.shared_users.all():
        note.content += request.data.get('content')
        note.updated_at = datetime.now()
        note.save()
        NoteVersion.objects.create(
            note=note,
            user=request.user,
            changes=request.data.get('content')
        )
        return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You don't have permission to update this note"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def note_version_history(request, id):
    """
    Retrieve the version history of a note.
    """
    note = get_object_or_404(Note, id=id, user=request.user)
    versions = note.noteversion_set.all()
    serializer = NoteVersionSerializer(versions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
