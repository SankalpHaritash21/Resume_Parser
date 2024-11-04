import os
import re
from pdfminer.high_level import extract_text
import spacy
from email_validator import validate_email, EmailNotValidError

# Load SpaCy English model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(file_path):
    """Extract text from the given PDF file."""
    return extract_text(file_path)

def extract_information(text):
    """Extract key information from the resume text."""
    doc = nlp(text)
    name = None
    email = None
    phone = None
    education = []
    work_experience = []
    skills = []

    # Regular expressions for email and phone number extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d[\d\s\-\(\)]{7,}\d'

    # Define a list of target skills
    target_skills = {
        "HTML", "CSS", "Tailwind CSS", "JavaScript", "TypeScript",
        "React.Js", "Jest", "Node.Js", "Express", "MongoDB",
        "SQL", "Git", "GitHub", "Visual Studio Code", "Postman"
    }

    # Extract named entities
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and not name:
            name = ent.text

    # Extract email
    email_matches = re.findall(email_pattern, text)
    if email_matches:
        email = email_matches[0]

    # Extract phone number
    phone_matches = re.findall(phone_pattern, text)
    if phone_matches:
        phone = phone_matches[0]

    # Validate email
    if email:
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            email = None

    # Split the text into lines for further analysis
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        # Extract education details
        if any(degree in line for degree in ["Bachelor", "Master", "PhD", "degree"]):
            education.append(line)
        # Extract work experience details
        elif "Experience" in line or "Work" in line or "employed" in line.lower():
            work_experience.append(line)
        # Extract skills based on the target skills list
        else:
            # Check if any skill in target_skills is present in the line
            found_skills = [skill for skill in target_skills if re.search(rf'\b{skill}\b', line, re.IGNORECASE)]
            skills.extend(found_skills)

    # Remove duplicates in skills list
    skills = list(set(skills))

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'education': education,
        'work_experience': work_experience,
        'skills': skills
    }

def main():
    # Change the path to your resume PDF file
    file_path = './Sankalp_Haritash.pdf'  # Replace with the path to your resume PDF
    if os.path.exists(file_path):
        text = extract_text_from_pdf(file_path)
        info = extract_information(text)

        # Print the extracted information to the console
        print("Extracted Information:")
        print(f"Name: {info['name']}")
        print(f"Email: {info['email']}")
        print(f"Phone: {info['phone']}")
        print("Education:")
        for edu in info['education']:
            print(f"- {edu}")
        print("Work Experience:")
        for exp in info['work_experience']:
            print(f"- {exp}")
        print("Skills:")
        for skill in info['skills']:
            print(f"- {skill}")
    else:
        print("File not found. Please check the file path.")

if __name__ == '__main__':
    main()
