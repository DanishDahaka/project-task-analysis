import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import random as r
import os

### resources ###
#https://wiki.en.it-processmaps.com/index.php/Checklist_Incident_Priority
#https://www.bmc.com/blogs/impact-urgency-priority/

begin = pd.Timestamp.now()

infile = "organisation-test.xlsx"
outfile = infile

#split column 5 ('Prerequisite (IDs) based on separator into one or multiple list elements)
df = pd.read_excel(infile, usecols = "A:R") 
#Q as comment can be almost greyed out but the title should be super short (mantra-like 3 words maximum and show you what exactly the task is about)

print(df.tail())

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
def urgency(vec, weekend):
    """adding the estimate is relevant! how do you otherwise know IF and WHEN to start a project? Combine this with Predecessor/Successor""" 
    urgency, worked_on, hours_left, finished, estimate, set_to_doing, id, deadline, name = vec[0], vec[1], vec[2], vec[3], vec[4], vec[5], vec[6], vec[7], vec[8]
    
    #get boolean about weekend, True if current day either 5 or 6.
    weekend = weekend

    #today_hour = pd.Timestamp.now().hour

    #this ratio puts most tasks to low urgency if they have just been entered a couple minutes ago -> they might sneak up on you. maybe different approach in the future?
    ratio = worked_on/(worked_on+hours_left)

    ###########################
    # remaining hours urgency #
    ###########################

    #set urgency based on whether the task can be completed until 21.00 on a weekday or 23.00 on weekends.
    if weekend == True:
        #move the point outside plotting area (1,100) if there is an entry in "finished on"
        if pd.isna(finished) == False: #https://stackoverflow.com/questions/32863674/python-pandas-isnull-does-not-work-on-nat-in-object-dtype
            urgency = -100
        elif hours_left >= 5:
            urgency = int(ratio * 100)  

        #make the duration of hours left more sophisticated based on todays date and the remaining hours whether it is a work day (09:-17:00/anything which people want)
        #or study day (presumably time until 22:00)
        elif 0 <= hours_left < 5:
            urgency = 100
        elif hours_left<0:
            print('Task {}: {} is overdone. Reconsider deadline'.format(id,name))
        else:
            raise Exception('check deadline for urgency at ID {}'.format(id))


    elif weekend == False:
        if pd.isna(finished) == False: #https://stackoverflow.com/questions/32863674/python-pandas-isnull-does-not-work-on-nat-in-object-dtype
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

    

    hours_left = int(hours_left)/4 #per day urgency

    """ for really low values in timestamps, the urgency somehow gets set to 0. check why! maybe the ratio is guilty! it sure is, mylord."""
        
    
        
    return urgency


def time_elapsed(vec):
    """ return here should be in hours """
    ins, outs, time_elapsed = vec[0], vec[1], vec[2]
    
    #add state-change from "to-do" into "doing", called "Begin Date"
    
    if pd.isnull(outs) == False:
        return round((outs - ins).total_seconds()/3600,2)
    else:
    #return this as some fixed time which is default for all non-completed tasks. what would you want?
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

    names = ["Low","Medium","High","Today","Done"]

    urgency, impact, priority = vec[0], vec[1], vec[2]

    if urgency == 100:
        priority = names[3]
    
    else:
        
        impact = map_10s_to_100s(impact)
        calc = (urgency + (impact)) /2
        #print("this is calc for {} from urgency".format(calc))

        if 0 < calc <= 33:
            priority = names[0]
        elif 33 < calc <= 66:
            priority = names[1]
        elif 66 < calc <= 99.99:
            priority = names[2]
        else:                               
            priority = names[-1]                            #mark tasks without urgency calculation as "done"

    return priority

def status(vec):

    prio, status, finished, set_to_doing, id = vec[0], vec[1], vec[2], vec[3], vec[4]

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
        #this, and also the 'is overdone. Reconsider deadline' print can be put more sophisticated into a list which fills up and prints at the end!
        print('Task {} has a mismatch between Deadline and Finished on'.format(str(id)))
    else:
        pass
	            	    
	    
#add one row consisting of all data that was inputted over GUI (best case: only name)
def add_row(df):
    
    id = (len(df.index)+1) #adjusted because entry 0 in successor refers to no concrete task, they all begin with 1     
    
    
    stuff = [id]
    
    
    return pd.series(stuff)
        
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

# checking the dataframe for sanity, cleaning NaN (this removes only rows which have rows that are completely empty though ("all"))
df = df.dropna(axis=0, how = "all")

# creating two new columns with relative time from Entry Date to now to Deadline
df['Time left (hrs)'] = df['Deadline'].apply(get_remaining_hours, args=(True,)) #consider adding this column again to the excel in the future!
df['Worked on (hrs)'] = df['Entry Date'].apply(get_remaining_hours, args=(False,))


# Updating urgency, thanks to: https://stackoverflow.com/questions/34279378/python-pandas-apply-function-with-two-arguments-to-columns
df['Urgency'] = df[['Urgency','Worked on (hrs)','Time left (hrs)','Finished on', 'Estimate (hrs)', 'Set to Doing', 'ID', 'Deadline', 'Name']].apply(urgency, args=(weekend,), axis = 1)

# Setting priority 
df['Priority'] = df[['Urgency','Impact/Output','Priority']].apply(lambda y: priority(y), axis = 1)

# Setting Time elapsed 
df['Time elapsed'] = df[['Entry Date','Finished on','Time elapsed']].apply(lambda z: time_elapsed(z), axis = 1)


