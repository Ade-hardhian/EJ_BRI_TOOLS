import streamlit as st
import pandas as pd
import os
    
def analysis_EJ(filename):
  output=[]
  with open(filename) as f:
    all_line = f.readlines()

  start_date = ""
  start_time = ""
  end_time = ""
  card_insert = ""
  pin_enter = ""
  dispensed_amount = ""
  total_deposit_amount = 0
  trx_a = ""


  for i, line in enumerate(all_line):
    if "Transaction Start" in line:
      
      start_data = line.split(" ")
      
      start_date = start_data[0]
      start_time = start_data[1]
      end_time = ""
      card_insert = ""
      pin_enter = ""
      dispensed_amount = ""
      total_deposit_amount = 0
      trx_a = ""

    if "Notes Dispensed" in line:
      trx_a = ("Tarikan")
    else:
      if  "Notes Counted" in line:
        trx_a = ("Setoran") 
    
    if "Card Inserted" in line:
      card_data = line.split(" ")
      card_insert = card_data[1]

    if "PIN Entered" in line:
      pin_data = line.split(" ")
      pin_enter = pin_data[1]

    if "Notes Dispensed" in line:
      line_a = i + 1       
    
      note_data = all_line[line_a].split("*")
      note_dispensed = note_data[0].strip('IDR')
      note_pcs = note_data[1]

      dispensed_amount = int(note_dispensed) * int(note_pcs)


    if "Notes Counted" in line:
      deposit_amount_100 = 0
      deposit_amount_50 = 0
      for j in range(3):
        line_number = i + j +1
       

        if "IDR100000x" in all_line[line_number]:
          deposit_data_100 = all_line[line_number].split("x")
       
          deposit_denom_100 = deposit_data_100[0].strip('IDR')

          deposit_pcs_100 = deposit_data_100[1] 
          
          deposit_amount_100 = int(deposit_denom_100) * int(deposit_pcs_100)
         

        if "IDR50000x" in all_line[line_number]:
          deposit_data_50 = all_line[line_number].split("x")
        
          deposit_denom_50 = deposit_data_50[0].strip('IDR')

        
          deposit_pcs_50 = deposit_data_50[1] 

       
          deposit_amount_50 = int(deposit_denom_50) * int(deposit_pcs_50)
         

        if "Rejectx" in all_line[line_number]:
          deposit_rejected = all_line[line_number].split("x")

          deposit_pcs_reject = deposit_rejected[1] 
         

      total_deposit_amount = deposit_amount_100 + deposit_amount_50

      
    if "Transaction End" in line:
      end_data = line.split(" ")
      end_time = end_data[1]
    

      output.append([start_date, start_time, card_insert, pin_enter, trx_a, dispensed_amount, total_deposit_amount, end_time])
      #print(output)
    
  return output


title = st.text_input('Input your Directory EJ Sample like below:', 'D:/Git/BRI/EJ/')
st.write('your directory:', title)

if st.button('Execute'):

  for foldername, subfolders, filenames in os.walk(title): 
    #print(filenames)

  
    output_ej_data = []

    for filename in filenames:
      #print(filename)

      basename, ext = os.path.splitext(filename)
      #print(basename)

      if ext == '.jrn':

      
        input_filename = foldername + '/' + filename

        
        output_trx = analysis_EJ(input_filename)
        #print(output_trx)

        
        output_ej_data = output_ej_data + output_trx
        #print(output_ej_data)
        
    df = pd.DataFrame(output_ej_data)
    #print(df)
    df.rename(columns={0:'Start Date', 1:'Start Time', 2:'Card Inserted', 3:'Pin Entered', 4:'Transaction Type', 5:'50K', 6:'100K',7:'End Time'}, inplace=True)
    df
