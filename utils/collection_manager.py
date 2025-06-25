# This file is disabled for PineScript trading assistant app
# All document/textbook search functionality has been removed

# import json
# import os
# from typing import List, Dict, Optional
# from pymilvus import connections, Collection, utility, db
# from pathlib import Path

# Configuration - DISABLED
# MILVUS_HOST = "127.0.0.1"
# MILVUS_PORT = "19530"
# DB_NAME = "documentdb"
# METADATA_COLLECTION = "pdf_metadata"

# Path to PDF ID mappings - DISABLED
# BASE_DIR = Path(__file__).parent.parent / "project"
# MAPPING_JSON = BASE_DIR / "pdf_id_mappings.json"

# DISABLED - Document search functionality removed
# class CollectionManager:
#     def __init__(self):
#         self.connect()
#         
#     def connect(self):
#         """Connect to Milvus"""
#         connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
#         db.using_database(DB_NAME)
    
#     def get_available_collections(self) -> List[Dict]:
#         """
#         Get all available collections with metadata
#         Returns list of dicts with collection info
#         """
#         collections = []
#         
#         # Get all collections
#         all_collections = utility.list_collections()
#         
#         # Filter out system collections
#         pdf_collections = [c for c in all_collections if c not in ['pdf_metadata']]
#         
#         # Load PDF mappings if available
#         pdf_mappings = {}
#         if MAPPING_JSON.exists():
#             with open(MAPPING_JSON, 'r') as f:
#                 pdf_mappings = json.load(f)
#         
#         # Get metadata for each collection
#         for collection_name in pdf_collections:
#             try:
#                 # Get collection stats
#                 collection = Collection(name=collection_name)
#                 collection.load()
#                 
#                 # Find original PDF name from mappings
#                 original_name = collection_name
#                 total_pages = 0
#                 
#                 # Search in mappings for matching collection name
#                 for main_id, mapping in pdf_mappings.items():
#                     # Check if this collection matches the PDF
#                     clean_name = self._clean_collection_name(mapping['original_name'])
#                     if clean_name == collection_name:
#                         original_name = mapping['original_name']
#                         # Calculate total pages from splits
#                         if mapping['splits']:
#                             last_split = mapping['splits'][-1]
#                             total_pages = last_split['page_end']
#                         break
#                 
#                 collections.append({
#                     'collection_name': collection_name,
#                     'display_name': original_name,
#                     'num_entities': collection.num_entities,
#                     'total_pages': total_pages,
#                     'description': f"{original_name} ({collection.num_entities} chunks)"
#                 })
#                 
#             except Exception as e:
#                 print(f"Error getting info for collection {collection_name}: {e}")
#                 collections.append({
#                     'collection_name': collection_name,
#                     'display_name': collection_name,
#                     'num_entities': 0,
#                     'total_pages': 0,
#                     'description': collection_name
#                 })
#         
#         return sorted(collections, key=lambda x: x['display_name'])
    
#     def _clean_collection_name(self, original_name: str) -> str:
#         """Convert original PDF name to collection name format"""
#         collection_name = ''.join(c if c.isalnum() else '_' for c in original_name.lower())
#         while '__' in collection_name:
#             collection_name = collection_name.replace('__', '_')
#         collection_name = collection_name.strip('_')
#         if collection_name and not collection_name[0].isalpha():
#             collection_name = 'pdf_' + collection_name
#         return collection_name or 'pdf_collection'
#     
#     def get_collection_info(self, collection_name: str) -> Optional[Dict]:
#         """Get detailed info about a specific collection"""
#         try:
#             collection = Collection(name=collection_name)
#             collection.load()
#             
#             # Get sample chunks to understand content
#             sample_results = collection.query(
#                 expr="id != ''",
#                 limit=5,
#                 output_fields=["id", "pdf_name", "page_number"]
#             )
#             
#             # Get page range
#             page_numbers = [r['page_number'] for r in sample_results if 'page_number' in r]
#             
#             return {
#                 'collection_name': collection_name,
#                 'num_entities': collection.num_entities,
#                 'sample_chunks': sample_results,
#                 'page_range': (min(page_numbers), max(page_numbers)) if page_numbers else (0, 0)
#             }
#         except Exception as e:
#             print(f"Error getting collection info: {e}")
#             return None
#     
#     def validate_collections(self, collection_names: List[str]) -> List[str]:
#         """Validate that collections exist and are accessible"""
#         valid_collections = []
#         all_collections = utility.list_collections()
#         
#         for name in collection_names:
#             if name in all_collections:
#                 try:
#                     collection = Collection(name=name)
#                     collection.load()
#                     valid_collections.append(name)
#                 except Exception as e:
#                     print(f"Collection {name} exists but couldn't load: {e}")
#             else:
#                 print(f"Collection {name} does not exist")
#         
#         return valid_collections

# DISABLED - Singleton instance
# _manager = None

# def get_collection_manager() -> CollectionManager:
#     """Get singleton instance of CollectionManager"""
#     global _manager
#     if _manager is None:
#         _manager = CollectionManager()
#     return _manager

# Placeholder function for compatibility
def get_collection_manager():
    """Disabled - Collection management removed for PineScript app"""
    raise NotImplementedError("Collection management disabled for PineScript trading assistant")