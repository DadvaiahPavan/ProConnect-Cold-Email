import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import logging

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=os.getenv("GROQ_API_KEY"), 
            model_name="llama-3.1-70b-versatile"
        )

    def extract_skills(self, context):
        """
        Extract skills from the given context.
        
        Args:
            context (str): Context containing potential skills
        
        Returns:
            list: Extracted skills or empty list
        """
        skill_prompt = PromptTemplate(
            input_variables=["context"],
            template="""
            From the following context, extract a list of technical skills, 
            programming languages, tools, and technologies. Return them as a comma-separated list:
            
            Context: {context}
            
            Skills:"""
        )
        
        try:
            skills_text = self.llm.invoke(skill_prompt.format(context=context)).content
            # Convert the skills text into a list, clean up any whitespace
            skills_list = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
            return skills_list
        except Exception as e:
            logging.error(f"Error extracting skills: {e}")
            return []

    def write_personalized_mail(self, context, job_description, links, tone='Professional', sender_name=None):
        """
        Generate a personalized email based on comprehensive context.
        
        Args:
            context (str): Comprehensive context about the job and sender
            job_description (str): Detailed job description
            links (list): Relevant portfolio project links
            tone (str, optional): Email tone. Defaults to 'Professional'.
            sender_name (str, optional): Name to be used in the signature
        
        Returns:
            str: Generated personalized email
        """
        # Ensure links is a list, default to empty list if None
        links = links or []
        
        # Define tone-specific instructions
        tone_instructions = {
            'Professional': "Maintain a formal, polished, and corporate communication style.",
            'Friendly': "Use a warm, conversational tone that feels personal and approachable.",
            'Formal': "Adopt a highly structured, precise, and traditional business communication approach.",
            'Casual': "Write in a relaxed, modern style that feels natural and engaging."
        }
        
        # Default to Professional if tone is not recognized
        tone_instruction = tone_instructions.get(tone, tone_instructions['Professional'])
        
        # Prepare sender name for signature
        signature = f"\nBest regards,\n{sender_name.strip()}" if sender_name else "\nBest regards,"
        
        prompt_email = PromptTemplate(
            input_variables=["context", "job_description", "links", "tone_instruction", "signature"],
            template="""
            You are a professional email writer helping a job seeker craft a personalized cold email.

            ### COMMUNICATION STYLE GUIDANCE
            {tone_instruction}

            ### COMPREHENSIVE CONTEXT
            {context}

            ### JOB DESCRIPTION
            {job_description}

            ### RELEVANT PORTFOLIO LINKS
            {links}

            ### EMAIL GENERATION INSTRUCTIONS
            Craft a compelling, personalized cold email that:
            1. Directly addresses the recipient by name
            2. Clearly states the purpose of the email
            3. Demonstrates understanding of the company and role
            4. Highlights 2-3 most relevant skills/experiences
            5. Shows genuine interest and value proposition
            6. Maintains the specified communication tone
            7. Keeps the email concise (under 250 words)

            ### SIGNATURE REQUIREMENTS
            - STRICTLY USE ONLY THE PROVIDED SIGNATURE
            - DO NOT ADD ANY ADDITIONAL TEXT AFTER THE SIGNATURE
            - NO CONTACT INFORMATION ALLOWED
            - EXACTLY MATCH THE PROVIDED SIGNATURE FORMAT

            ### OUTPUT FORMAT
            - No preamble
            - Personalize based on the provided context
            - Adhere to the specified communication style
            - END THE EMAIL WITH EXACTLY: {signature}

            ### EMAIL CONTENT:
            """
        )
        
        # Create the email generation chain
        email_chain = prompt_email | self.llm
        
        try:
            # Generate the email with the specified tone
            email = email_chain.invoke({
                "context": context, 
                "job_description": job_description, 
                "links": str(links),
                "tone_instruction": tone_instruction,
                "signature": signature
            })
            
            # Post-process to ensure only the signature is used
            email_parts = email.content.split("\nBest regards,")
            processed_email = email_parts[0] + signature
            
            return processed_email
        except Exception as e:
            print(f"Error generating email: {e}")
            return f"Error generating email: {e}"

    def extract_jobs(self, text):
        """
        Extract job details from text.
        
        Args:
            text (str): Text containing job information
        
        Returns:
            list: Extracted job details
        """
        job_extraction_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Extract key job details from the following text:
            {text}

            Return a JSON list of job details with keys:
            - title: Job title
            - skills: List of required skills
            - description: Brief job description
            """
        )
        
        job_chain = job_extraction_prompt | self.llm | JsonOutputParser()
        
        try:
            res = job_chain.invoke({"text": text})
            return res if isinstance(res, list) else [res]
        except Exception as e:
            print(f"Error extracting jobs: {e}")
            return []

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))