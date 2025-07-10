import requests
import logging
from django.conf import settings
from django.utils import timezone
from .models import ChatSession, ChatMessage

logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    def create_chat_session(user=None):
        """Create a new chat session"""
        return ChatSession.objects.create(user=user)
    
    @staticmethod
    def save_user_message(session, message):
        """Save a user message to the session"""
        return ChatMessage.objects.create(
            session=session,
            sender='user',
            content=message
        )
    
    @staticmethod
    def save_bot_message(session, message):
        """Save a bot message to the session"""
        return ChatMessage.objects.create(
            session=session,
            sender='bot',
            content=message
        )
    
    @staticmethod
    def end_session(session):
        """End a chat session"""
        session.end_time = timezone.now()
        session.save()
    
    @staticmethod
    def call_openrouter_api(message):
        """Call OpenRouter API to get bot response"""
        try:
            api_key = settings.OPENROUTER_API_KEY
            api_url = settings.OPENROUTER_API_URL
            
            if not api_key or not api_url:
                raise Exception('OpenRouter API key or URL is not configured')
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            request_body = {
                "model": "deepseek/deepseek-r1-0528:free",
                "messages": [
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(api_url, headers=headers, json=request_body)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f'OpenRouter API error: {response.text}')
                
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {str(e)}")
            raise e
    
    @staticmethod
    def process_chat_message(message, user=None):
        """Process a chat message and return bot response"""
        try:
            # Create a new chat session
            session = ChatService.create_chat_session(user)
            
            # Save user message
            ChatService.save_user_message(session, message)
            
            # Get bot response from OpenRouter
            bot_response = ChatService.call_openrouter_api(message)
            
            # Save bot response
            bot_message = ChatService.save_bot_message(session, bot_response)
            
            # End the session
            ChatService.end_session(session)
            
            return {
                'response': bot_response,
                'session_id': session.id,
                'message_id': bot_message.id,
                'session_ended': True
            }
            
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            raise e
    
    @staticmethod
    def get_chat_history(user=None):
        """Get chat history for a user"""
        try:
            if user:
                # For authenticated users, get their sessions
                sessions = ChatSession.objects.filter(user=user).order_by('-start_time')
            else:
                # For anonymous users, get sessions without user
                sessions = ChatSession.objects.filter(user__isnull=True).order_by('-start_time')
            
            history = []
            for session in sessions:
                messages = session.messages.all().order_by('timestamp')
                session_data = {
                    'session_id': session.id,
                    'start_time': session.start_time,
                    'end_time': session.end_time,
                    'messages': [
                        {
                            'id': msg.id,
                            'sender': msg.sender,
                            'content': msg.content,
                            'timestamp': msg.timestamp
                        } for msg in messages
                    ]
                }
                history.append(session_data)
            
            return {
                'history': history,
                'total_sessions': len(history)
            }
            
        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
            raise e
    
    @staticmethod
    def get_session_by_id(session_id, user=None):
        """Get a specific chat session by ID"""
        try:
            if user:
                session = ChatSession.objects.get(id=session_id, user=user)
            else:
                session = ChatSession.objects.get(id=session_id)
            
            messages = session.messages.all().order_by('timestamp')
            return {
                'session_id': session.id,
                'start_time': session.start_time,
                'end_time': session.end_time,
                'messages': [
                    {
                        'id': msg.id,
                        'sender': msg.sender,
                        'content': msg.content,
                        'timestamp': msg.timestamp
                    } for msg in messages
                ]
            }
            
        except ChatSession.DoesNotExist:
            raise Exception(f'Chat session with ID {session_id} not found')
        except Exception as e:
            logger.error(f"Error retrieving chat session: {str(e)}")
            raise e
    
    @staticmethod
    def delete_session(session_id, user=None):
        """Delete a specific chat session"""
        try:
            if user:
                session = ChatSession.objects.get(id=session_id, user=user)
            else:
                session = ChatSession.objects.get(id=session_id)
            
            session.delete()  # This will also delete all related messages due to CASCADE
            return True
            
        except ChatSession.DoesNotExist:
            raise Exception(f'Chat session with ID {session_id} not found')
        except Exception as e:
            logger.error(f"Error deleting chat session: {str(e)}")
            raise e
    
    @staticmethod
    def delete_all_history(user=None):
        """Delete all chat history for a user"""
        try:
            if user:
                deleted_count = ChatSession.objects.filter(user=user).count()
                ChatSession.objects.filter(user=user).delete()
            else:
                deleted_count = ChatSession.objects.filter(user__isnull=True).count()
                ChatSession.objects.filter(user__isnull=True).delete()
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error deleting chat history: {str(e)}")
            raise e 