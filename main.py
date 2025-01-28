from src.extractor import ResumeExtractor, JdExtractor
from src.cohere_client import CohereClient
from src.parser import ResumeParser
from src.similarity import SimilarityCalculator
import json
import os

def main():
    # Initialize components
    extractor = ResumeExtractor(input_folder="./data/resumes/")
    jd_extractor = JdExtractor(input_folder="./data/jd/")
    cohere_client = CohereClient()
    parser = ResumeParser(output_folder="./data/output/")
    similarity_calculator = SimilarityCalculator(jd_folder="./data/jd/")
    # jd_text = similarity_calculator.extract_job_descriptions()

    # Extract JD text:
    jd_files = jd_extractor.get_all_files()
    jd_text = ""

    for file_path in jd_files:
        try:
            print(f"Processing: {file_path}")
            text = jd_extractor.extract_text(file_path)
            jd_text = jd_text + text
        except Exception as e:
            print(f"Error processing {file_path}: {e}")


    # Extract and process resumes
    files = extractor.get_all_files()
    all_data = []
    resume_texts = []

    for file_path in files:
        try:
            print(f"Processing: {file_path}")
            raw_text = extractor.extract_text(file_path)
            # if raw_text:
            #     # print(raw_text)
            #     # cleaned_text = extractor.clean_text(raw_text)  # Clean the extracted text
            #     # if cleaned_text:
            #     #     print(f"Cleaned text: {cleaned_text[:100]}")
            #     # else:
            #     #     print(f"Error: Unable to clean text from {file_path}")
            # else:
            #     print(f"Error: Unable to extract text from {file_path}")

            resume_texts.append(raw_text)
            # print(resume_texts)
            # print("text extracted successfully.",text)
            extracted_json = cohere_client.generate_json(raw_text)
            parsed_data = json.loads(extracted_json)
            print("data parsed successfully")
            # Calculate similarity scores
            # similarity_score = similarity_calculator.calculate_similarity(parsed_data, jd_text)
            # parsed_data['Similarity score'] = similarity_score
            all_data.append(parsed_data)
            # print(parsed_data)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Calculate similarity scores
    similarity_scores = similarity_calculator.calculate_similarity(resume_texts, jd_text)

    # Add similarity scores to parsed data
    for i, data in enumerate(all_data):
        data['Similarity_Score'] = similarity_scores[i]
    # print(all_data)

    # Save results to JSON and aggregated CSV
    file_name = "final"
    parser.save_as_json(all_data, file_name)
    # Save aggregated CSV
    if all_data:
        parser.save_as_csv(all_data, "final_csv")
        print("Information stored successfully.")
if __name__ == "__main__":
    main()
