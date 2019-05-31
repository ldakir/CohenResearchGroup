# CohenResearchGroup

## The following repository contains:

  - Scripts to analyze and visualize Chandra observations of zeta Pup for single spectral lines
  - Data of the Chandra observations of zeta Pup
  - Plots of single spectral lines

## How to navigate this repository:

For now, I have only included zeta Pup observations. If you open the ZPUP folder you would find folders saved as "ObsID". Each ObsID represents a different cycle of observations. <br/>
Within the "ObsID", there are two folders:  
  - DATA: contains data from xspec. 
  - PLOTS: contains results. <br/>
#### Note: In the ZPUP folder there is also an excel sheet containing all necessary information about each spectral line

## How to get repository on your computer:
	git clone https://github.com/ldakir/CohenResearchGroup.git

## How to get add contents:

##### Before adding anything, make sure to git pull. This is necessary to avoid merge problems. <br/>

Let's say you want to add plots from the 21659 data set of zeta pup:

	> cd CohenResearchGroup
	> cd ZPUP  
	> mkdir 21659  
	> cd 21659
	> mkdir PLOTS  
	--> Add your plots to the PLOTS folder
	--> Go back to zpup folder
	> git add 21659
	> git commit -m "21659 plots"
	> git push
	
If you open the repository, your plots should be there! 


	






  
