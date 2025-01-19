import os
import sys
import logging

# Try to import pysqlite3 and replace sqlite3 if possible
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    print("Warning: Could not import pysqlite3. Using system sqlite3.")

import pandas as pd
import uuid

class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        """
        Initialize portfolio with required columns
        """
        try:
            if pd.os.path.exists(file_path):
                self.df = pd.read_csv(file_path)
            else:
                self.df = pd.DataFrame(columns=['id', 'name', 'description', 'skills', 'link'])
        except Exception as e:
            logging.error(f"Error initializing portfolio: {e}")
            self.df = pd.DataFrame(columns=['id', 'name', 'description', 'skills', 'link'])

    def add_project(self, project_name, description, skills, link=None):
        """
        Add a new project to the portfolio
        
        Args:
            project_name (str): Name of the project
            description (str): Project description
            skills (list): List of skills used in the project
            link (str, optional): Project link
        """
        project_id = str(uuid.uuid4())
        new_project = {
            'id': project_id,
            'name': project_name,
            'description': description,
            'skills': ', '.join(skills),
            'link': link
        }
        
        self.df = self.df._append(new_project, ignore_index=True)
        self.save()
        return project_id

    def get_projects_by_skill(self, skill):
        """
        Retrieve projects that match a specific skill
        
        Args:
            skill (str): Skill to search for
        
        Returns:
            DataFrame: Projects matching the skill
        """
        return self.df[self.df['skills'].str.contains(skill, case=False, na=False)]

    def query_links(self, skills):
        """
        Retrieve project links that match the specified skills.
        
        Args:
            skills (list): List of skills to search for.
        
        Returns:
            list: Project links that match the skills.
        """
        if self.df.empty or 'skills' not in self.df.columns:
            return []
            
        links = []
        for _, row in self.df.iterrows():
            if pd.isna(row['skills']) or pd.isna(row['link']):
                continue
            row_skills = str(row['skills']).lower().split(', ')
            if any(skill.lower() in row_skills for skill in skills):
                if row['link'] and not pd.isna(row['link']):
                    links.append(row['link'])
        return links

    def save(self, file_path="my_portfolio.csv"):
        """
        Save portfolio to CSV
        
        Args:
            file_path (str): Path to save the CSV
        """
        try:
            self.df.to_csv(file_path, index=False)
        except Exception as e:
            logging.error(f"Error saving portfolio: {e}")

    def load_portfolio(self, file_path="my_portfolio.csv"):
        """
        Load portfolio from a CSV file
        
        Args:
            file_path (str): Path to the CSV file to load
        
        Returns:
            DataFrame: Loaded portfolio projects
        """
        try:
            self.df = pd.read_csv(file_path)
            return self.df
        except FileNotFoundError:
            logging.warning(f"Portfolio file {file_path} not found. Creating an empty portfolio.")
            self.df = pd.DataFrame(columns=['id', 'name', 'description', 'skills', 'link'])
            return self.df
        except Exception as e:
            logging.error(f"Error loading portfolio: {e}")
            self.df = pd.DataFrame(columns=['id', 'name', 'description', 'skills', 'link'])
            return self.df

    def __len__(self):
        """
        Get number of projects in portfolio
        
        Returns:
            int: Number of projects
        """
        return len(self.df)

    def display(self):
        """
        Display portfolio projects
        
        Returns:
            DataFrame: Portfolio projects
        """
        return self.df
