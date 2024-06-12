#importing pandas as pd 
import pandas as pd 
import os
  
def convert_demographics_excel_to_csv(filename_xlsx,filename_csv):
    if os.path.exists(filename_csv):
        os.remove(filename_csv)
    
    # Read and store content 
    # of an excel file  
    read_file = pd.read_excel (filename_xlsx) 
      
    # Write the dataframe object 
    # into csv file 
    read_file.to_csv (filename_csv,  
                      index = None, 
                      header=True) 
        
    # read csv file and convert  
    # into a dataframe object 
    df = pd.DataFrame(pd.read_csv(filename_csv)) 
      
    # show the dataframe 
    # df