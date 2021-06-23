#!/home/emanners/Crypto/Chia/chia-blockchain/venv/bin/python3

# Author: Edson Manners
# TODO: Enable copying from both harvestors - DONE
# TODO: 06182021: Create plotter config file with lists of plotters
# TODO: 06182021: Make program cp SSH keys on first login

# Install smbclient on Ubuntu
# sudo apt install smbclient
# --
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
from colorama import Fore, Style
# https://docs.python.org/3/howto/logging.html
# https://realpython.com/python-logging/
import logging
# https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/
import os
import subprocess
#import sleep from time
import time
# --

def checkForPlots(os):
    logging.debug(getTimeStamp() + ' : Hello from CheckForPlots')
    if isPlotDirEmpty(os):
        return 0
    else:
        print("Copying plots")
        return 1
def copyPlotsToFarmer(os):
    logging.debug(getTimeStamp() + ' : Hello from copyPlotsToFarmer')
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
        print('SRC_PLOT: ' + str(src_plot))
        if os == 'Linux':
          if isStalePlot(getPlotFile(src_plot)):
            deleteStalePlot(src_plot)
            continue
        elif os == 'Windows':
          if isStalePlot(src_plot):
            deleteStalePlot(src_plot)
            continue
        # Create command to copy file to Harvestor
        if os == 'Linux':
            command2 = 'scp ' + getHost(plotter) + ':' + src_plot + ' ' + harvestorPlotDir + '/' + getPlotFile(src_plot) + '.bob'
        elif os == 'Windows':
            command2 = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "get ' + src_plot + ' ' + harvestorPlotDir + '/' + src_plot + '.bob"'
        # Copy the plot
        #print(command2)
        result = subprocess.Popen(command2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        copy_status,err = result.communicate()
        #print(copy_status)
        # Rename the plot
        if os == 'Linux':
          print('mv ' + harvestorPlotDir + '/' + getPlotFile(src_plot) + '.bob ' + harvestorPlotDir + '/' + getPlotFile(src_plot))
          command3='mv ' + harvestorPlotDir + '/' + getPlotFile(src_plot) + '.bob ' + harvestorPlotDir + '/' + getPlotFile(src_plot)
        elif os == 'Windows':
          print('mv ' + harvestorPlotDir + '/' + src_plot + '.bob ' + harvestorPlotDir + '/' + src_plot)
          command3 = 'mv ' + harvestorPlotDir + '/' + src_plot + '.bob ' + harvestorPlotDir + '/' + src_plot
        result = subprocess.Popen(command3, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        returnCode = result.poll()
    return 1

def isPlotDirEmpty(os):
    logging.debug(getTimeStamp() + ' : Hello from isPlotDirEmtpy')
    if os == 'Linux':
        command = '/usr/bin/ssh ' + getHost(plotter) + ' \'ls -l ' + getPlotDir(plotter) + ' | wc -l\''
    elif os == 'Windows':
        logging.info(getTimeStamp() + ' : smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"')
        command = 'smbclient //' + getHost(plotter) + '/' + getPlotDir(plotter) + ' -U "Edson Manners%L3m0ns&P3ach3s" -c "dir"'
    else:
        print('No OS defined... leaving')

    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    returnCode = result.poll()

    #-- If the return code is valid we can continue to process the plots
    num_plots,err = result.communicate()
    #print('NUM_PLOTS: ' + str(num_plots))
    if not num_plots:
        return 1

    # We can't do a grep in Windows so this hack of checking for plot files after doign a dir on the directory will have to do.
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
    logging.debug(getTimeStamp() + ' : Hello from checkForStalePlots')
    # Create an array of all of the current plots
    command = 'ls -l ' + harvestorPlotDir + ' | tr -s " " | cut -d " " -f9'
    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    farmPlotArray,err = result.communicate()
    permPlots = cleanCMDOutput(str(farmPlotArray).split('\\n'))
    logging.debug(getTimeStamp() + ' : We have ' + str(len(permPlots)) + ' plots being farmed.')
    return permPlots
def getHost(a):
    return a.split('::')[0]
def getPlotDir(b):
    return b.split('::')[2]
def getPlotFullPath(c):
    logging.debug(getTimeStamp() + ' : Hello from getPlotFullPath')
    plot_array = str(c).split('\\n')
    return plot_array
def getPlotFile(d):
    logging.debug(getTimeStamp() + ' : Hello from getPlotFile')
    return d.split('ChiaFin/')[1]
def getPlotOS(e):
    logging.debug(getTimeStamp() + ' : Hello from getPlotOS')
    return e.split('::')[1]
def cleanCMDOutput(f):
    del f[0]
    del f[-1]
    return f
def isStalePlot(g):
    logging.debug(getTimeStamp() + ' : Hello from isStalePlot')
    if g in harvestorPlotArray:
      return 1
    else:
      return 0
def getTimeStamp():
    # https://docs.python.org/3/library/time.html
    return time.strftime('%b %d %H:%M:%S')
def checkHarvestorPlotDir(h):
    isdir = os.path.isdir(h)
    if isdir:
      return h
    else:
      print(getTimeStamp() + ' : Harvestor Plot directory does not exist... Exiting!')
      logging.critical(getTimeStamp() + ' : Harvestor Plot directory does not exist... Exiting!')
      print(getTimeStamp() + ' : ' + h + ' is missing!')
      logging.info(getTimeStamp() + ' : ' + h + ' is missing!')
      logging.info(getTimeStamp() + ' : --------------------------------STOP-------------------------------------')
      exit()
def deleteStalePlot(i):
    # We really only rename them
    logging.debug(getTimeStamp() + ' : Hello from isStalePlot')
    logging.debug(getTimeStamp() + ' : ' + getPlotFile(i) + "... Exists on the Harvestor, skipping. Deleting from Source!")
    logging.debug(getTimeStamp() + ' : scp ' + getHost(plotter) + ' "mv ' + i + ' ' + i + '.deleteme"')
    command='ssh ' + getHost(plotter) + ' "mv ' + i + ' ' + i + '.deleteme"'

    result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    deleted,err = result.communicate()
    return


#--------------------------- MAIN PART of the Code -------------------------#
#
# Change 'logging level' to match the verbosity that required.
logging.basicConfig(filename='getPlots.log', level=logging.DEBUG, format='%(message)s - %(levelname)s')
logging.info(getTimeStamp() + ' : --------------------------------START------------------------------------')

# List of plotters
# For now *Linux* Plotters MUST use wildcard on the plot directory!!
plotters = ['192.168.1.84::Linux::/mnt/Plots/ChiaFin/*.plot',
            '192.168.1.85::Linux::/media/emanners/40f6ed33-7153-40a2-ad49-20eaf9e38c71/ChiaFin/*.plot']
# Harvestor Final Plot Directory
harvestorPlotDir = checkHarvestorPlotDir('/media/emanners/WindowsChiaFinal/ChiaFinal')
harvestorPlotArray = []

for plotter in plotters:
    logging.info(getTimeStamp() + ' : ' + plotter)
    print(getTimeStamp() + ' : ' + plotter)
    print(f'This is {Fore.GREEN}color{style.RESET_ALL}!')
    # Check if plots new plots exist
    if checkForPlots(getPlotOS(plotter)):
      # If new plots exist, create an array of current plots then copy new ones to the farmer
      harvestorPlotArray = checkForStalePlots()
      copyPlotsToFarmer(getPlotOS(plotter))
    else:
      next

logging.info(getTimeStamp() + ' : --------------------------------STOP-------------------------------------')
