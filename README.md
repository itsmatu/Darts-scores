# Darts scores

This app provides a user-friendly way to keep track of users' darts match stats and averages.

Users are able to register, log in and add scores from individual matches.

## Current state

The app can be used [here](https://dartsscores.herokuapp.com/)

### Account management

Users are able to register a new account or log in to an existing account. A user account is required to save match averages to the site.

### Main functionality

Users are currently able to add averages from their matches. If the user is logged in to the site, `/mainpage` will show all personal averages and the average of the last 30 days stats, as well as the top 5 personal averages.

Users are able to view all saved averages and all time top 5 averages by accessing `/mainpage/allstats`. This site will be shown on default if the user is not logged in to the site.

Averages can be viewed individually by clicking them. Currently the page only shows the name of the user and the average but more features are going to be added soon.
 
### Work in progress

- `/newgame` will provide the user a score keeping tool while playing a match. Stats from a played game will be saved automatically to the database.
- Users will be able to manage their personal settings. For example to change the look of the UI (Dark mode etc) or change the language.
- A more visually pleasant look to the UI
- Ability to remove saved averages or modify them.
