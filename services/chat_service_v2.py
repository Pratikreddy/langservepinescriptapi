from typing import Dict, List, Optional
import uuid
from datetime import datetime
from memory.file_memory_v2 import FileMemoryStoreV2
from llm_agent.agent_multi import run_pinescript_agent, clear_conversation_memory
import json

class ChatServiceV2:
    def __init__(self):
        # Use backend storage path, not frontend path
        self.memory_store = FileMemoryStoreV2(storage_path="./storage/chat")
    
    def create_new_conversation(self, user_uuid: str, thread_name: str = None) -> Dict:
        """Create a new conversation thread for a user"""
        try:
            conversation_id = self.memory_store.create_conversation(user_uuid, thread_name)
            
            return {
                'success': True,
                'conversation_id': conversation_id,
                'thread_name': thread_name or f"Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_user_conversations(self, user_uuid: str) -> Dict:
        """List all conversations for a user"""
        try:
            conversations = self.memory_store.list_conversations(user_uuid)
            
            return {
                'success': True,
                'conversations': conversations,
                'total': len(conversations)
            }
        except Exception as e:
            print(f"Error listing conversations: {e}")
            return {
                'success': False,
                'error': str(e),
                'conversations': []
            }
    
    def process_message(self, user_uuid: str, conversation_id: str, message: str) -> Dict:
        """Process a message in an existing conversation"""
        
        # Verify conversation exists
        conversation_data = self.memory_store.load_conversation(user_uuid, conversation_id)
        if not conversation_data:
            return {
                'success': False,
                'error': f'Conversation {conversation_id} not found for user {user_uuid[:8]}...'
            }
        
        # Save user message
        user_msg = {
            'role': 'user',
            'content': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        success = self.memory_store.append_message(user_uuid, conversation_id, user_msg)
        if not success:
            return {
                'success': False,
                'error': 'Failed to save user message'
            }
        
        try:
            # Call the PineScript trading agent
            raw_json, tokens, cost, _, _ = run_pinescript_agent(
                message, 
                use_multi=True
            )
            
            # Parse response
            parsed = json.loads(raw_json)
            answer = parsed.get("answer", "No response generated")
            
            # Save assistant response
            ai_msg = {
                'role': 'assistant',
                'content': answer,
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': parsed
            }
            
            success = self.memory_store.append_message(user_uuid, conversation_id, ai_msg)
            if not success:
                return {
                    'success': False,
                    'error': 'Failed to save assistant response'
                }
            
            return {
                'success': True,
                'response': ai_msg,
                'conversation_id': conversation_id,
                'thread_name': conversation_data.get('thread_name', 'Untitled'),
                'tokens': tokens,
                'cost': cost
            }
            
        except Exception as e:
            print(f"Error in chat service: {e}")
            
            # Save error as assistant message
            error_msg = {
                'role': 'assistant',
                'content': f"Sorry, I encountered an error: {str(e)}",
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': {'error': str(e)}
            }
            
            self.memory_store.append_message(user_uuid, conversation_id, error_msg)
            
            return {
                'success': False,
                'response': error_msg,
                'conversation_id': conversation_id,
                'thread_name': conversation_data.get('thread_name', 'Untitled'),
                'error': str(e),
                'tokens': 0,
                'cost': 0
            }
    
    def get_conversation(self, user_uuid: str, conversation_id: str) -> Dict:
        """Get a specific conversation"""
        try:
            conversation_data = self.memory_store.load_conversation(user_uuid, conversation_id)
            
            if not conversation_data:
                return {
                    'success': False,
                    'error': f'Conversation {conversation_id} not found'
                }
            
            return {
                'success': True,
                'conversation': conversation_data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_conversation_name(self, user_uuid: str, conversation_id: str, new_name: str) -> Dict:
        """Update the name of a conversation thread"""
        try:
            success = self.memory_store.update_thread_name(user_uuid, conversation_id, new_name)
            
            if success:
                return {
                    'success': True,
                    'message': f'Thread renamed to "{new_name}"'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to update thread name'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_conversation(self, user_uuid: str, conversation_id: str) -> Dict:
        """Delete a conversation"""
        try:
            success = self.memory_store.delete_conversation(user_uuid, conversation_id)
            
            if success:
                return {
                    'success': True,
                    'message': 'Conversation deleted'
                }
            else:
                return {
                    'success': False,
                    'error': 'Conversation not found or could not be deleted'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_stats(self, user_uuid: str) -> Dict:
        """Get user statistics"""
        try:
            stats = self.memory_store.get_user_stats(user_uuid)
            return {
                'success': True,
                'stats': stats
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }