# task_organisation_and_plotting

Contains the following directories:

## organisation
Based on a task list called [organisation-test.xlsx](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/organisation-test.xlsx) data is read into a dataframe (df), adjusted, rewritten to file and plotted with [matplotlib / seaborn](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/task_organisation_xls_to_plt_with_sns.py) & [plotly] (https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/task_organisation_xls_to_plotly.py).
More advanced plots available on request.

Again using the same .xlsx file, we use [create_organisation_backup.py](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/create_organisation_backup.py) to write the current data into a new .xlsx file adding timestamps to the filename. Useful for e.g. automation of backups

## recommend_similar_tasks
Create custom recommendations from the aforementioned task list [organisation-test.xlsx](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/organisation-test.xlsx) based on text input field rendered as HTML in Dash. The recommendations result from calculations of the [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity) between the text vectors created by [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf).
