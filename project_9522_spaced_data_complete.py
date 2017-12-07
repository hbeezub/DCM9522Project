#project_9522_spaced_data.py

def process_file(reader):
    """ (file open for reading) -> new file format
    Read and process each line to populate a csv file with the 
    DEPT, PRODUCT, IP NUM, RPT SEQ, FDR SYS, &FDR KEY from a text file.
    The file contains much other information that we are not interested in.
    .
    """
    
    result_line= ''
    result=''
    prod=''
    count=0    #count for === line for prod
    first_var='-------'
    first_count =0    #count for first prod for --- line for prod
    
    #first we need to add headers
    with open('9522_new.csv', 'a') as output_file:
        output_file.write('"DEPT","PRODUCT","IPNUM","RPTSEQ","FDRSYS","FDRKEY"' +'\n')
        
    #get each line (for review/procesing)
    for line in reader:
        line=line.strip()    #removes leading/trailing whitespace
        field = line.split()  #seperates each word/field separated by whitespace
        #looking for the "end" of each product infrmation which is a === total line
        #this is only one item
        if len(field)>0 and len(field)<2:
            for e in range(len(field)):
                #to find product description find === line before
                if field[e].startswith('==='):
                    #the count line is so when it know the 'next' line is the description
                    count = 1
                    prod=''
        #don't want to look at any lines with no data or less than 3 'words'        
        elif len(field)>3:
            ##print('001-field=',field)
            for i in range(0,2):    #the first 2 'words' contain identifier fields
                #find dept         
                if field[i] == 'DEPT:':
                    #save DEPT
                    dept=field[i+1]
                    ##deptname? from field(i+3 to end)
                #to find first product description find --- line before since
                #there are several --- line types store this in a variable
                if field[i] == first_var:
                    first_count = 1
                    prod=''
                    #once we find this line we want to go to the next line
                    #which will be our first product description
                    break     
            
                #find first prod desc
                if first_count == 1:
                    #after first item update first_var
                    first_var='datasci'   #value 'datasci' is not in our text file
                    for f in range(len(field)):
                        if field[f]=='FDE':
                            #don't want any info after FDE
                            first_count=10    #so first count is no longer 1
                            #once we have the complete first prod desc we can go to the next line
                            break
                        else:
                            #compile the product description
                            prod=prod+field[f]+' '
                            #redundant reset of variables
                            count=0
                            first_count=10
                        
                #find prod desc after the first prod desc
                #'hardcode' in the startswith field[0] instead of using i
                #'filter out' all the header lines from the prod description
                if (count >0 and not field[0].startswith('*') and not field[0].startswith('DCM')
                        and not field[0].startswith('RUN')and not field[0].startswith('BILL') and not
                        field[0].startswith('FISCAL') and not field[0].startswith('DEPT:') and not
                        field[0].startswith('PRODUCT')and not field[0].startswith('-------')):
                    ##print ('count at not *=',count)
                    ##print('field[i]=',field[i])
                    ##print('field=',field)
                    for d in range(len(field)):
                        if field[d]=='FDE':
                            #only want the info before FDE
                            count=0
                            #once we get to FDE we have the description & can go to the next line
                            break
                        else:
                            prod=prod+field[d].replace(","," ")+' '
                            #some descriptions have commas in the description -need to remove them
                            #https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch02s11.html
                            # If you needed to do something to the inner space, you would need to use another technique, such as using the replace() method or a regular expression substitution.
                            #redundant reset of variable
                            count=0
                                                    
                #find IPNUM
                if field[i] == 'IP' and field[i+1] =='NUM':
                    #save IPNUM
                    ipnum=field[i+2].strip(':')
                #find RPT Seq
                if field[i] == 'RPT' and field[i+1].startswith('SEQ:'):
                    #save RPT SEQ
                    rptseq =field[i+1].strip('SEQ:')
                #find FDR SYS
                if field[i] == 'FDR' and field[i+1].startswith('SYS:'):
                    #(Kudgel) strip SYS deletes the leading/trailing S from the fdrsys
                    if field[i+1] == 'SYS:SUR':
                        #save FDR SYS
                        fdrsys='SUR'
                    else:
                        #save FDR SYS
                        fdrsys=field[i+1].lstrip('SYS:')  #lstrip accounts for ECS fdr system
                #find FDR KEY (last item before write to file)
                if field[i] == 'FDR' and field[i+1].startswith('KEY:'):
                        #(Kudgel)save FDR KEY
                        if field[i+2] == 'COST':   #for 'MEDIUM COST' fdrkey
                            fdrkey=field[i+1].lstrip('KEY:') + ' COST'
                        elif field[i+2] == 'DRUG':  #for 'NEW DRUG #' fdrkey
                            fdrkey=field[i+1].lstrip('KEY:') + ' DRUG '+ field[i+3]
                        else:
                            #all other 'normal" one 'word' feeder keys
                            fdrkey=field[i+1].lstrip('KEY:') #lstrip accounts for 'E'in fdrkey
                            
                        #when result has no data it is a blank line
                        ##print('20-result-line=', result_line)
                        if result_line != None:
                            with open('9522_new.csv', 'a') as output_file:
                                #prod rstrip to remove end whitespace
                                list_2_line=dept+','+prod.rstrip()+','+ipnum+','+rptseq+','+fdrsys+','+fdrkey
                                #print('list 2 line=',list_2_line)
                                output_file.write(list_2_line+'\n')
                                result=''
                                list_2_line=''
                
           

if __name__ == '__main__':
    with open('9522.txt', 'r') as input_file:
        process_file(input_file)


