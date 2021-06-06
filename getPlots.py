#!/home/emanners/Crypto/Chia/chia-blockchain/venv/bin/python3

import subprocess

def checkForPlots():
    print('Hello fron CheckForPlots')
    if isPlotDirEmpty():
        return 0
    else:
        print("Copying plots")
        return 1
def copyPlotsToFarmer():
    print('Hello fron copyPlotsToFarmer')
    command = '/usr/bin/ssh ' + getHost(plotter) + ' \'ls ' + getPlotDir(plotter) + '\''
    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    num_plots,err = result.communicate()
    plot_list = getPlotFullPath(num_plots)
    # We need to do some cleanup
    # First we remove the first 2 characters from the first index in the array.
    plot_list[0] = plot_list[0][2:]
    # Second we remove/pop the last index from the array.
    del plot_list[-1]

    print('\nCopying plots with temorary names....')
    for src_plot in plot_list:
        command2= 'scp ' + getHost(plotter) + ':' + src_plot + ' /media/emanners/WindowsChiaFinal/ChiaFinal/' + getPlotFile(src_plot) + '.bob'
        print(command2)
        #result = subprocess.Popen(command2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return 1
def isPlotDirEmpty():
    print('Hello fron isPlotDirEmtpy')
    command = '/usr/bin/ssh ' + getHost(plotter) + ' \'ls -l ' + getPlotDir(plotter) + ' | wc -l\''
    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    num_plots,err = result.communicate()
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
    return b.split('::')[1]
def getPlotFullPath(c):
    #print('Hello fron getPlotFullPath')
    plot_array = str(c).split('\\n')
    return plot_array
def getPlotFile(d):
    return d.split('FinChia/')[1]

#--------------------------- MAIN PART of the Code -------------------------#
# List of plotters
#plotters = ['ThreeLeaf-Left::C:/Users/emanners/Chia','ThreeLeaf-Right::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia']
#plotters = ['ThreeLeaf-Right::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia']
plotters = ['192.168.1.85::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia/plot*']
# Harvestor Final Plot Directory
harvestorPlotDir = '/media/emanners/WindowsChiaFinal/ChiaFinal'

for plotter in plotters:
    print(plotter)
    if checkForPlots():
      copyPlotsToFarmer()
    else:
      next


