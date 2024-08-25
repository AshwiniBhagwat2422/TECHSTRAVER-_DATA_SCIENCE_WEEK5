import os
import re
import pandas as pd
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    return pdf_extract_text(file_path)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def parse_resume(text):
    sections = {
        "education": "",
        "experience": "",
        "skills": ""
    }

    education_pattern = re.compile(r'(Education|Academic Background).*', re.IGNORECASE | re.DOTALL)
    experience_pattern = re.compile(r'(Experience|Work History).*', re.IGNORECASE | re.DOTALL)
    skills_pattern = re.compile(r'(Skills|Core Competencies).*', re.IGNORECASE | re.DOTALL)

    sections['education'] = re.search(education_pattern, text)
    sections['experience'] = re.search(experience_pattern, text)
    sections['skills'] = re.search(skills_pattern, text)

    for key in sections.keys():
        if sections[key]:
            sections[key] = sections[key].group(0)
        else:
            sections[key] = "Not Found"
    
    return sections

def analyze_text(text):
    doc = nlp(text)
    entities = {
        "names": [],
        "dates": [],
        "organizations": []
    }
    for ent in doc.ents:
        if ent.label_ in ["PERSON"]:
            entities["names"].append(ent.text)
        elif ent.label_ in ["DATE"]:
            entities["dates"].append(ent.text)
        elif ent.label_ in ["ORG"]:
            entities["organizations"].append(ent.text)
    return entities

def store_data_to_csv(data, filename='resume_data.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

file_path = 'C:/Users/USER/Desktop/TechStraver/Data Science/Week 5/Project 2/example_resume.pdf'
try:
    text = extract_text(file_path)
    parsed_data = parse_resume(text)
    analyzed_data = analyze_text(text)
    
    data = {
        "File": [file_path],
        "Education": [parsed_data['education']],
        "Experience": [parsed_data['experience']],
        "Skills": [parsed_data['skills']],
        "Names": [', '.join(analyzed_data['names'])],
        "Dates": [', '.join(analyzed_data['dates'])],
        "Organizations": [', '.join(analyzed_data['organizations'])]
    }
    
    store_data_to_csv(data)
    print(f"Data from {file_path} has been processed and stored.")

except Exception as e:
    print(f"An error occurred: {e}")