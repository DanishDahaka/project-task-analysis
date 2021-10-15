# task_organisation_and_plotting

Contains the following files:

## task_organisation_xls_to_plotly.py & task_organisation_xls_to_mpl.py
Based on task list in tabular format (.xlsx) which is read into a dataframe (df), adjusted, rewritten to file and plotted (matplotlib &amp; seaborn vs. plotly &amp; dash currently)

## create_organisation_backup.py
Again using the same .xlsx file, the current data is written into a new .xlsx file with added timestamps to the filename. Useful for e.g. automation of backups

## input_recommendations.py & recommender_sys_for_input.py
Create custom recommendations based on text input field rendered by Dash. The recommendations result from calculations of the (Cosine Similarity)[https://en.wikipedia.org/wiki/Cosine_similarity] between the text vectors created by (TF-IDF)[https://en.wikipedia.org/wiki/Tf–idf].
