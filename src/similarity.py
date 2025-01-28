import os
from src.extractor import ResumeExtractor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityCalculator:
    def __init__(self, jd_folder):
        self.jd_folder = jd_folder

    # def extract_job_descriptions(self):
    #     jd_texts = []
    #     jd_files = [
    #         os.path.join(self.jd_folder, f)
    #         for f in os.listdir(self.jd_folder)
    #         if f.endswith(('.pdf', '.docx'))
    #     ]
    #     for file_path in jd_files:
    #         # Use extractor logic (reuse from ResumeExtractor)
    #         text = ResumeExtractor(file_path).extract_text(file_path)
    #         jd_texts.append(text)
    #     return " ".join(jd_texts)  # Combine all JD texts into one

    def calculate_similarity(self, resume_texts, jd_text):
        similarity_scores = []

        # Initialize the vectorizer with English stop words
        vectorizer = TfidfVectorizer(stop_words='english')

        # Fit and transform the job description text (JD)
        jd_vector = vectorizer.fit_transform([jd_text])  # Shape: (1, n_features)

        # Transform the resume texts using the same vectorizer
        resume_vectors = vectorizer.transform(resume_texts)  # Shape: (n_resumes, n_features)

        # Calculate similarity score for each resume
        for resume_vector in resume_vectors:
            similarity_score = cosine_similarity(jd_vector, resume_vector)[0][0] * 100
            similarity_scores.append(similarity_score)

        return similarity_scores
