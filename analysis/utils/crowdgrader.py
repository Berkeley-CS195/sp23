import requests
import pandas as pd

from tqdm.notebook import trange, tqdm
from collections import defaultdict

def process_reviews(df):
    """Get the number of reviews and grades for each student."""
    review_counts, submission_grades = defaultdict(int), defaultdict(list)
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        URL = row['Reviews']
        data = requests.get(URL).json()
        submission_author, reviews = data['User email'], data['Reviews']
        for review in reviews:
            review_author, grade = review['Review author'], review['Review grade']
            review_counts[review_author] += 1
            submission_grades[submission_author].append(grade)

    # Now convert to a list of dicts to merge with the assignment_df.
    reviews = [{'User email': k, 'Reviews Num': v} for k, v in review_counts.items()]
    grades = [{'User email': k, 'Grades': v} for k, v in submission_grades.items()]
    return pd.DataFrame(reviews), pd.DataFrame(grades)

def process_crowdgrader(assignment_df):
    # Avoid side-effects.
    assignment_df = assignment_df.copy()

    # Get the number of reviews per student and the peer review grades.
    reviews_df, grades_df = process_reviews(assignment_df)

    # Add the number of reviews to each student.
    assignment_df = assignment_df.merge(reviews_df, how='outer', on='User email')

    # Add the peer-review grades for each student's submission.
    assignment_df = assignment_df.merge(grades_df, how='outer', on='User email')

    # Change type of submission date.
    assignment_df['Submission date'] = assignment_df['Submission date'].astype('datetime64')
    return assignment_df