#state change from to-do to doing.
#df['To-Do to Doing'] = df[['Entry Date','Doing change','To-Do to Doing']].apply(lambda z: time_elapsed(z), axis = 1)

df['Status'] = df[['Priority','Status','Finished on', 'Set to Doing', 'ID']].apply(lambda a: status(a), axis = 1)

#Effort is based on the time which elapsed from set to doing until finished
df['Effort (hrs)'] = df[['Set to Doing','Finished on','Effort (hrs)']].apply(lambda b: time_elapsed(b), axis=1)

# remove unwanted columns, maybe also drop time elapsed but use it for calculations!! the column name needs to change anyway because there will be state transitions from to-do to doing to done
df.drop(['Time left (hrs)','Worked on (hrs)'], axis = 1, inplace = True)

#sort df by id for overview in excel sheet
df = df.sort_values(ascending=False, by='ID')

# validating uniqueness and consecutiveness of IDs
ids = df['ID'].tolist()
idstrs = [str(i) for i in ids]

# uniqueness still needs to be checked! possibly create a dictionary with all values which should exist and compare the found value for each key, if its not 1 then return key!

#create checklist based on the length of the entire dataframe, IDs should start at 1
#if you have different df's then concatenate all of them until this very point :)

checklist = [i for i in range(1, len(df)+1)]

#sequence in ids does not matter but all natural integers from 1 to len(df) should be inside it 
if len(ids) == len(checklist):
    for i in range(0,len(ids)):
        if(checklist[i] in ids):
            #increment value for the key here, so that any value which appears twice gets a value of 2 etc. -> simplifies tracing the wrong ID.
            pass
        else:
            print("{} is not contained in the IDs. Pls check".format(str(checklist[i])))
else:
    print("amount of IDs seems to be different than the amount of rows")


labels = df['Name'].tolist()

#creates joined list containing both the IDs first and labels second, used for showing info on hover
joined = [i + ": " + j for i, j in zip(idstrs, labels)] 


##############
### OUTPUT ###
##############

writer = pd.ExcelWriter(outfile, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index = False)

workbook  = writer.book
worksheet = writer.sheets['Sheet1']

"""#formatting anything with xlsxwriter that contains format datetime seems not to work: https://xlsxwriter.readthedocs.io/example_pandas_column_formats.html -> solution: set the main doc up once and refresh data.
elapsed_time_format = workbook.add_format({'num_format': '[$-x-systime]h:mm:ss AM/PM'}) """
#change sheet size to match column width (manually, this does not auto-fit), https://stackoverflow.com/questions/17326973/is-there-a-way-to-auto-adjust-excel-column-widths-with-pandas-excelwriter
worksheet.set_column('A:A', 4)  # ID column, width for larger numbers required in the long run, after 999
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
print('A total of {} tasks exists. \nThere are {} tasks marked "Done".\n{} I am currently "Doing" and {} remain "To-Do"'.format(len(df),len(done_tasks),len(doing_tasks),len(todo_tasks)))
print('-----------------')
###

for i in range(0,len(today_tasks)):
    print('Task with ID {} named "{}" can be completed today'.format(today_tasks.iloc[i].ID,today_tasks.iloc[i].Name))
    i += 1

#checking for day, setting remainining hours printout
if(weekend == False):
#weekend time, day_of_week 5 or 6
    print("It is a weekday, today you have {} hours set aside for tasks".format(str(weekdays_hours)))
elif(weekend == True):
    print("It is a weekend day, today you have {} hours set aside for tasks".format(str(weekend_hours)))
else:
    raise Exception("Days did not work")

#also changes impact for plotting, outside of reading and writing to the files
df['Impact/Output'] = df['Impact/Output'].apply(lambda x: map_10s_to_100s(x))

#####################################################################
### plotting with matplotlib featuring hovering mouse over points ###
#####################################################################

# big THANKS to ImportanceOfBeingErnest from https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib

#change style and size of labels
sns.set_style("darkgrid")
sns.set_context("notebook")

fig,ax = plt.subplots()
sc = plt.scatter(df['Impact/Output'], df['Urgency'], marker = "x") #change markers to your desire: https://matplotlib.org/3.1.0/api/markers_api.html#module-matplotlib.markers
#setting markers 10 points down and 70 left, so that they are visible in the plotting area
annot = ax.annotate("", xy=(0,0), xytext=(-100,-10), textcoords="offset points")

### draw two lines in order to separate the plot into (equally sized) quadrants
lower_bound = -15
upper_bound = 115
p1,p2 = [50,50],[lower_bound,upper_bound]
vert_sect = plt.plot(p1,p2,c="black")
first_hor_sect = plt.plot(p2,p1,c="black")

#setting axes bigger than values looks a lot nicer in terms of distance from the exact corner points
plt.axis([-15,115,-15,115]) 

#make title a variable which calls the respective rows from certain categories only, and changes title to "work", "study" etc. (use a dropdown list out of shortcuts?) possibly no
plt.gca().set(xlabel="Impact/Output", ylabel="Urgency", title="Tasks Organisation")

annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    #change for label settings
    text = "{}".format(" ".join([joined[n] for n in ind["ind"]]))
    annot.set_text(text)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

end = pd.Timestamp.now()
compilation_time = (end-begin).total_seconds()

#printing filename -> https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
print(os.path.basename(__file__),'compilation time: {}s'.format(compilation_time))

#show plot
plt.show()
