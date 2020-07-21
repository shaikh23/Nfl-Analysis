import requests
from bs4 import BeautifulSoup as bs
from bs4 import Comment as Comment
import numpy as np
import pandas as pd
import sqlite3
import pymongo
from bson.objectid import ObjectId


client = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0.znued.mongodb.net/test?ssl=true')


db = client.testFootballStats

#client = pymongo.MongoClient('mongodb://localhost:27017/')

client.list_database_names()
collection = db.players







Base_URL="https://www.pro-football-reference.com"
TeamsURL=Base_URL+"/teams/"

session=requests.session() 
headers=['urlteam','startYear','EndYear','TeamN']
vals=[['nwe',	'1960',	'1970',	'BOS']
,['nyj',	'1960',	'1962',	'NYT']
,['clt',	'1953',	'1983',	'BAL']
,['clt',	'1984',	'2019',	'IND']
,['oti',	'1960',	'1996',	'HOU']
,['oti',	'1997',	'2019',	'TEN']
,['kan',	'1960',	'1962',	'DTX']
,['sdg',	'1960',	'1960',	'LAC']
,['sdg',	'1961',	'2016',	'SDG']
,['sdg',	'2017',	'2019',	'LAC']
,['rai',	'1960',	'1981',	'OAK']
,['rai',	'1982',	'1994',	'RAI']
,['rai',	'1995',	'2019',	'OAK']
,['ram',	'1946',	'1994',	'RAM']
,['ram',	'1995',	'2015',	'STL']
,['ram',	'2016',	'2019',	'LAR']
,['crd',	'1950',	'1959',	'CRD']
,['crd',	'1960',	'1987',	'STL']
,['crd',	'1988',	'1993',	'PHO']
,['crd',	'1994',	'2019',	'ARI']
,['htx',	'1990',	'2019',	'HOU']
,['rav',	'1995',	'2019',	'BAL']
]
team_mapping=pd.DataFrame(vals, columns=headers)

def uniquify(df_columns):
    seen = set()

    for item in df_columns:
        fudge = 1
        newitem = item

        while newitem in seen:
            fudge += 1
            newitem = "{}_{}".format(item, fudge)

        yield newitem
        seen.add(newitem)

def get_team_df(session):
    res1=session.get(TeamsURL)
    
    soup1 = bs(res1.text.encode('utf8'), 'html.parser')
    
    Colheaders=[]
    for heads in soup1.select("#teams_active thead")[0].find_all('th')[7:]:
            Colheaders.append(heads.text)
            
                              
    
    for thead in soup1.select("#teams_active thead"):
        tbody = thead.find_next_sibling("tbody")
        rows=tbody.find_all('tr')
        rownumselect=[]
        for rown in rows:
            try:
                rownumselect.append(rown.find('th',{'class':'left'}).find('a').get('href'))
            except:
                rownumselect.append('')
    
        table = "<table>%s</table>" % (str(thead) + str(tbody))
    
        df = pd.read_html(str(table))[0]
        df['href'] = rownumselect
    
    Final_active_df=df.loc[df['href'] != '']
    Final_active_df=Final_active_df.reset_index()
    Final_active_df=Final_active_df.drop(Final_active_df.columns[[0]], axis=1)
    return Final_active_df

def get_team_data(session,teamname):
    Ind_Team=Base_URL+teamname
    
    res2=session.get(Ind_Team)
    
    soup2 = bs(res2.text.encode('utf8'), 'html.parser')
    
    
    for thead in soup2.select("#team_index thead"):
            tbody = thead.find_next_sibling("tbody")
            rows=tbody.find_all('tr')
            rownumselect=[]
            for rown in rows:
                try:
                    rownumselect.append(rown.find('th',{'class':'left'}).find('a').get('href'))
                except:
                    rownumselect.append('')
        
            table = "<table>%s</table>" % (str(thead) + str(tbody))
        
            df = pd.read_html(str(table))[0]
            df['href'] = rownumselect
    Final_ind_active_df=df
    return Final_ind_active_df


def get_YearTeam_data(session,YearTeam):
    Ind_Year=Base_URL+YearTeam
    res3=session.get(Ind_Year)
    soup3 = bs(res3.text.encode('utf8'), 'html.parser')
    
    for thead in soup3.select("#games thead"):
        tbody = thead.find_next_sibling("tbody")
        rows=tbody.find_all('tr')
        rownumselect=[]
        for rown in rows:
            try:
                rownumselect.append(rown.find('td',{'data-stat':'boxscore_word'}).find('a').get('href'))
            except:
                rownumselect.append('')
        
        table = "<table>%s</table>" % (str(thead) + str(tbody))
        
        df = pd.read_html(str(table))[0]
        df['href'] = rownumselect
        
    
    Final_Year_active_df=df
    return Final_Year_active_df

