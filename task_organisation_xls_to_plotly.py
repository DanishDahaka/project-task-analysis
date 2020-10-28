import pandas as pd
import numpy as np
import math
import random as r
import os

### resources ###
#https://wiki.en.it-processmaps.com/index.php/Checklist_Incident_Priority
#https://www.bmc.com/blogs/impact-urgency-priority/

begin = pd.Timestamp.now()

### change infile accordingly depending on path/file
infile = "organisation-test.xlsx"
outfile = infile


#split column 5 ('Prerequisite (IDs) based on separator into one or multiple list elements)
df = pd.read_excel(infile, usecols = "A:R") 


def get_remaining_hours(timestamp,forward):

    current_day = pd.Timestamp.now()

    if forward == True:
        seconds = (timestamp - current_day).total_seconds()
    elif forward == False:
        seconds = (current_day - timestamp).total_seconds()
    else:
        raise Exception("conversion wrong, check input")

    return round(seconds/3600,2)

#version without estimate, consider adding if it deems necessary at some point
def urgency(vec):
    """adding the estimate is relevant! how do you otherwise know IF and WHEN to start a project? 
    Combine this with Predecessor/Successor""" 
    urgency, worked_on, hours_left, finished, estimate, set_to_doing, id, deadline, name = \
    vec[0], vec[1], vec[2], vec[3], vec[4], vec[5], vec[6], vec[7], vec[8]

    """this ratio puts most tasks to low urgency if they have just been entered a couple
    minutes ago -> they might sneak up on you. maybe different approach in the future?"""
    ratio = worked_on/(worked_on+hours_left)

    ###########################
    # remaining hours urgency #
    ###########################
    #dividing by four in order to narrow one day down to 6hrs max
    hours_left = int(hours_left)/4 

    if pd.isna(finished) == False:
        urgency = -100
    elif hours_left >= 6:
        urgency = int(ratio * 100)  
    elif 0 <= hours_left < 6:
        urgency = 100
    elif hours_left<0:
        print('Task {}: {}  is overdone. Reconsider deadline'.format(id,name))
    else:
        raise Exception('check deadline for urgency at ID {}'.format(id)) 

    """  urgency should be 0 when the prerequisites/predecessors are not finished yet  """
    
    return urgency


def time_elapsed(vec):
    """ return here should be in hours """
    ins, outs, time_elapsed = vec[0], vec[1], vec[2]
    
    if pd.isnull(outs) == False:
        return round((outs - ins).total_seconds()/3600,2)
    else:
        return time_elapsed

#for plotting the impact 0-10 values onto a 0-100 scale in the graph:
def map_10s_to_100s(i):

    rand1,rand2,rand3,rand4 = r.randrange(10),r.randrange(10),r.randrange(10),r.randrange(10)
    
    if i == 10:
        i = 100
    else:
        i = (i*10)+((rand1+rand2)/2)-((rand3+rand4)/2)
    return int(i)

def priority(vec):

    #maybe change this to numbers, so you can sort? can always add strings again later on!
    names = ["Low","Medium","High","Today","Done"]

    urgency, impact, priority = vec[0], vec[1], vec[2]

    if urgency == 100:
        priority = names[3]
    
    else:
        
        impact = map_10s_to_100s(impact)
        calc = (urgency + (impact)) /2

        if 0 < calc <= 33:
            priority = names[0]
        elif 33 < calc <= 66:
            priority = names[1]
        elif 66 < calc <= 99.99:
            priority = names[2]
        else:
            #marks tasks which do not have any urgency "done"                                
            priority = names[-1]
    
    return priority

def status(vec):

    prio, status, finished, set_to_doing, id = vec[0], vec[1], vec[2], vec[3], vec[4]


    #check these conditions here, still some improvements to be done!
    if "Done" in prio:
        status = "Done"
    elif pd.isna(finished) == True and status == "Done":
        status = "Check finished column" #possibly only a print statement important?
    elif pd.isna(set_to_doing) == False:
        status = "Doing"
    else:
        status = "To-Do" #does this work properly with both "Doing" and "To-Do" as possible status?

    return status
	
	#show pop up window (clickable list?) with tasks which are marked with today
	
	#def show_daily(vec):

def wrong_deadline_finished(vec):

    id, overdue = vec[0], vec[1]

    if overdue <= 0:
        print('Task {} has a mismatch between Deadline and Finished on'.format(str(id)))
    else:
        pass
	            	    
        
#######################    
### begin main code ###
#######################
weekdays_hours, weekend_hours = 6,5
current_day = pd.Timestamp.now()
day_of_week = current_day.dayofweek

if(day_of_week < 5):
#weekend time, day_of_week 5 or 6
    weekend = False
elif(day_of_week == 5 or day_of_week == 6):
    weekend = True
else:
    raise Exception("Days did not work")

###############################
# pandas dataframe operations #
###############################

# checking the dataframe for sanity, cleaning NaN
df = df.dropna(axis=0, how = "all")

# creating two new columns with relative time from Entry Date to now to Deadline
df['Time left (hrs)'] = df['Deadline'].apply(get_remaining_hours, args=(True,)) 
df['Worked on (hrs)'] = df['Entry Date'].apply(get_remaining_hours, args=(False,))


