# Ava's Garden
#### Video Demo:  <URL HERE>
#### Description:
 explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them. Ensure you allocate sufficient time and energy to writing a README.md that documents your project thoroughly. Be proud of it! A README.md in the neighborhood of 750 words is likely to be sufficient for describing your project and all aspects of its functionality. If unable to reach that threshold, that probably means your project is insufficiently complex.

- What is:
  - Garden log

My project is a straightforward garden log that keeps track of which plant grew in which plot in my garden. On the index page, you can click on a button that represents exactly which 12x12 inch plot you're interested in knowing the history of, as well as add plants and notes to the history data yourself. Since the shape of my boxes weren't particularly ordinary, I chose to demonstrate the overall garden as a drawn picture, and then organize the buttons underneath. This was a much better solution than my previous attempt, which was to try (and fail) to create an L - shaped table with buttons that would lead to each seperate plothistory page. 

While the log in and register pages are strictly speaking unnecessary, I still included them so I could take from previous homework and enjoy the feeling of logging in to my own webpage. 

The main workhorses of this program are the SQL database, plothistory, and the add pages. I was able to create a separate program called sql.py that created and logged each plot of my garden into a SQL database. The main tables are the plants, history, and plot tables. Each logged plant may have a url associated with it that will be later accessed if the user wishes to read up more on it. The plot table logs every plot in my garden and assigns them an id. The history table is set up to coincide with both the plant and plot tables, and includes more information about each history instance such as date, seed source, and notes. 

The index gives the user a list of options to click through, and saves which button value was clicked to the session - which is correlated to the plot data -  so that it can redirect them to a plothistory page. This is how the plot data is saved from one route to another. This can then give the illusion of a separate plot history page for each plot. I modified sql.py into a jinja format in index.html in order to create each plot button. 

Every time a user is directed to the plothistory page, the history of the button clicked is looked up in the database given the button and plot's value. In this page, the user has the option to add notes about a specific plant, or learn more about a logged plant depending on whether a link is provided in the database or not. If so, the plant name is linked to an outside resource (most likely to growinginthegarden.com). 

If a user wishes to add notes to a particular plant, they may do so by entering data into a textbox in the notes section. The html page has two inputs for each note, one being hidden whos value is the history id. This is so that data entered into one section won't get put into an unrelated one. The page is then redirected back to itself so the user does not need to manually refresh the page.

In order to add a plant to a plot, a user must navigate to the dedicated page. Here they have the option to log in more information about the plant being entered. The plot coordinates are related to the bed number and its x and y values. The beds are numbered from top-down left to right, for example: the North West L - shaped bed is also known as bed number 1. It is then checked to see if the user enered in a valid plot number by checking to see if there is an id associated with a plot with the given values. 

I was also able to look in flask's docs in order to create a personalized 404 error page.

A main focus I had during the development of this website was to solidify my git and github skills. As such, I was able to get comfortable creating and merging branches when working on different aspects of the code, as well as pushing and pulling to and from github.

- Files:
  - Templates:
    - add, index, layout, plothistory, login, notfound, register
  - Static:
    - CSS
  - code:
    - app.py
    - sql.py
    - helpers.py

  - Some taking from past homework projects, like the login and register pages (because originally wanted to have it an open-ended garden planner where people could design their own space, but later focused on just my own garden). I kept them because it's fun to log in and out, and it's kind of amusing that it's the same website regardless.


- learning git, github, playing with branches
- Linking to other websites, depending on if have url in 
  database or not
- Designing database (could have picture of layout)
- look up flask documentation to figure out how to get info
  from one function to another, and to make a customized
  404 error page
- User table because wanted to originally make it a    
  generalized thing and might still figure that out
- Wrote python file that logged every plot in my garden
- Modified that file to create button on screen for each   
  plot
- Originally tried to do most of the logic on html jinja to
  create these wonky shapes but was advised otherwise.
- CSS to get the plot buttons to align better on page
  instead of just one long line down the left side of 
  screen (adding two classes, one for the overal beds and another for each bed... so each in one big div but have its own seperate one as well)
- Index lists out all the buttons, and when click on one
  it redirects to the "plothistory page" which looks up the
  data of the plot and lists out every plant you've logged
  there
- Add page is where you can add plants to plots 
- Plothistory you can add notes to and I chose to    
  'redirect' to the same page so that you don't have to
  manually refresh the page each time. 