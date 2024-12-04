import pandas as pd
import plotly.express as px
import plotly
import numpy as np

# Gathering Data from the CSV File
df = pd.read_csv("K:\InhouseERP\xficienZ\Dataset\Log Sheets\SV1312-SIVARAMAN_S.csv")#SV-0123_SIVARAMAN_S.csv

pie_chart = px.pie(data_frame=df, values='MAN_HOURS', names='PROJECT', 
                    # color='PROJECT / SERVICE(1)',
                    title= 'Project / Service Worked' , template='plotly_white',
                    )
pie_chart.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
pie_chart.show()
# plotly.offline.plot(pie_chart, filename="projectpie.html")

pie_chart1 = px.pie(data_frame=df, values='MAN_HOURS', names='FIELD_ OF_WORK', 
                    # color='PROJECT / SERVICE(1)',
                    title= 'Field Of Work Concentrated' , template='plotly_white',
                    )
pie_chart1.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
pie_chart1.show()
# plotly.offline.plot(pie_chart1, filename="projectpie1.html")

pie_chart2 = px.pie(data_frame=df, values='MAN_HOURS', names='SECTION', 
                    # color='PROJECT / SERVICE(1)',
                    title= 'Sections Worked' , template='plotly_white',
                    )
pie_chart2.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
pie_chart2.show()
# plotly.offline.plot(pie_chart2, filename="projectpie2.html")

pie_chart3 = px.pie(data_frame=df, values='MAN_HOURS', names='DAILY_ACTIVITY',title= 'Daily Activity Concentrated' , template='plotly_white')
pie_chart3.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
pie_chart3.show()
# plotly.offline.plot(pie_chart3, filename="projectpie3.html")

projbar = px.bar(data_frame=df, x='PROJECT', y='MAN_HOURS', title='Projects Concentrated', template='plotly_white', color='PROJECT')
projbar.update_traces()
projbar.show()
# plotly.offline.plot(projbar, filename="projectbar.html")