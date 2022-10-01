import pandas as pd

def Close_Match_with_passed(passed, fail):
  # filtering data based on same UniqueID, Amount and Name
  filter_matches = passed[(passed["UniqueID"]==fail["UniqueID"]) & (passed["Amount"]==fail["Amount"]) & (passed["Name"]==fail["Name"])]
  # if no filter found, then return None 
  if len(filter_matches)==0:
    return fail , passed
  match_index = 0 
  close_match = filter_matches.iloc[0,]
  for row in range(len(passed)):
    if 	fail["date"]<passed.iloc[row,]["date"]: # check if current date 
      diff = passed.iloc[row,]["date"] - fail["date"]
      if diff.seconds/3600<24:  # if it is within one day 
        close_match = passed.iloc[row,]
        match_index = row
  # removing matched sucess from passed
  passed=  passed.drop(passed.index[match_index])
  return close_match, passed



def main():
  new_df = pd.DataFrame({'date':[],
                   'Status':[],
                   'UniqueID':[],
                   'Name':[],
                   'Amount':[],
                   'Description':[]})
  


  df = pd.DataFrame({'date':['2022-02-03 8:00','2022-02-03 8:01','2022-02-03 8:05','2022-02-05 9:00','2022-02-06 8:00','2022-02-07 10:00','2022-02-08 11:00','2022-02-10 10:00','2022-02-13 9:00','2022-02-13 9:05','2022-02-13 9:03','2022-02-13 9:07','2022-02-13 9:00','2022-02-13 9:02','2022-02-13 9:03','2022-02-13 9:07','2022-02-13 9:00'],
                    'Status':['Fail','Fail','Pass','Fail','Pass','Fail','Pass','Fail','Fail','Pass','Fail','Pass','Fail','Fail','Pass','Pass','Fail'],
                    'UniqueID':['12345','12345','12345','45678','45678','98765','98765','58345','77777','77777','77777','77777','88888','88888','88888','88888','88888'],
                    'Name':['A','A','A','B','B','C','C','C','D','D','D','D','E','E','E','E','E'],
                    'Amount':[9.99,9.99,9.99,10.99,10.99,99.99,99.99,100,500,450,100,100,200,200,200,200,200],
                    'Description':['2 failed with 1 pass (only 1 should match)','2 failed with 1 pass (only 1 should match)','2 failed with 1 pass (only 1 should match)','1 fail with 1 matching pass the next day 23 hours later','1 fail with 1 matching pass the next day 23 hours later','1 fail with 1 pass the next day 25 hours later (no match due to time)','1 fail with 1 pass the next day 25 hours later (no match due to time)','Fail with no match','Fail with pass that has wrong matching dollar amt','Fail with pass that has wrong matching dollar amt','Fail with matching pass','Fail with matching pass','3 fails with 2 matching passes','3 fails with 2 matching passes','3 fails with 2 matching passes','3 fails with 2 matching passes','3 fails with 2 matching passes']})
  df['date'] = pd.to_datetime(df['date']) #convert date to correct format
  # print(df.to_string())
  df = df.sort_values(['date']) #sorting date because it is required for the merge
  failed = df[df['Status'] == 'Fail'] #create df with just the fail records
  passed = df[df['Status'] == 'Pass'] #create df with just the pass records
  # check every fail with each passed
  match_status = []
  new_df = pd.DataFrame({'date':[],
                    'Status':[],
                    'UniqueID':[],
                    'Name':[],
                    'Amount':[],
                    'Description':[]}) 
  for fail in range(len(failed)):
    close_match, passed = Close_Match_with_passed(passed, failed.iloc[fail,])
    if failed.iloc[fail,]["Status"] == close_match["Status"]:  # if failed is returned, it means, no match found with pass
      match_status.append("Not Match")
      new_df = new_df.append(close_match, ignore_index = True) 
    else:
      match_status.append("Match")
      new_df = new_df.append(failed.iloc[fail,], ignore_index = True) 
      match_status.append("Match")
      new_df = new_df.append(close_match, ignore_index = True)
  new_df["Match Status"] =match_status
  new_df.to_csv("Output.csv", index=False)
main()