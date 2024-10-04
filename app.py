import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
from tkinter import Tk, Label, Entry, Text, Button, END, Frame, Scrollbar, VERTICAL, RIGHT, Y, BOTH
from tkinter import font as tkFont

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    
    # Converting words to root form
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    
    return ' '.join(words)

with open("D:/NLP Project/preprocess_text.pkl", "rb") as file:
    df = pickle.load(file)

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def suggest_sections(complaint, dataset, min_suggestions=5):
    preprocessed_complaint = preprocess_text(complaint)
    complaint_embedding = model.encode(preprocessed_complaint)
    section_embedding = model.encode(dataset['Combo'].tolist())
    similarities = util.pytorch_cos_sim(complaint_embedding, section_embedding)[0]
    similarities_thershold = 0.9
    
    relevant_indices = []
    
    while len(relevant_indices) < min_suggestions and similarities_thershold > 0:
        relevant_indices = [i for i, sim in enumerate(similarities) if sim > similarities_thershold]
        similarities_thershold -= 0.05
        sorted_indices = sorted(relevant_indices, key=lambda i: similarities[i], reverse=True)
        
        suggestions = dataset.iloc[sorted_indices].drop('Combo', axis=1).to_dict(orient='records')

    return suggestions

def get_suggestions():
    complaint = complaint_entry.get()
    suggestions = suggest_sections(complaint, df)
    output_text.delete(1.0, END)
    if suggestions:
        output_text.insert(END, "Suggested Sections:\n\n")
        for suggestion in suggestions:
            output_text.insert(END, f"Description: {suggestion['Description']}\n")
            output_text.insert(END, f"Offense: {suggestion['Offense']}\n\n")
            output_text.insert(END, f"Punishment: {suggestion['Punishment']}\n\n")
            output_text.insert(END, "-" * 100 + "\n\n")
    else:
        output_text.insert(END, "No record found!")

# Initialize the main window
root = Tk()
root.title("Crime Section Suggestion")
root.geometry("800x600")  
root.configure(bg="#f0f0f0")  


title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
label_font = tkFont.Font(family="Helvetica", size=12)


frame = Frame(root, bg="#f0f0f0", padx=10, pady=10)
frame.pack(fill=BOTH, expand=True)


title_label = Label(frame, text="Crime Section Suggestion Tool", font=title_font, bg="#f0f0f0", fg="#333")
title_label.pack(pady=(10, 20))


complaint_label = Label(frame, text="Enter Crime Description:", font=label_font, bg="#f0f0f0", anchor='w')
complaint_label.pack(fill="x")

complaint_entry = Entry(frame, width=100, font=("Arial", 12), bd=2, relief="sunken")
complaint_entry.pack(pady=(5, 15))

# Suggestion button
suggest_button = Button(frame, text="Get Suggestions", command=get_suggestions, bg="#4CAF50", fg="white", font=label_font)
suggest_button.pack(pady=10)

# Output text area with scrollbar
output_frame = Frame(frame)
output_frame.pack(fill="both", expand=True)

scrollbar = Scrollbar(output_frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

output_text = Text(output_frame, wrap="word", yscrollcommand=scrollbar.set, width=100, height=20, font=("Arial", 12), bd=2, relief="sunken")
output_text.pack(fill="both", expand=True)
scrollbar.config(command=output_text.yview)

root.mainloop()
