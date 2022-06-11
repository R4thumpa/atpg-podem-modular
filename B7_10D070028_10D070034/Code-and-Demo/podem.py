import copy
f=open("netlist2.txt","r")
l=f.readlines();

def read_netlist():
    device_id=0; #id of the devices
    for i in range (0, len(l)): #iterate the entirety of the text file
        temp=l[i] #initialize temporary as content of netlist (per line)
        temp_str='' #initialize temporary string
        device=[] #initialize device list
        if(temp=='\n'): #if temporary is enter, reiterate
            continue
        else:
            device.append(device_id) #appends current device into device list
            device_id=device_id+1 #next device is +1 of current device's id
            
        for j in range (0, len(temp)): #iterate the entirety of the line
            if (j==len(temp)-1): #if counter reaches 1 letter before the end of the word
                if (temp[j] != ' ' or temp[j] == '\n'):#if letter is enter or space
                    if(temp_str): #if letter is not empty
                        device.append(temp_str) #append temp string to device
                        temp_str='' #reset letter
                else: 
                    if(temp_str): #if letter is not empty
                        device.append(temp_str) #append temp string to device
                        temp_str='' #reset letter
            elif (temp[j] !=' '): #elseif counter isn't 1 letter before end of word, and content isn't space
                temp_str = temp_str + temp[j] #add content of temp[counter] to temp string
                
            else: #last temp string append to make sure it misses nothing
                if(temp_str):
                    device.append(temp_str)
                temp_str=''
        netlist.append(device) #device gets appended to netlist as a whole
    
def convert_netlist():
    
    temp=1 #temporary counter
    
    node_old =[] #list for old nodes
    node_new =[] #list for new nodes
    for i in range (0, len(netlist)): #iterates through netlist 
        
        if (netlist[i][1][:5] == 'and2_'): #assigns each device with a device id (devices are on the 1st column of every row)
            netlist[i][1] = 3
        elif (netlist[i][1][:4] == 'or2_'): 
            netlist[i][1] = 2
        elif (netlist[i][1][:3] == 'not'):
            netlist[i][1] = 1
        elif (netlist[i][1][:6] == 'nand4_'):
            netlist[i][1] = 8
        elif (netlist[i][1][:6] == 'nand2_'):
            netlist[i][1] = 5
        elif (netlist[i][1][:5] == 'nor2_'):
            netlist[i][1] = 4
            
        for j in range (2,len(netlist[i])): #iterates through netlist, skipping over device id (0) and gate type (1), straight towards output node (2), and input node (3)
            if (netlist[i][j][:2] == 'in'): #if the node has primary input
                match=0 #match
                for k in range (0, len(node_old)): #iterates through old node
                    if (netlist[i][j] == node_old[k]): #if netlist's node is old
                        match=1 #match and break
                        break
                        
                if (match): #if match = 1
                    netlist[i][j]=node_new[k] #insert new node
                else:
                    ins.append(temp) #appends temp into ins
                    node_old.append(netlist[i][j]) #appends current netlist to old node
                    node_new.append(temp) #appends temp into new node
                    netlist[i][j]=temp #insert temp into netlist
                    temp=temp+1 #increment temp
                    
            elif (netlist[i][j][:3] == 'out'): #elif the node has primary output
                match=0 #match 
                for k in range (0, len(node_old)): #iterates through old node
                    if (netlist[i][j] == node_old[k]): #if netlist's node is old
                        match=1 #match and break
                        break
                        
                if (match): #same as before
                    netlist[i][j]=node_new[k]
                else:                    
                    outs.append(temp)
                    node_old.append(netlist[i][j])
                    node_new.append(temp)
                    netlist[i][j]=temp
                    temp=temp+1
            else: #if only device
                match=0 #match
                for k in range (0, len(node_old)): #same as before
                    if (netlist[i][j] == node_old[k]):
                        match=1
                        break
                        
                if (match): #same as before
                    netlist[i][j]=node_new[k]
                else:
                    node_old.append(netlist[i][j])
                    node_new.append(temp)
                    netlist[i][j]=temp
                    temp=temp+1
    for i in range(0, len(node_old)):
        temp2 = []
        temp2.append(node_old[i])
        temp2.append(node_new[i]) 
        node_map.append(temp2) #creates nodemap out of old and new node
    return (temp-1) #returns the temp-1

def values_initial (no_nodes): #makes initial values into nodes (initial values are -5)
 
    for i in range (0, no_nodes+1):
        node_values.append(-5) 