def get_indGame_data(session,IndGame):
    Ind_Year=Base_URL+IndGame
    try:
        res4=session.get(Ind_Year)
    except:
        try:
            res4=session.get(Ind_Year)
        except:
            try:
                session=requests.session() 
                res4=session.get(Ind_Year)
            except:
                res4=''
                
    soup4 = bs(res4.text.encode('utf8'), 'html.parser')
    
    for thead in soup4.select("#player_offense thead"):
        tbody = thead.find_next_sibling("tbody")
        rows=tbody.find_all('tr')
        rownumselect=[]
        for rown in rows:
            try:
                rownumselect.append(rown.find('th',{'data-stat':'player'}).find('a').get('href'))
            except:
                rownumselect.append('')
        
        table = "<table>%s</table>" % (str(thead) + str(tbody))
        
        df = pd.read_html(str(table))[0]
        df['href'] = rownumselect
    playeroffense_DF=df
    tables=soup4.select('#all_team_stats')[0]
    ind=0
    while ind < len(tables.find_all(text=lambda text: isinstance(text, Comment))):
        comment = tables.find_all(text=lambda text: isinstance(text, Comment))[ind]
        table= bs(comment, 'html.parser')
        for thead in table.select("#team_stats thead"):
            tbody = thead.find_next_sibling("tbody")
            rows=tbody.find_all('tr')
            table = "<table>%s</table>" % (str(thead) + str(tbody))
            
            df = pd.read_html(str(table))[0]
        ind+=1
    teamstats_df=df
    tables=soup4.select('#all_game_info')[0]
    ind=0
    while ind < len(tables.find_all(text=lambda text: isinstance(text, Comment))):
        comment = tables.find_all(text=lambda text: isinstance(text, Comment))[ind]
        table= bs(comment, 'html.parser')
        for thead in table.select("table"):
            
            rows=tbody.find_all('tr')
            table = "<table>%s</table>" % (str(thead) )
            
            df = pd.read_html(str(table))[0]
            df.columns= df.iloc[0]
            df=df.drop(0)
        ind+=1
    gameinfo_df=df
    try:
        tables=soup4.select('#all_officials')[0]
        ind=0
        while ind < len(tables.find_all(text=lambda text: isinstance(text, Comment))):
            comment = tables.find_all(text=lambda text: isinstance(text, Comment))[ind]
            table= bs(comment, 'html.parser')
            for thead in table.select("table"):
                
                rows=tbody.find_all('tr')
                table = "<table>%s</table>" % (str(thead) )
                
                df = pd.read_html(str(table))[0]
                df.columns= df.iloc[0]
                df=df.drop(0)
            ind+=1
        officials_df=df
    except:
        officials_df="NA"
    try:
        tables=soup4.select('#all_home_starters')[0]
        ind=0
        while ind < len(tables.find_all(text=lambda text: isinstance(text, Comment))):
            comment = tables.find_all(text=lambda text: isinstance(text, Comment))[ind]
            table= bs(comment, 'html.parser')
            for thead in table.select("table"):
               
                rows=tbody.find_all('tr')
                table = "<table>%s</table>" % (str(thead))
                
                df = pd.read_html(str(table))[0]
                
            ind+=1
        homestarters_df=df
    except:
        homestarters_df="NA"
    try:
        tables=soup4.select('#all_vis_starters')[0]
        ind=0
        while ind < len(tables.find_all(text=lambda text: isinstance(text, Comment))):
            comment = tables.find_all(text=lambda text: isinstance(text, Comment))[ind]
            table= bs(comment, 'html.parser')
            for thead in table.select("table"):
                rows=tbody.find_all('tr')
                table = "<table>%s</table>" % (str(thead))
                
                df = pd.read_html(str(table))[0]
                
            ind+=1
        awaystarters_df=df
        result = pd.concat([homestarters_df, awaystarters_df],axis=0)
        playeroffense_DF.columns =playeroffense_DF.columns.droplevel(0)
        playeroffense_DF=pd.merge(playeroffense_DF, result, on='Player', how='left')
    except:
        playeroffense_DF['Pos']="N/A"
    
    
    
    return playeroffense_DF,teamstats_df,gameinfo_df,officials_df


