# Manage_Intervals_Challenge

Author:         Kevin Dious (kdious@gmail.com)

This program is designed to manage a list of intervals.

[[1, 3], [4, 6]] is a valid object gives two intervals.  
[[1, 3], [3, 6]] is not a valid object because it is not disjoint. [[1, 6]] is the intended result.

Empty array [] means no interval, it is the default/start state.

The program supports the following functions/routines:

add \<from> \<to>:&nbsp;&nbsp;&nbsp;&nbsp;Adds a new interval to the list  
remove \<from> \<to>:&nbsp;Removes an interval from the list  
clear:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Clears the interval list  
enableDebugging:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Enables extra debugging logs  
disableDebugging:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Disables debugging logs  
displayList:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Display the current interval list  
exit:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Exits the program  
help:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Displays a list of commands

Here is an example sequence:  
Start: []  
Call: add 1 5&nbsp;&nbsp;&nbsp;&nbsp;=> [[1, 5]]  
Call: remove 2 3&nbsp;=> [[1, 2], [3, 5]]  
Call: add 6 8&nbsp;&nbsp;&nbsp;&nbsp;=> [[1, 2], [3, 5], [6, 8]]   
Call: remove 4 7&nbsp;=> [[1, 2], [3, 4], [7, 8]]  
Call: add 2 7&nbsp;&nbsp;&nbsp;&nbsp;=> [[1, 8]]    
