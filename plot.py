import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import sys
import time

def choose_DIMM(addr,config_dict):
    num_bits = 3 #TODO change to dynamic
    DIMM_num = 0
    for i in range (0,num_bits):
        DIMM_num |= ((addr>>(config_dict['DIMMBits'][i])) & 1)<<i
    return DIMM_num

def choose_bank(addr,config_dict):
    num_bits = 2 #TODO change to dynamic
    bank_num = 0
    for i in range (0,num_bits):
        bank_num |= ((addr>>(config_dict['BaBits'][i])) & 1)<<i
    return bank_num

def choose_ch(addr,config_dict):
    ch_num = 0
    ch_num |= (addr>>config_dict['ChBits']) & 1
    return ch_num

def create_statistics():
    print "%s%s%s" %("saving in ",output_folder,"/statistics.txt")
    file = open(output_folder+'/statistics.txt','w+')
    #DIMM stats
    file.write('DIMM Statistics\n')
    for i in range(0,len(DIMM_array)):
        perc = float(len(DIMM_array[i]))/float(total_errors)
        file.write('DIMM'+str(i+1)+':'+str(perc)+'% of errors\n')

    #Bank stats
    file.write('\nBank Statistics\n')
    for i in range(0,len(bank_array)):
        perc = float(len(bank_array[i]))/float(total_errors)
        file.write('Bank'+str(i+1)+':'+str(perc)+'% of errors\n')

    #Channel stats
    file.write('\nChannel Statistics\n')
    for i in range(0,len(ch_array)):
        perc = float(len(ch_array[i]))/float(total_errors)
        file.write('Channel'+str(i+1)+':'+str(perc)+'% of errors\n')

    

def create_DIMMPlot(DIMM_array):
    #use a plot per dimm
    for i in range(1,num_dimms+1):
        plt.figure(i)
        plt.figure(i).clear()
        title = "Dimm "+`i`
        plt.title(title)
        plt.axis([0,0xFFFFF,0,0xFFF]);
        plt.ylabel('Offset')
        plt.xlabel('Page')
        axes=plt.gca()
        axes.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
        axes.get_yaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
        page_array = []
        offset_array = []

    for i in range(0,len(DIMM_array)):
        for j in DIMM_array[i]:
            page_array += [(j & 0xFFFFF000)>>12]
            offset_array += [j & 0xFFF]
    
        plt.figure(i+1)
        plt.plot(page_array,offset_array,'r,',alpha=.7)
        page_array = []
        offset_array = []

    #show/save plot
    #plt.show()
    print "%s%s%s" %("saving in ",output_folder,"/DIMMGraphs.pdf")
    pp=PdfPages(output_folder+'/DIMMGraphs.pdf')
    for i in range(1,num_dimms+1):
        pp.savefig(plt.figure(i))
    pp.close()
#end create_DIMMPlot

def create_BankPlot(Bank_array):
    #use a plot per bank
    for i in range(1,num_banks+1):
        plt.figure(i)
        plt.figure(i).clear()
        title = "Bank "+`i`
        plt.title(title)
        plt.axis([0,0xFFFFF,0,0xFFF]);
        plt.ylabel('Offset')
        plt.xlabel('Page')
        axes=plt.gca()
        axes.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
        axes.get_yaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
        page_array = []
        offset_array = []

    for i in range(0,len(bank_array)):
        for j in bank_array[i]:
            page_array += [(j & 0xFFFFF000)>>12]
            offset_array += [j & 0xFFF]
    
        plt.figure(i+1)
        plt.plot(page_array,offset_array,'r,',alpha=.7)
        page_array = []
        offset_array = []

    #show/save plot
    #plt.show()
    print "%s%s%s" %("saving in ",output_folder,"/BankGraphs.pdf")
    pp=PdfPages(output_folder+'/BankGraphs.pdf')
    for i in range(1,num_banks+1):
        pp.savefig(plt.figure(i))
    pp.close()