def master(nums):
    Team_list=get_team_df(session)
    Teamdf=Team_list.iloc[[nums]]
    Team_Year_Data=get_team_data(session,Teamdf['href'].iloc[0])
    Team_Year_Data=Team_Year_Data.loc[Team_Year_Data['href'] != '']
    Team_Year_Data.columns =Team_Year_Data.columns.droplevel(0)
    Team_Year_Data['Year']=Team_Year_Data['Year'].astype(str)
    Team_Year_Data=Team_Year_Data[(Team_Year_Data['Year']>'2009')]
    
    Final_Player_table=[]
    teamstats_table=[]
    gameinfo_table=[]
    officials_table=[]
    for years in Team_Year_Data['']:
        Team_Year_Game_Data=get_YearTeam_data(session,years)
        Team_Year_Game_Data=Team_Year_Game_Data.loc[Team_Year_Game_Data['href'] != '']
        Team_Year_Game_Data['Year']=years.split("/")[:4][3].replace(".htm","")
        Team_Year_Game_Data['TeamURLName']=years.split("/")[:4][2]
        for ind,games in enumerate(Team_Year_Game_Data['href']):
            print(years+' '+games)
            df=Team_Year_Game_Data.iloc[[ind]]
            df.columns =df.columns.droplevel(0)
            df=df[df.columns.unique()] 
            res_dfs=get_indGame_data(session,games)
            df['key'] = 0
            joint=res_dfs[0]
            joint1=res_dfs[1]
            joint2=res_dfs[2]
            joint3=res_dfs[3]
            joint['key'] = 0
            joint1['key'] = 0
            joint2['key'] = 0
            joint=joint[joint.columns.unique()] 
            joint2=joint2[joint2.columns.unique()] 
            try:
                joint3['key'] = 0
                dfn=pd.merge(df,joint3,on='key',how='outer')
                dfn.columns=list(uniquify(dfn.columns))
                officials_table.append(dfn)
                
            except:
                'NA'
            
            dfn=pd.merge(df,joint,on='key',how='outer')
            dfn.columns=list(uniquify(dfn.columns))
            Final_Player_table.append(dfn)
            dfn=pd.merge(df,joint1,on='key',how='outer')
            dfn.columns=list(uniquify(dfn.columns))
            teamstats_table.append(dfn)
            dfn=pd.merge(df,joint2,on='key',how='outer')
            dfn.columns=list(uniquify(dfn.columns))
            gameinfo_table.append(dfn)


    
    
   
    final_final_Final_Player_table=pd.concat(Final_Player_table)
    final_final_Final_Player_table = final_final_Final_Player_table[Final_Player_table[0].columns]
    conn = sqlite3.connect(':memory:')
    #write the tables
    final_final_Final_Player_table.to_sql('PlayerTab', conn, index=False)
    team_mapping.to_sql('team_mapping', conn, index=False)
    
    qry = '''
        select  
            pt.*,
            case when tm.urlteam IS NULL then lower(Tm_y) else tm.urlteam END as urlteam
        from
            PlayerTab as pt left join team_mapping as tm on
            _x_2>= startYear and _x_2<=EndYear 
            and TeamN=Tm_y
        '''
    QBStarts = pd.read_sql_query(qry, conn)
    #QBStarts=QBStarts[QBStarts['Pos']=="QB"]
    QBStarts2 = QBStarts[QBStarts['urlteam']==QBStarts['_x_3']]
    
    insertObj = {
        "crd": {
            "2019": {
                "1" : {
                    "Player" : {
                        
                        }
                    }
                }
            }
        }
    QBStarts2=QBStarts2.reset_index()
    QBStarts2['Week'].replace('Conf. Champ.', 'ConfFInal',inplace=True)
    for index, row in QBStarts2.iterrows():
        print(index)
        if index==0:
             insertObj = {
                 "Team": row['_x_3'],
                 row['_x_3'] : {
                     row['_x_2'] : {
                          str(row['Week']) : [{
                              row['Player'] : {
                                  "Position": row['Pos'],
                                  "PassCmp": row['Cmp'],
                                  "PassAtt": row['Att'],
                                  "PassYds": row['Yds'],
                                  "PassTD": row['TD'],
                                  "PassInt": row['Int'],
                                  "PassSk": row['Sk'],
                                  "PassYds": row['Yds'],
                                  "PassLng": row['Lng'],
                                  "PassRate": row['Rate'],
                                  "RushAtt": row['Att_2'],
                                  "RushYds": row['Yds_2'],
                                  "RushTD": row['TD_2'],
                                  "RushLng": row['Lng_2'],
                                  "RecTgt": row['Tgt'],
                                  "Rec": row['Rec_y'],
                                  "RecYds": row['Yds_3'],
                                  "RecTD": row['TD_3'],
                                  "RecLng": row['Lng_3'],
                                  "Fmb": row['Fmb'],
                                  "FL": row['FL'],
                                  }
                              }]
                         }
                     }
                 }
             collection.insert_one(insertObj)
        else:
            #{row['_x_3']+'.'+row['_x_2']+'.Week': row['Week']}
            collection.update({"Team": row['_x_3']}, 
                                   { "$push" : { row['_x_3']+'.'+row['_x_2']+'.'+str(row['Week']) :
                                                {
                                       row['Player'] : {
                                      "Position": row['Pos'],
                                      "PassCmp": row['Cmp'],
                                      "PassAtt": row['Att'],
                                      "PassYds": row['Yds'],
                                      "PassTD": row['TD'],
                                      "PassInt": row['Int'],
                                      "PassSk": row['Sk'],
                                      "PassYds": row['Yds'],
                                      "PassLng": row['Lng'],
                                      "PassRate": row['Rate'],
                                      "RushAtt": row['Att_2'],
                                      "RushYds": row['Yds_2'],
                                      "RushTD": row['TD_2'],
                                      "RushLng": row['Lng_2'],
                                      "RecTgt": row['Tgt'],
                                      "Rec": row['Rec_y'],
                                      "RecYds": row['Yds_3'],
                                      "RecTD": row['TD_3'],
                                      "RecLng": row['Lng_3'],
                                      "Fmb": row['Fmb'],
                                      "FL": row['FL'],
                                      }}}}, True
                                  )
         
    return QBStarts2


nums=7

numteams = np.arange(0,32,1)

for ilength in numteams:
    master(ilength)


    