# Project task analysis

## Short Table of Contents

1. Why
2. How
3. What
    1. organisation
    2. recommend_similar_tasks
    
## Why
To get a better overview about tasks in an (agile) project backlog.

## How
Read tasks rows from .xlsx format, calculate time passed from insertion and update task status.

## What
Plot tasks on a simple colored scatterplot consisting of three dimensions: 
- x-axis -> date as timestamp
- y-axis -> duration in hours
- color  -> category of task

Contains the following two directories:

## organisation
Based on a task list called [organisation-test.xlsx](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/organisation-test.xlsx) data is read into a dataframe (df), adjusted and plotted as two variations, one with [matplotlib / seaborn](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/task_organisation_xls_to_plt_with_sns.py) & [plotly](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/task_organisation_xls_to_plotly.py).

Example plot with Plotly:
![](https://github.com/DanishDahaka/project_task_analysis/blob/master/images/task_scatter_matrix.png)

More advanced plots available on request.

Again using the same .xlsx file, we use [create_organisation_backup.py](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/create_organisation_backup.py) to write the current data into a new .xlsx file adding timestamps to the filename. Useful for e.g. automation of backups

## recommend_similar_tasks
Create custom recommendations from the aforementioned task list [organisation-test.xlsx](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/organisation-test.xlsx) based on text input field rendered as HTML in Dash. The recommendations result from calculations of the [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity) between the text vectors created by [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf).

Default view of the recommender system:
![Test](https://github.com/DanishDahaka/project_task_analysis/blob/master/images/recommender_sys_dash_default.png)

Example input and recommendations:
![](https://github.com/DanishDahaka/project_task_analysis/blob/master/images/recommender_sys_dash_example.png)
