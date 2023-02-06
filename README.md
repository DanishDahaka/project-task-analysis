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

### Organisation

Plot tasks from [organisation-test.xlsx](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/organisation-test.xlsx) on a simple colored scatterplot consisting of three dimensions: 
- x-axis -> Impact (1-100)
- y-axis -> Urgency (1-100)
- color  -> category of task

Plots created with with [Plotly](https://plotly.com/python/).

Example simple Urgency / Importance matrix with Plotly:
![](https://github.com/DanishDahaka/project_task_analysis/blob/master/images/task_scatter_matrix.png)

More advanced plots available on request.

Again utilizing the same .xlsx file, we use [create_organisation_backup.py](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/create_organisation_backup.py) to write the current data into a newly named .xlsx file; simply by appending timestamps to the filename. This script may be utilized for e.g. the automation of backups

### Recommend similar tasks
Create custom recommendations from the aforementioned task list [organisation-test.xlsx](https://github.com/DanishDahaka/project_task_analysis/blob/master/organisation/organisation-test.xlsx) based on text input field rendered as HTML in Dash. The recommendations result from calculations of the [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity) between the text vectors created by [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf).

Example input and recommendations:
![](https://github.com/DanishDahaka/project_task_analysis/blob/master/images/recommender_sys_dash_example.png)