def nand_out(o,i1,i2,g): #nand gate o is output, i1 and i2 are inputs, and g is flag. 0 for backtrace and 1 for imply

    if (g==0): #if backtrace
        if(o == -5): #if initial values
            i1=i1 #assign input/outputs
            i2=i2
            o=o;      
        elif(o == 0): #if output zero
            i1 = 1; i2 = 1 #inputs must be both 1s
        elif(o == 1): #if output one
            if (i1 == 1): #if 1st in is one
                i2= 0 #2nd in must be zero
            elif(i2 == 1): #if 2nd in is one
                    i1= 0 #1st in must be zero
            elif (i1== 0): #likewise, if it's zero, then the other input are don't care
                i2= i2
            elif (i2== 0):
                i1= i1;
            else: #if all else fails, double zero
                i1=0;
                i2=0;


    else: #if imply
        if(i1 == -5 and i2 == -5): #if initial
            o =-5 #set output to initial
        else: 
            o1 = (i1 and i2) 
            if(abs(o1)>1): #if it's not a bit
                o = -5 #return to initial
            else:
                o = int(not(o1)) #if not just return the output
    return[o,i1,i2] 

def not_out(o,i1,g): #not gate
    if(g==0): #if backtrace
        if(o==-5): #if initial
            i1 = -5; #set input to initial
        else:    
            i1 = int(not(o)) #if not just not
    else: #if imply
        if(i1==-5): #if initial
            o = -5 #set out initial
        else:    
            o = int(not(i1)) #if not just not
    return[o,i1]

def or_out(o,i1,i2,g): #or gate
    if (g==0): #if backtrace
        if(o == -5): #if output initial
            i1= i1 #set input and output
            i2= i2
            o=o    
        elif(o == 1): #if output 1
            if (i1 == 0): #if i1 zero
                i2 = 1 #therefore i2 must be 1
            elif (i2 == 0): #likewise
                i1 = 1
            elif (i1 == 1): #if i1 one
                i2 = i2 #therefore i2 don't care
            elif (i2 == 1): #likewise
                i1 = i1
            else: #if all else fails, set both to one
                i1 = 1 
                i2 = 1
        elif(o == 0): #if output 0
            i1 = 0; i2 = 0 #therefore both inputs must be 0
    else: #if imply
        if(i1 == -5 and i2 == -5): #if both initials
            o =-5; #set output as initial
        else: #if imply
            o1 = (i1 or i2) #or both of them
            if(abs(o1)>1): #if not binary 
                o = -5 #return to initial
            else:
                o = o1; #else just return
    return[o,i1,i2]

def nor_out(o,i1,i2,g): #nor gate
    if (g==0): #if backtrace
        if(o == -5): #if output initial
            i1= i1 #set input and output
            i2= i2
            o=o    
        elif(o == 0): #if output 0
            if (i1 == 0): #if i1 zero
                i2 = 1 #therefore i2 must be 1
            elif (i2 == 0): #likewise
                i1 = 1
            elif (i1 == 1): #if i1 one
                i2 = i2 #therefore i2 don't care
            elif (i2 == 1): #likewise
                i1 = i1
            else: #if all else fails, set both to one
                i1 = 1 
                i2 = 1
        elif(o == 1): #if output 1
            i1 = 0; i2 = 0 #therefore both inputs must be 0
    else: #if imply
        if(i1 == -5 and i2 == -5): #if both initials
            o =-5; #set output as initial
        else: #if imply
            o1 = (i1 or i2) #or both of them
            if(abs(o1)>1): #if not binary 
                o = -5 #return to initial
            else:
                o = int(not(o1)); #else just return
    return[o,i1,i2] 

def and_out(o,i1,i2,g): #and gate
    if (g==0): #if backtrace
        if(o == -5): #if initials
            i1= i1 #set up input output 
            i2= i2
            o=o   
        elif(o == 1): #if output 1
            i1 = 1; i2 = 1; #therefore input
        elif(o == 0): #if output 0
            if (i1 == 1): #if i1 is one
                i2= 0 #therefore i2 is 0
            elif(i2 == 1): #likewise
                i1= 0
            elif(i1== 0): #if i1 is zero
                i2= i2 #i2 is don't care
            elif(i2== 0): #likewise
                i1= i1
            else: #if all else fails, inputs equal zero
                i1=0 
                i2=0
    else: #if imply
        if(i1 == -5 and i2 == -5): #if initials
            o =-5 #output initials
        else:
            o1 = (i1 and i2) 
            if(abs(o1)>1): #if not binary
                o = -5 #set initials
            else:
                o = o1 #if not just and
    return[o,i1,i2] 