# Updating urgency
df['Urgency'] = df[['Urgency','Worked on (hrs)','Time left (hrs)','Finished on', \
'Estimate (hrs)', 'Set to Doing', 'ID', 'Deadline', \
'Name']].apply(urgency, args=(weekend,), axis = 1)

# Setting priority 
df['Priority'] = df[['Urgency','Impact/Output', \
'Priority']].apply(lambda y: priority(y), axis = 1)

# Setting Time elapsed 
df['Time elapsed'] = df[['Entry Date','Finished on',\
'Time elapsed']].apply(lambda z: time_elapsed(z), axis = 1)


df['Status'] = df[['Priority','Status','Finished on', \
'Set to Doing', 'ID']].apply(lambda a: status(a), axis = 1)

#Effort is based on the time which elapsed from set to doing until finished
df['Effort (hrs)'] = df[['Set to Doing','Finished on',\
'Effort (hrs)']].apply(lambda b: time_elapsed(b), axis=1)

# remove unwanted columns
df.drop(['Time left (hrs)','Worked on (hrs)'], axis = 1, inplace = True)

#sort df by id for overview in excel sheet
df = df.sort_values(ascending=False, by='ID')

# validating uniqueness and consecutiveness of IDs
ids = df['ID'].tolist()
idstrs = [str(i) for i in ids]

checklist = [i for i in range(1, len(df)+1)]

#sequence in ids does not matter but all natural integers from 1 to len(df) should be inside it 
if len(ids) == len(checklist):
    for i in range(0,len(ids)):
        if(checklist[i] in ids):
            pass
        else:
            print("{} is not contained in the IDs. Pls check".format(str(checklist[i])))
else:
    print("amount of IDs seems to be different than the amount of rows")


##############
### OUTPUT ###
##############

writer = pd.ExcelWriter(outfile, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index = False)

workbook  = writer.book
worksheet = writer.sheets['Sheet1']

#change sheet size to match column width 
worksheet.set_column('A:A', 4)  # ID column
worksheet.set_column('B:B', 17) # name column
worksheet.set_column('C:C', 9)  # category column
worksheet.set_column('D:D', 17)
worksheet.set_column('E:E', 17)
worksheet.set_column('F:G', 15)
worksheet.set_column('H:H', 12)
worksheet.set_column('I:I', 12)
worksheet.set_column('J:J', 15)
worksheet.set_column('M:N', 17) # timestamps fit perfectly inside width=17 cells (in excel)
worksheet.set_column('O:O', 12)
worksheet.set_column('Q:Q', 12) # measured effort 
#column p is comment, no need for setting any width because it is the last column


writer.save() 

##################
### OUTPUT END ###
##################

#splitting final dataframe into subsets depending on Status, maybe do sth with this?
done_tasks = df[df['Status']=='Done']
doing_tasks = df[df['Status']=='Doing']
todo_tasks = df[df['Status']=='To-Do']
#getting stuff from priority as well
today_tasks = df[df['Priority']=='Today']

#sanity check whether the deadline is still before the finished on timestamp.
df['overdue'] = (done_tasks['Deadline'] - done_tasks['Finished on']).astype('timedelta64[h]')

#creates a df of shape (len(df),2) which simplifies mismatch calculation, dropping all NaN rows.
smaller_df = df[['ID','overdue']].dropna(axis=0, how = "any")

smaller_df[['ID','overdue']].apply(lambda x: wrong_deadline_finished(x), axis = 1)

###########################
### informative prints ###
###########################

#possibly percentage more helpful for some metrics?
print('General Overview:')
print('-----------------')
print('A total of {} tasks exists. \nThere are {} tasks marked "Done".\n{} I am currently "Doing" +\
and {} remain "To-Do"'.format(len(df),len(done_tasks),len(doing_tasks),len(todo_tasks)))
print('-----------------')
###

for i in range(0,len(today_tasks)):
    print('Task with ID {} named "{}" can be completed +\
    today'.format(today_tasks.iloc[i].ID,today_tasks.iloc[i].Name))
    i += 1


#dropping all rows which have -100 in urgency
df = df[df['Urgency']>=0]

#also changes impact for plotting, outside of reading and writing to the files
df['Impact/Output'] = df['Impact/Output'].apply(lambda x: map_10s_to_100s(x))

labels = df['Name'].tolist()

#creates joined list with both the IDs first and labels second, used for showing info on hover
joined = [i + ": " + j for i, j in zip(idstrs, labels)] 

#######################
### plotly plotting ###
#######################

#pip install plotly
import plotly.express as px

fig = px.scatter(df,    x=df['Impact/Output'], 
                        y=df['Urgency'],
                        #hover_data = add existing data to plot
                        #displays top title when hovering over 
                        hover_name=joined,           
                        color=df['Category'])

# Set axes ranges
fig.update_xaxes(range=[-10, 110])
fig.update_yaxes(range=[-10, 110])

#put horizontal and vertical bars
fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=50,
            y0=-10,
            x1=50,
            y1=110,
            line=dict(
                color="black",
                width=3
            )
))

fig.add_shape(
        # Line horizontal
        dict(
            type="line",
            x0=-10,
            y0=50,
            x1=110,
            y1=50,
            line=dict(
                color="black",
                width=3
            )
))

fig.update_traces(marker=dict(size=8,
                              line=dict(width=2,
                                color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.show()
