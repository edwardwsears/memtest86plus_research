import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import time

def add_range(begin_addr,end_addr,stride):
    temp = begin_addr
    addr_array = []
    page_array = []
    offset_array = []
    
    while (temp<=end_addr):
        addr_array += [temp]
        temp += stride

    for index in addr_array:
        page_array += [(index & 0xFFFFF000)>>12]
        offset_array += [index & 0xFFF]
    
    plt.plot(page_array,offset_array,'ro')
    print "added range"



#MAIN
#create plot
t0 = time.clock()
plt.axis([0,0xFFFFF,0,0xFFF]);
plt.ylabel('Offset')
plt.xlabel('Page')
axes=plt.gca()
axes.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
axes.get_yaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))

#get addr range and stride from file
begin_addr = 0
end_addr = 0
stride = 0
file_name = sys.argv[1]
fileHandle = open(file_name,'r')
file_str = fileHandle.read()
fileHandle.close()
file_str = file_str.split("\n")
for line in file_str:
    split = line.split(":")
    if (split[0] == "Stride"):
        stride = int(split[1],16)
    elif (split[0] == "High Addr"):
        end_addr = int(split[1],16)
    elif (split[0] == "Low Addr"):
        begin_addr = int(split[1],16)
        #call fn
        add_range(begin_addr,end_addr,stride)

print "seconds to complete: ",time.clock()-t0
#show plot
plt.show()
