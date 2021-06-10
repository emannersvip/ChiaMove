#!/home/emanners/Crypto/Chia/chia-blockchain/venv/bin/python3

# Read all plots already copied and skip/delete the source
#f = open("demofile2.txt", "a")
#f.write("Now the file has more content!")
#f.close()

##open and read the file after the appending:
#f = open("demofile2.txt", "r")
#print(f.read())

# Author: Edson Manners

# Install smbclient on Ubuntu
# sudo apt install smbclient
import subprocess

def checkForPlots(os):
    print('Hello fron CheckForPlots')
    if isPlotDirEmpty(os):
        return 0
    else:
        print("Copying plots")
        return 1
def copyPlotsToFarmer(os):
    print('Hello fron copyPlotsToFarmer')
    if os == 'Linux':
        command = '/usr/bin/ssh ' + getHost(plotter) + ' \'ls ' + getPlotDir(plotter) + '\''
    elif os == 'Windows':
        command = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"'
    else:
        print('No OS defined... leaving')

    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    num_plots,err = result.communicate()
    plot_list = getPlotFullPath(num_plots)
    # We need to do some cleanup
    # First we remove the first 2 characters from the first index in the array.
    plot_list[0] = plot_list[0][2:]

    if os == 'Linux':
        # Second we remove/pop the last index from the array.
        del plot_list[-1]
    elif os == 'Windows':
        # Remove the current and parent working directory and last 4 useless entries in the array.
        del plot_list[0]
        del plot_list[0]
        del plot_list[-1]
        del plot_list[-1]
        del plot_list[-1]
        #Clean up the strinmg to just get the individual plot file names.
        for plot_file in range(0, len(plot_list)):
            plot_list[plot_file] = plot_list[plot_file].split()[0]
            #print(plot_list[plot_file])
    else:
        print('No OS defined... leaving')

    print('\nCopying plots with temorary names....')
    for src_plot in plot_list:
        if os == 'Linux':
            command2 = 'scp ' + getHost(plotter) + ':' + src_plot + ' /media/emanners/WindowsChiaFinal/ChiaFinal/' + getPlotFile(src_plot) + '.bob'
        elif os == 'Windows':
            command2 = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "get ' + src_plot + ' /media/emanners/WindowsChiaFinal/ChiaFinal/' + src_plot + '.bob"'
#smbclient //THREELEAF-LEFT/ChiaFin -U "Edson Manners%L3m0ns&P3ach3s" -c "get plot-k32-2021-06-02-10-18-f9204d0c78d3088efb86be588867d7287e9e75dea048cab8750941b3fdefacfa.plot /media/emanners/WindowsChiaFinal/ChiaFinal/plot-k32-2021-06-02-10-18-f9204d0c78d3088efb86be588867d7287e9e75dea048cab8750941b3fdefacfa.plot.bob"
        print(command2)
        result = subprocess.Popen(command2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        copy_status,err = result.communicate()
        print(copy_status)
    return 1

def isPlotDirEmpty(os):
    print('Hello fron isPlotDirEmtpy')
    if os == 'Linux':
        command = '/usr/bin/ssh ' + getHost(plotter) + ' \'ls -l ' + getPlotDir(plotter) + ' | wc -l\''
    elif os == 'Windows':
        print('smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"')
        command = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"'
    else:
        print('No OS defined... leaving')

    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    num_plots,err = result.communicate()
    # We can't do a grep in Windows so this hack of checkign for plot files after doign a dir on the directory will have to do.
    # I should just use this check for Linux in the future since this way works better for both OSes.
    if os == 'Windows':
        parse_result = str(num_plots).split('\\n')
        if str(num_plots).split('\\n')[2].find('plot'):
            num_plots = 1
    #Plot directory not empty
    if int(num_plots) > 0:
        print("Found plots")
        return 0
    #Plot directory empty
    else:
        print("No plots to copy!!")
        return 1

def getHost(a):
    return a.split('::')[0]
def getPlotDir(b):
    return b.split('::')[2]
def getPlotFullPath(c):
    #print('Hello fron getPlotFullPath')
    plot_array = str(c).split('\\n')
    return plot_array
def getPlotFile(d):
    return d.split('FinChia/')[1]
def getPlotOS(e):
    print('Hello fron getPlotOS')
    return e.split('::')[1]

#--------------------------- MAIN PART of the Code -------------------------#
# List of plotters
#plotters = ['ThreeLeaf-Left::Windows::/ChiaTmp','ThreeLeaf-Right::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia']
#plotters = ['ThreeLeaf-Right::Linux::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia']
#plotters = ['192.168.1.85::Linux::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia/plot*']
plotters = ['192.168.1.50::Windows::ChiaFin/']
# Harvestor Final Plot Directory
harvestorPlotDir = '/media/emanners/WindowsChiaFinal/ChiaFinal'

for plotter in plotters:
    print(plotter)
    if checkForPlots(getPlotOS(plotter)):
      copyPlotsToFarmer(getPlotOS(plotter))
    else:
      next