def nand_4input(o,i1,i2,i3,i4,g): #nand gate 4 inputs, not used
    if(g==0):
        if(o==-5):
            i1 = i2 = i3 = i4 = -5;
        if(o == 0):
            i1 = i2 = i3 = i4 = 1;
        elif (o==1): 
            i1 = 0;
    elif(g==1):
        o1 = (i1*i2*i3*i4) ;
        if(abs(o1)>1): 
            o = -5;
        else:
            o = int(not(o1));
    return(o,i1,i2,i3,i4);
         
def Type(V,row): #type, checks type of gate, then calls gate function, then updates the row with updated values
    g=0; #initialize g
    row_update = copy.deepcopy(row) #deepcopies row to update
    if(V == -5): #if initial
        row_update = copy.deepcopy(row) #deepcopy row again
        print('Value of V is not allowed') #print error
    else: #if not
        if(int(row[1])==1): #checks which device, and updates it
            row_update[2:5] =  not_out(V, row[3], g)
        elif(int(row[1])==2):
            row_update[2:5] =  or_out( V, row[3], row[4], g)
        elif(int(row[1])==3):
            row_update[2:5] =  and_out( V, row[3], row[4], g)
        elif(int(row[1])==4):
            row_update[2:5] =  nor_out( V, row[3], row[4], g)
        elif(int(row[1])==5):
            row_update[2:5] =  nand_out( V, row[3], row[4], g)
        elif(int(row[1])==8):
            row_update[2:7] =  nand_4input( V, row[3], row[4], row[5], row[6],g)
    return row_update

def update_rowvalues(device_id): #used update the values of the rows
    rowvector=[] #vector of the rows 
    rowvector.append(device_id) #appends the device id into the vector
    rowvector.append(netlist[device_id][1]) #appends the netlist into the vector
    
    for i in range (2, len(netlist[device_id])): #iterates through the netlist to append node values
        rowvector.append(node_values[netlist[device_id][i]])

    return rowvector #returns the vector

def backtrace(nG, nV): #backtraces
    for i in range (0,len(netlist)): #iterates through netlist
        if (int(netlist[i][2]) == nG): #if netlist equals to ng
            row_values = update_rowvalues(i) #update rowvalues
            row_v = Type(nV,row_values) #checks type of gate, then calls gate function, then updates the row with updated values

            for j in range (0, len(row_v)-3): #iterates through the row, except the last 3 parts
                g = int(netlist[i][3+j]) 
                v = row_v[3+j];
                m =  [g,v]
                stack_G.append(m)
              
def objective(nG, nV): #objective that uses backtrace function. backtraices until it meets a primary input, then PI flag is asserted.
    isPI=0
    while(nV !=-5 and isPI == 0):
        
        
        for i in range (0, len(ins)):
            if (nG == ins[i]):
                isPI=1
                break
        if (isPI==1):
            return (nG, nV)
        else:
            backtrace(nG,nV)
            
            if(stack_G):
                (nG,nV) = stack_G.pop()
            #isPI=0
        
    return (nG, nV)

def type_imply(row_imply):  #same as type but used in imply
    g=1
    row_update = copy.deepcopy(row_imply)
    temp = int(row_imply[1])
    if(temp==1):
        [row_update[2],row_update[3]]= not_out(row_update[2], row_imply[3],g)
    elif(temp==2):
        [row_update[2],row_update[3],row_update[4]] = or_out( row_update[2], row_imply[3], row_imply[4],g)
    elif(temp==3):
        [row_update[2],row_update[3],row_update[4]] = and_out( row_update[2], row_imply[3], row_imply[4],g)
    elif(temp==4):
        [row_update[2],row_update[3],row_update[4]] = nor_out(row_update[2], row_imply[3], row_imply[4], g)
    elif(temp==5):
        [row_update[2],row_update[3],row_update[4]] = nand_out(row_update[2], row_imply[3], row_imply[4], g) 
    elif(temp==8):
        [row_update[2],row_update[3],row_update[4],row_update[5],row_update[6]] = nand_4input( row_update[2], row_imply[3], row_imply[4], row_imply[5], row_imply[6],g)
    return row_update



def cnctd_devices (c_Node): #idex devices
    device_index = []
    for i in range (0,len(netlist)):
        for j in range(3,len(netlist[i])):
            if(c_Node == netlist[i][j]):
                device_index.append(i)
                
    return device_index

def create_devicemap(): #finds device connected to each node once
    
    for i in range (0, len(netlist)):
        
        device_map.append (cnctd_devices (netlist[i][2]));


