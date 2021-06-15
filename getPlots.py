#!/home/emanners/Crypto/Chia/chia-blockchain/venv/bin/python3

# Author: Edson Manners
# TODO: Enable copying from both harvestors

# Install smbclient on Ubuntu
# sudo apt install smbclient
# --
# https://docs.python.org/3/howto/logging.html
import logging
import subprocess
#import sleep from time
import time
# --

def checkForPlots(os):
    print('Hello fron CheckForPlots')
    if isPlotDirEmpty(os):
        return 0
    else:
        print("Copying plots")
        return 1
def copyPlotsToFarmer(os):
    # print('Hello fron copyPlotsToFarmer')
    # Get list of plots on Plotter
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

    print('\nCopying plots with temporary names....')

    # Check for stale plots then copy the rest
    for src_plot in plot_list:
        # Check if this plot is already been copied and print it for manual deletion
        print(src_plot)
        if os == 'Linux':
          if isStalePlot(getPlotFile(src_plot)):
            print(getPlotFile(src_plot) + "... Exists on the Harvestor, skipping. Please delete from Source!")
            continue
        elif os == 'Windows':
          if isStalePlot(src_plot):
            print(src_plot + "... Exists on the Harvestor, skipping. Please delete from Source!")
            continue
        # Create command to copy file to Harvestor
        if os == 'Linux':
            command2 = 'scp ' + getHost(plotter) + ':' + src_plot + ' ' + harvestorPlotDir + '/' + getPlotFile(src_plot) + '.bob'
        elif os == 'Windows':
            command2 = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "get ' + src_plot + ' ' + harvestorPlotDir + '/' + src_plot + '.bob"'
        # Copy the plot
        print(command2)
        result = subprocess.Popen(command2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        copy_status,err = result.communicate()
        print(copy_status)
        # Rename the plot
        if os == 'Linux':
          print('mv ' + harvestorPlotDir + '/' + getPlotFile(src_plot) + '.bob ' + getPlotFile(src_plot))
          #command3 = 'mv ' + harvestorPlotDir + '/' + getPlotFile(src_plot) + '.bob ' + getPlotFile(src_plot)
        if os == 'Windows':
          print('mv ' + harvestorPlotDir + '/' + src_plot + '.bob ' + src_plot)
          #command3 = 'mv ' + harvestorPlotDir + '/' + src_plot + '.bob ' + src_plot
    return 1

def isPlotDirEmpty(os):
    #print('Hello fron isPlotDirEmtpy')
    if os == 'Linux':
        command = '/usr/bin/ssh ' + getHost(plotter) + ' \'ls -l ' + getPlotDir(plotter) + ' | wc -l\''
    elif os == 'Windows':
        logging.info('smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"')
        command = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"'
    else:
        print('No OS defined... leaving')

    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    returnCode = result.poll()

    if 'None' in str(returnCode):
        time.sleep(5)
        returnCode = result.poll()
        print(returnCode)
    else:
        

    print(returnCode)
    #-- If the return code is valid we can continue to process the plots
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

def checkForStalePlots():
    print('Hello fron checkForStalePlots')
    # Create an array of all of the current plots
    command = 'ls -l ' + harvestorPlotDir + ' | tr -s " " | cut -d " " -f9'
    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    farmPlotArray,err = result.communicate()
    permPlots = cleanCMDOutput(str(farmPlotArray).split('\\n'))
    return permPlots
def getHost(a):
    return a.split('::')[0]
def getPlotDir(b):
    return b.split('::')[2]
def getPlotFullPath(c):
    #print('Hello fron getPlotFullPath')
    plot_array = str(c).split('\\n')
    return plot_array
def getPlotFile(d):
    return d.split('ChiaFin/')[1]
def getPlotOS(e):
    print('Hello fron getPlotOS')
    return e.split('::')[1]
def cleanCMDOutput(f):
    del f[0]
    del f[-1]
    return f
def isStalePlot(g):
    #print('Hello fron isStalePlot')
    if g in harvestorPlotArray:
      return 1
    else:
      return 0


#--------------------------- MAIN PART of the Code -------------------------#
# List of plotters
#plotters = ['ThreeLeaf-Left::Windows::/ChiaTmp','ThreeLeaf-Right::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia']
#plotters = ['ThreeLeaf-Right::Linux::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/FinChia']
#--
plotters = ['192.168.1.50::Windows::ChiaFin/','192.168.1.85::Linux::/media/emanners/822cf109-0675-41f0-a401-3a237d4cdf65/ChiaFin/plot*']
# Harvestor Final Plot Directory
harvestorPlotDir = '/media/emanners/WindowsChiaFinal/ChiaFinal'
harvestorPlotArray = []
#
## Fix later ## logging.basicConfig(filename='getPlots.log', encoding='utf-8', level='logging')

for plotter in plotters:
    print(plotter)
    # Check if plots new plots exist
    if checkForPlots(getPlotOS(plotter)):
      # If new plots exist, create an array of current plots then copy new ones to the farmer
      harvestorPlotArray = checkForStalePlots()
      copyPlotsToFarmer(getPlotOS(plotter))
    else:
      next
