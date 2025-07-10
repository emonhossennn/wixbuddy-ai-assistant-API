from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .services import ChatService
from .serializers import ChatRequestSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_api(request):
    """
    API endpoint for interacting with OpenRouter AI chatbot with history
    """
    try:
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid message format'}, status=status.HTTP_400_BAD_REQUEST)
        
        message = serializer.validated_data['message']
        user = request.user if request.user.is_authenticated else None
        
        # Process the chat message
        result = ChatService.process_chat_message(message, user)
        
        return Response(result)
        
    except Exception as e:
        return Response({'error': f'Error processing request: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def chat_history(request):
    """
    Get chat history for the current user (authenticated or anonymous)
    """
    try:
        user = request.user if request.user.is_authenticated else None
        result = ChatService.get_chat_history(user)
        return Response(result)
        
    except Exception as e:
        return Response({'error': f'Error retrieving chat history: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_chat_session(request, session_id):
    """
    Delete a specific chat session by session_id and all its messages
    """
    try:
        user = request.user if request.user.is_authenticated else None
        ChatService.delete_session(session_id, user)
        return Response({'message': f'Chat session {session_id} deleted successfully'})
        
    except Exception as e:
        return Response({'error': f'Error deleting chat session {session_id}: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_all_chat_history(request):
    """
    Delete all chat history for the current user (authenticated or anonymous)
    """
    try:
        user = request.user if request.user.is_authenticated else None
        deleted_count = ChatService.delete_all_history(user)
        
        return Response({
            'message': f'All chat history deleted successfully',
            'deleted_sessions': deleted_count
        })
        
    except Exception as e:
        return Response({'error': f'Error deleting chat history: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_chat_session(request, session_id):
    """
    Get a specific chat session by ID with all its messages
    """
    try:
        user = request.user if request.user.is_authenticated else None
        result = ChatService.get_session_by_id(session_id, user)
        return Response(result)
        
    except Exception as e:
        return Response({'error': f'Error retrieving chat session: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 