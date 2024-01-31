# Ava's Garden
#### Video Demo:  <URL HERE>
#### Description:
 explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them. Ensure you allocate sufficient time and energy to writing a README.md that documents your project thoroughly. Be proud of it! A README.md in the neighborhood of 750 words is likely to be sufficient for describing your project and all aspects of its functionality. If unable to reach that threshold, that probably means your project is insufficiently complex.

- What is:
  - Garden log

My project is a straightforward garden log that keeps track of which plant grew in which plot in my garden. On the index page, you can click on a button that represents exactly which 12x12 inch plot you're interested in knowing the history of, as well as add plants and notes to the history data yourself. Since the shape of my boxes weren't particularly ordinary, I chose to demonstrate the overall garden as a drawn picture, and then organize the buttons underneath. 

While the log in and register pages are strictly speaking unnecessary, I still included them so I could take from previous homework and enjoy the feeling of logging in to my own webpage. 

The main workhorses of this program are the SQL database, plothistory, and the add pages. 

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

