import fitz  
import re
import spacy
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    #Extract raw text from pdf 
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def normalize_text(text):
    #Cleans the raw text, removing white space and line breaks 
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()



def extract_name_from_top(text, n_lines=15):
    lines = text.split('\n')
    top_text = '\n'.join(lines[:n_lines])
    doc = nlp(top_text)
    candidates = [
        ent.text.strip() for ent in doc.ents
        if ent.label_ == "PERSON" and len(ent.text.strip().split()) > 1
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda x: len(x.split()), reverse=True)
    return candidates[0]

def extract_graduation_year(text):
    current_year = datetime.now().year
    grad_phrases = re.findall(
        r'(expected|graduated|graduation)[^\d]{0,15}(\d{4})',
        text, flags=re.IGNORECASE
    )
    for _, year_str in grad_phrases:
        year = int(year_str)
        if 1900 <= year <= current_year + 5:
            return str(year)
    years = re.findall(r'\b(19\d{2}|20\d{2}|2030)\b', text)
    years = [int(y) for y in years if 1900 <= int(y) <= current_year + 5]
    return str(max(years)) if years else None

def is_skill_line(line):
    doc = nlp(line)
    nouns = sum(1 for token in doc if token.pos_ in ('NOUN', 'PROPN', 'ADJ'))
    verbs = sum(1 for token in doc if token.pos_ == 'VERB')
    return nouns > 0 and verbs == 0 and len(line.split()) <= 7

def extract_skills_adaptive(lines):
    skill_headers = ['skills', 'expertise', 'technical skills', 'core competencies', 'abilities', 'strengths']
    collected = []
    collecting = False
    max_lines = 10

    for line in lines:
        lower = line.lower().strip()
        if any(h in lower for h in skill_headers):
            collecting = True
            continue
        if collecting:
            if not line.strip() or len(collected) >= max_lines:
                break
            if is_skill_line(line):
                collected.append(line.strip())

    skill_text = ' '.join(collected)
    parts = re.split(r'[•,\-\|\n;·●]', skill_text)
    skills = [p.strip() for p in parts if p.strip()]
    return skills if skills else None

def extract_fields(text):
    result = {}

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    result['Name'] = extract_name_from_top(text)

    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    result['Email'] = email_match.group(0) if email_match else None

    result['GraduationYear'] = extract_graduation_year(text)

    skills = extract_skills_adaptive(lines)
    result['Skills'] = ', '.join(skills) if skills else None

    return result



with open("OfficialOfficialResume.pdf", "rb") as f:
    doc = fitz.open(stream=f.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

data = extract_fields(text)
print(data)
