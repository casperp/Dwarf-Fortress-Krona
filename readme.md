#Dwarf fortress krona plots

This script makes two krona plots from dwarf fortress world sites and pops file.
Plot 1 is an overview of civilisations (dwarf,goblins,elf's, ect.) than populations groups (goverments) and than there sites and the amount of units in the cites

Plot 2 is an overview of inhabits per site per population(government).


## requirements 
1. krona needs to be installed [] This wil only work on mac os x and linux
2. python3.X 

## usages 
Run plot_world_info.py in the terminal with the the following paramters : 
```
  python3 plot_world_info.py  F   F_O   F_OO
  F              df world sites_and_pop file
  F_O            Name for civ plot html
  F_OO           Name for civ and pop plot html
  ```
 Example:
 ```bash
python3 plot_world_info.py examples/region13-00350-01-01-world_sites_and_pops.txt examples/plot1.html examples/plot2.html
```

#Issues
Because dwarf fortress is Procedural generated not al tags are know for sites.
Currently the tags administrator,law_giver,Owner,Parent,lord and lady are now in this program and are ignored when counting 
populations. If there are any wierd names in the plot like "lord:Parent Civ, something something" please open an issue with the tag name and the 
df file so I can add the tag to the know tags. 