def imply_device(device_id): #calls type_imply that evaluates the output node values, also updates the nove_values arrays
    
    row_imply = update_rowvalues(device_id)
    row_update = type_imply(row_imply)
    node_values [netlist[device_id][2]] = row_update[2]

       
def imply(PI, PI_Value): #simulates the circuit logically depending on the PIs
    count_OUT = [] #searches for gates in netlist where PI node is an input, stores in device_connected array
    flag = 0 
    node_values[PI] = PI_Value
    device_connected_next = []
    while (len(count_OUT) != len(outs)): #runs a while loop that runs until all primary outputs are implied
        #(len(count_OUT) != len(outs)):
        #device_connected_next = []
        #device_connected = []
        
        if(flag==0):
            flag = 1
            device_connected = cnctd_devices(PI)
            for i in range (0, len(device_connected)):
                imply_device(device_connected[i])
                       
        else:
            flag = flag +1
            device_connected = device_connected_next
            device_connected_next = []
            
            for i in range(0, len(device_connected)):
                imply_device(device_connected[i])
            
            
           
        next_d = []
        
        for i in range (0, len(device_connected)):
                device_map_copy = copy.deepcopy(device_map)
                next_d = device_map_copy[device_connected[i]]
            
            # check if temp_d is empty
                if (len(next_d)==0):
                    
                    match_out = False
                    
                    for i1 in range (0, len(count_OUT)):
                        if (count_OUT[i1] == device_connected[i]):
                            match_out = True
                            break
                    if (~match_out):
                        count_OUT.append(device_connected[i])
                   
                if(next_d):
                        x = -1
                        while (len(next_d) > 0):
                            x = next_d.pop()
                            match_12 = False
                            for i2 in range(0, len(device_connected_next)):                         
                                
                                if(x==device_connected_next[i2]):
                                    match_12 = True
                                    break
                                    
                            if(~match_12):
                                    device_connected_next.append(x)
        # Values[i][j] = copy.deepcopy(V_temp); 
        #flag = 5 
        #break     
#****************************************************************************


def main_podem(nG_C, nV):
    read_netlist()
    no_nodes = convert_netlist()
    create_devicemap()
    values_initial(no_nodes)
    for i in range(1, len(node_map)):
        if(nG_C == node_map[i][0]):
            nG = node_map[i][1]
            FL = node_map[i][1]
            
    (PI, PI_V) = objective(nG, nV)
    imply(PI, PI_V)
    
    while(node_values[FL] == -5):
        if(stack_G):
            (nG,nV) = stack_G.pop()
        else:
            print("Error")
            return
        (PI, PI_V) = objective(nG, nV)
        imply(PI, PI_V)
    #

    #NCV = [-5,-5,1,-5,1,-5,-5,1];
    index_arr =  cnctd_devices(FL)
    k = len(index_arr)
    if(k==0):
        #fault at primary output
        if (FV==node_values[FL] ):
            print('Fault is detectable')
        else:
            print('Fault is not detectable')
    
    for j in range (0, len(index_arr)):
        count = 0 ;
        nc_value = 1#NCV[int(netlist[index_arr[j]][1])]
        connected_in = netlist[index_arr[j]][3:len(netlist[index_arr[j]])]
        for p in range(0, len(connected_in)):
            if(connected_in[p] != FL):
                if(node_values[connected_in[p]] == -5):
                    (PI, PI_V) = objective(connected_in[p], nc_value)
                    imply(PI, PI_V)
                    if(node_values[connected_in[p]] == nc_value):
                        count = count + 1;
                elif(node_values[connected_in[p]] == nc_value): 
                    count = count +1
                elif(node_values[connected_in[p]] == (1-nc_value)):
                    print('Test not detected')
                    break
        if(count == (len(connected_in)-1)): 
            print('Fault is detectable')
            print (' ')
            print('Primary Input values are:')
            for i in range (0, len(ins)):
                if(node_values[ins[i]]==-5):
                    print ('Node',node_map[ins[i]][0]," ",'x')
                else:
                    print ('Node',node_map[ins[i]][0]," ",node_values[ins[i]])

        else:
            print('Fault is not detectable')
    
    return (PI, PI_V)

netlist=[]
node_values = []        
ins=[]
outs=[]
device_map = []
stack_G = []
node_map=[[]]

# ------------------------------------------------#
# Define Fault_Location and Fault_Location here   #
# ------------------------------------------------#
Fault_Location = 'n4'
Fault_Value = 0
# ------------------------------------------------#
# ------------------------------------------------#

FL = 0
FV = Fault_Value

print ('Fault Location', Fault_Location)
print ('Fault Value', FV)
print (' ')
main_podem(Fault_Location,FV)