#end create_BankPlot

def create_chPlot(ch_array):
    #use a plot per channel
    for i in range(1,num_chs+1):
        plt.figure(i)
        plt.figure(i).clear()
        title = "Channel "+`i`
        plt.title(title)
        plt.axis([0,0xFFFFF,0,0xFFF]);
        plt.ylabel('Offset')
        plt.xlabel('Page')
        axes=plt.gca()
        axes.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
        axes.get_yaxis().set_major_formatter(ticker.FormatStrFormatter("%x"))
        page_array = []
        offset_array = []

    for i in range(0,len(ch_array)):
        for j in ch_array[i]:
            page_array += [(j & 0xFFFFF000)>>12]
            offset_array += [j & 0xFFF]
    
        plt.figure(i+1)
        plt.plot(page_array,offset_array,'r,',alpha=.7)
        page_array = []
        offset_array = []

    #show/save plot
    #plt.show()
    print "%s%s%s" %("saving in ",output_folder,"/ChannelGraphs.pdf")
    pp=PdfPages(output_folder+'/ChannelGraphs.pdf')
    for i in range(1,num_chs+1):
        pp.savefig(plt.figure(i))
    pp.close()
#end create_ChPlot

#return dictionary of items
def parse_config():
    config_dict = {}
    file_name = sys.argv[2]
    fileHandle = open(file_name,'r')
    file_str = fileHandle.read()
    fileHandle.close()
    file_str = file_str.split("\n")
    for line in file_str:
        split = line.split(":")
        if (split[0] == "Num DIMMs"):
            config_dict['NumDIMMs'] = int(split[1])
        elif (split[0] == "Channel Bits"):
            config_dict['ChBits'] = int(split[1])
        elif (split[0] == "Bank Bits"):
            config_dict['BaBits'] = [int(split[1].split(",")[0]),int(split[1].split(",")[1])]
        elif (split[0] == "DIMM Bits"):
            config_dict['DIMMBits'] = [int(split[1].split(",")[0]),int(split[1].split(",")[1]),int(split[1].split(",")[2])]
    return config_dict

#MAIN
t0 = time.clock()
#parse config options
config_dict = parse_config()
#create plots
num_dimms = config_dict['NumDIMMs']
num_banks = 4 #TODO make dynamic
num_chs = 2

#get addr range and stride from file
begin_addr = 0
end_addr = 0
stride = 0
total_errors = 0

#initialize arrays for graphs
DIMM_array = []
for i in range(0,num_dimms):
    DIMM_array += [[]]
bank_array = []
for i in range(0,num_banks):
    bank_array += [[]]
ch_array = []
for i in range(0,num_chs):
    ch_array += [[]]

#get output folder
output_folder = sys.argv[3]

file_name = sys.argv[1]
fileHandle = open(file_name,'r')
file_str = fileHandle.read()
fileHandle.close()
file_str = file_str.split("\n")
for line in file_str:
    split = line.split(":")
    if (split[0] == "Errors"):
        total_errors += int(split[1],16)
    elif (split[0] == "Stride"):
        stride = int(split[1],16)
    elif (split[0] == "High Addr"):
        end_addr = int(split[1],16)
    elif (split[0] == "Low Addr"):
        begin_addr = int(split[1],16)
        #run through range
        temp_addr = begin_addr
        while (temp_addr<=end_addr):
            DIMM_array[choose_DIMM(temp_addr,config_dict)] += [temp_addr]
            bank_array[choose_bank(temp_addr,config_dict)] += [temp_addr]
            ch_array[choose_ch(temp_addr,config_dict)] += [temp_addr]
            temp_addr += stride

#create plots
create_DIMMPlot(DIMM_array)
create_BankPlot(bank_array)
create_chPlot(ch_array)

#create statistics
create_statistics()

print "seconds to complete: ",time.clock()-t0
