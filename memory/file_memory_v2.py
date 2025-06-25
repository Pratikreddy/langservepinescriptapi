import json
import os
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

class FileMemoryStoreV2:
    def __init__(self, storage_path: str = "./storage/chat"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        print(f"[FileMemoryV2] Initialized at: {self.storage_path.absolute()}")
    
    def _get_user_dir(self, user_uuid: str) -> Path:
        """Get user's directory, create if doesn't exist"""
        user_dir = self.storage_path / user_uuid
        user_dir.mkdir(exist_ok=True)
        return user_dir
    
    def _get_conversation_file(self, user_uuid: str, conversation_id: str) -> Path:
        """Get conversation file path"""
        user_dir = self._get_user_dir(user_uuid)
        return user_dir / f"{conversation_id}.json"
    
    def create_conversation(self, user_uuid: str, thread_name: str = None) -> str:
        """Create a new conversation and return its ID"""
        conversation_id = str(uuid.uuid4())
        
        # Generate default name if none provided
        if not thread_name:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            thread_name = f"Chat - {timestamp}"
        
        # Create initial conversation data
        data = {
            'conversation_id': conversation_id,
            'user_uuid': user_uuid,
            'thread_name': thread_name,
            'messages': [],
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Save to file
        file_path = self._get_conversation_file(user_uuid, conversation_id)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[FileMemoryV2] Created conversation '{thread_name}' for user {user_uuid[:8]}...")
        return conversation_id
    
    def list_conversations(self, user_uuid: str) -> List[Dict]:
        """List all conversations for a user with metadata"""
        user_dir = self._get_user_dir(user_uuid)
        conversations = []
        
        for file_path in user_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Extract summary info
                message_count = len(data.get('messages', []))
                last_message = ""
                last_updated = data.get('updated_at', data.get('created_at', ''))
                
                if message_count > 0:
                    last_msg = data['messages'][-1]
                    last_message = last_msg.get('content', '')[:100] + "..." if len(last_msg.get('content', '')) > 100 else last_msg.get('content', '')
                
                conversations.append({
                    'conversation_id': data.get('conversation_id', file_path.stem),
                    'thread_name': data.get('thread_name', f"Chat {file_path.stem}"),
                    'message_count': message_count,
                    'last_message': last_message,
                    'created_at': data.get('created_at', ''),
                    'updated_at': last_updated
                })
                
            except Exception as e:
                print(f"[FileMemoryV2] Error reading {file_path}: {e}")
        
        # Sort by last updated (newest first)
        conversations.sort(key=lambda x: x['updated_at'], reverse=True)
        print(f"[FileMemoryV2] Found {len(conversations)} conversations for user {user_uuid[:8]}...")
        
        return conversations
    
    def load_conversation(self, user_uuid: str, conversation_id: str) -> Optional[Dict]:
        """Load a specific conversation"""
        file_path = self._get_conversation_file(user_uuid, conversation_id)
        
        if not file_path.exists():
            print(f"[FileMemoryV2] No conversation found: {conversation_id}")
            return None
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(f"[FileMemoryV2] Loaded conversation '{data.get('thread_name', conversation_id)}' with {len(data.get('messages', []))} messages")
            return data
        except Exception as e:
            print(f"[FileMemoryV2] Error loading conversation: {e}")
            return None
    
    def save_conversation(self, user_uuid: str, conversation_id: str, data: Dict) -> bool:
        """Save conversation data"""
        file_path = self._get_conversation_file(user_uuid, conversation_id)
        
        try:
            # Ensure directory exists
            file_path.parent.mkdir(exist_ok=True)
            
            # Update timestamp
            data['updated_at'] = datetime.utcnow().isoformat()
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"[FileMemoryV2] Saved conversation to: {file_path}")
            return True
        except Exception as e:
            print(f"[FileMemoryV2] Error saving conversation: {e}")
            return False
    
    def append_message(self, user_uuid: str, conversation_id: str, message: Dict) -> bool:
        """Append a message to a conversation"""
        # Load existing conversation
        data = self.load_conversation(user_uuid, conversation_id)
        
        if not data:
            print(f"[FileMemoryV2] Conversation {conversation_id} not found, cannot append message")
            return False
        
        # Append message
        data['messages'].append(message)
        
        # Save updated conversation
        success = self.save_conversation(user_uuid, conversation_id, data)
        
        if success:
            print(f"[FileMemoryV2] Appended message. Total: {len(data['messages'])} messages")
        
        return success
    
    def update_thread_name(self, user_uuid: str, conversation_id: str, new_name: str) -> bool:
        """Update the name of a conversation thread"""
        data = self.load_conversation(user_uuid, conversation_id)
        
        if not data:
            return False
        
        data['thread_name'] = new_name
        return self.save_conversation(user_uuid, conversation_id, data)
    
    def delete_conversation(self, user_uuid: str, conversation_id: str) -> bool:
        """Delete a conversation"""
        file_path = self._get_conversation_file(user_uuid, conversation_id)
        
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"[FileMemoryV2] Deleted conversation: {conversation_id}")
                return True
            except Exception as e:
                print(f"[FileMemoryV2] Error deleting conversation: {e}")
                return False
        
        return False
    
    def get_user_stats(self, user_uuid: str) -> Dict:
        """Get usage statistics for a user"""
        conversations = self.list_conversations(user_uuid)
        
        total_messages = sum(conv['message_count'] for conv in conversations)
        
        return {
            'user_uuid': user_uuid,
            'total_conversations': len(conversations),
            'total_messages': total_messages,
            'most_recent_activity': conversations[0]['updated_at'] if conversations else None
        }