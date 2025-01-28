import pandas as pd
import nltk
from sklearn.preprocessing import MinMaxScaler

# Load the CSV file
# Columns: ['Name', 'Experience_Years', 'Education_Score', 'Skills_Score', 'Achievements_Score', 'Keywords_Match']
df = pd.read_csv("resumes.csv")

# Define weights for each parameter (adjust based on role priorities)
weights = {
    'Experience_Years': 0.3,  # 30% weight
    'Education_Score': 0.2,   # 20% weight
    'Skills_Score': 0.3,      # 30% weight
    'Achievements_Score': 0.1, # 10% weight
    'Keywords_Match': 0.1      # 10% weight
}

# Normalize columns to a 0-1 range for uniform scoring
scaler = MinMaxScaler()
for col in weights.keys():
    df[col] = scaler.fit_transform(df[[col]])

# Calculate a weighted score for each resume
df['Total_Score'] = sum(df[col] * weight for col, weight in weights.items())

# Sort resumes by total score
df = df.sort_values(by='Total_Score', ascending=False)

# Select the top 50 resumes
top_resumes = df.head(50)

# Save the top resumes to a new CSV file
top_resumes.to_csv("top_resumes.csv", index=False)

print("Top 50 resumes have been saved to 'top_resumes.csv'.")
