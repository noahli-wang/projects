import fitz  #PyMuPDF
import re   #regex
import spacy #spacy
from datetime import datetime


#Trained neural network to look for Specific Keywords
nlp = spacy.load("en_core_web_sm")


#Extract text from the document
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def normalize_text(text):
    #Cleans the raw text, removing white space and line breaks 
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()


#Gets the name from the cleaned text
def findName(text):
    #Trained Model to tokenize text and sort it 
    doc = nlp(text)   
    #Find text that think is a persons name
    candidates = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
    #Filter
    candidates = [c for c in candidates if len(c.split()) >= 2]
    #If candidates is empty
    if not candidates:
        return None
    
    #If found multiple names, choose the longest one 
    candidates.sort(key=lambda x: len(x.split()), reverse=True)
    return candidates[0]


def findGradYear(text):
    current_year = datetime.now().year
    #Finds 4 digit years number using regex
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    #Validating Years
    validYears = []
    for y in years:
        yearNum = int(y)
        if 1900 <= yearNum <= current_year + 6:
            validYears.append(y)

    if(len(years)) > 0:
        latest_year = max(years)
        return str(latest_year)
    return None

def findEmail(text):
    #Finds anything that matches any letters and @ then a . domain
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if match:
        email = match.group(0)
        return email
    return None


def extractSkills(text):
    lines = text.split('\n')
    #Common headers that people put on their resumes to display their skilsl
    headers = ["skills", "technical", "abilities", "strengths"]


    collect = False
    foundHeader = False
    skill = []

    #Go thorugh each line until we find one of the names from a header
    for line in lines:
        lower = line.lower()

        # Check if this line *starts* the skills section
        for h in headers:
            if h in lower:
                collect  = True
                # Don't treat the header line itself as a skill
                continue
        
        # Once we are collecting, try to capture skills
        if collect:

             # Stop when reaching a new section
            stop_words = ["education", "experience", "work history","projects", "volunteer", "certifications"]
            if any(w in line.lower() for w in stop_words):
                break

            # Stop when we hit a blank line (new section)
            if not line.strip():
                break

            #Look for key words, nouns, verbs, adj
            doc = nlp(line)
            #Let spacy find words that it thinks are nouns, proper nouns, adjectives, and verbs
            allowedNouns = ("NOUN", "PROPN", "ADJ")
            allowedVerbs = ("Verbs")
            #count the amount of nouns and verbs  in per line for filtering later on
            nouns = 0 
            verbs = 0 

            for token in doc:
                if token.pos_ == "NOUN" or token.pos_ == "PROPN" or token.pos_ == "ADJ":
                    nouns += 1
                elif token.pos_ == "VERB":
                    verbs += 1

            #if line only contains nouns and no verbs, must be a skill
            if nouns >= 1 and verbs == 0:
                skill.append(line.strip())
    
    #Final cleaning up
    finalSkills = []
    for s in skill:
        #Removes any bulletins that might be there
        parts = re.split(r'[•,\-\|\n;·●]', s)
        for p in parts:
            p = p.strip().title()
            if p not in finalSkills:
                finalSkills.append(p)

    if finalSkills:
        return finalSkills
    return None



def printResume(pdf_path):

    raw_text = extract_text_from_pdf(pdf_path)
    text = normalize_text(raw_text)

    results = {}

    results["Name"] = findName(text)
    results["Email"] = findEmail(text)
    results["Graduation Year"] = findGradYear(text)
    results["Skills"] = extractSkills(raw_text)

    return results


#----------User Input---------------------------

output = printResume("inputhere.pdf")

print("\n=================Resume Summary=================")
if output["Name"]:
    print(f"Name: {output['Name']}")

if output["Email"]:
    print(f"Email: {output['Email']}")

if output["Graduation Year"]:
    print(f"Graduation Year: {output['Graduation Year']}")

if output["Skills"]:
    print("\nSkills:")
    for skill in output["Skills"]:
        print(f"  - {skill}")






            




            

            





