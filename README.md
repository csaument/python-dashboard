# python-dashboard
testing area to learn about python and plotly dashboards

## Purpose
The overall purpose of this application is to learn how to code in Python and to learn about using Plotly Dash. Due to personal interest, I've selected the ProPublical Congress API for an external datasource.

## Capabilities
* National dashboard
* State dashboard
* Congressman dashboard
* Votes/abstains
* Party alignment
* Sponsorships/cosponsorships
* Nomination data
* Floor actions
* Committee data
* Current year, current term, lifetime perspectives


## Mechanics
* Front-end application in Python
* Uses public API endpoints for back-end data collection
* Possible future feature to add local storage/copy of data for faster management
* Plotly Dash for data presentation

## Development process
[x] Initial planning/brainstorm
[x] Initial setup
    [x] Add config with private API key
    [x] Setup .gitignore to ignore config
    [x] Build initial Python file
[] Organize initial dashboard
    [] Header
    [] US Map
    * State boundaries
    [] Sliders for data
    * Session/year
    * Democrat/Republican/Independent
    * National/state/district breakdown (stretch)
    [] Drop downs for data
    * Votes
    * Sponsor/cosponsor
    * House/senate
    [] Hover
    * Shows name of relevant members of district/

## Resources
* https://www.propublica.org/datastore/api/propublica-congress-api
* https://www.brookings.edu/multi-chapter-report/vital-statistics-on-congress/

## Dependencies
* Python 
* Dash 
* Pandas
* Requests