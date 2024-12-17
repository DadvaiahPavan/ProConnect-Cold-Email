import os
import sys
import sqlite3

# Attempt to use pysqlite3 for newer SQLite version
try:
    import pysqlite3 as sqlite3
except ImportError:
    pass

# Check SQLite version
sqlite_version = sqlite3.sqlite_version_info
print(f"SQLite Version: {sqlite3.sqlite_version}")

if sqlite_version < (3, 35, 0):
    print("Warning: SQLite version is lower than recommended")

import pandas as pd
import chromadb
import uuid

# Optional fallback for Chroma if SQLite is problematic
try:
    client = chromadb.Client()
except Exception as e:
    print(f"Chroma initialization error: {e}")
    client = None


class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        """Load portfolio data into ChromaDB if not already loaded."""
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        """
        Query portfolio links based on skills.
        
        Args:
            skills (list): List of skills to match against portfolio
        
        Returns:
            list: Relevant portfolio project links
        """
        # Handle case where skills might be empty or None
        if not skills:
            # Return all links if no specific skills provided
            return self.data['Links'].tolist()
        
        try:
            # Ensure skills is a list
            if isinstance(skills, str):
                skills = [skills]
            
            # Query ChromaDB
            query_result = self.collection.query(
                query_texts=skills, 
                n_results=3  # Limit to top 3 matches
            )
            
            # Extract links from metadata
            links = []
            metadata_lists = query_result.get('metadatas', [])
            
            # Flatten and extract unique links
            for metadata_sublist in metadata_lists:
                if metadata_sublist:
                    for metadata in metadata_sublist:
                        if isinstance(metadata, dict) and 'links' in metadata:
                            links.append(metadata['links'])
            
            # If no links found, return all links
            return links if links else self.data['Links'].tolist()
        
        except Exception as e:
            print(f"Error in query_links: {e}")
            # Fallback to all links if query fails
            return self.data['Links'].tolist()
