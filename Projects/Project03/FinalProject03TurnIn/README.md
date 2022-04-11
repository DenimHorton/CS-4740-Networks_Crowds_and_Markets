# Introduction
Below is a quick overview of the project python file written to demonstrate the spreading process in the network/graph that was provided to us. 

<p align="center">
<img src="./images/Figure1.1.PNG" width="250" height="250">
<br>
Project Provided Graph
</p>

# File structure and outputs 
Below is the provided file structure for this project where XX at the end of each file, before the "." file extension, represents the node that is pointing at the bad connection
```
FinalProject03TurnIn
├─ Deliverable01
│  └─ project03_code.pdf
│ 
├─ Deliverable02
│  ├─ Graphs
│  │  ├─ shrtAllOverallPValsBadEdgeXX.png
│  │  ├─ shrtNodeOpnionsBadEdgeXX.png
│  │  └─ longOverallPValsBadEdgeXX.png
│  │ 
│  └─ Tables
│     └─ ShortTermTableBadConnectionXX.txt
│ 
├─ Deliverable03
│  ├─ Graphs
│  │  ├─ longAllOverallPValsBadEdgeXX.png
│  │  ├─ longNodeOpnionsBadEdgeXX.png
│  │  └─ longOverallPValsBadEdgeXX.png
│  │ 
│  └─ Tables  
│     └─ LongTermTableBadConnection09.txt
│   
├─ Outputs
│  ├─ Graphs
│  │  ├─ mediumAllOverallPValsBadEdgeXX.png
│  │  ├─ mediumNodeOpnionsBadEdgeXX.png
│  │  ├─ mediumOverallPValsBadEdgeXX.png
│  │  └─ mediumOverallPValsBadEdgeXX.png
│  │
│  └─ Tables
│     └─ tableOutput.txt
│
├─ project03.py
├─ Project03Paper.pdf
└─ requirments.txt

```

# Install of dependencies
To take care of dependencies run the following command to pip install all the required libraries to run this program which you can also look under the requirements.txt file in the parent directory, FinalProjectTurnIn.
<p align="center">
```py -m pip install -r requirements.txt```
</p>

# Program execution
When running the program make sure to execute the project03.py file from within the working directory ./FinalProject03TurnIn.  
The zip if already filled with .txt and .png files inside the Deliverable01 and Deliverable02 folders that are output tables and graphs generated from earlier executions.  The program when ran will output the tables to the different DeliverableXX folders to the console.  Graphs will be saved to the Outputs/Graphs folder.  The Outputs folder also contains a Tables folder which contains table printout from all three types of runs,
* Short (2 time steps)
* Medium (10 time steps)
* Long (100 time steps)


