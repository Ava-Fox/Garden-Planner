# insert data into plots
# NW L : 1
# NE L : 2
# CENTER: 3
# SW L : 4
# SE L : 5
# SHADE : 6
from cs50 import SQL

db = SQL("sqlite:///garden.db")

# Start w/ the 4X4
for y in range(1,5):
    for x in range(1, 5):
        # add plot w/ local_x as x and local_y as y and bed = 3
        db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, 3)

# Now the 4x10
for y in range(1, 5):
    for x in range(1, 11):
       db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, 6)

# Now the L's
for b in range(1, 5):
    # Create NW L
    if b == 1:
        for y in range(1, 9):
            if y > 4:
                 # create 4X4
                for x in range(1, 5):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, b)
            else:
                 # create 4X8
                for x in range(1, 9):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, b)
              
    elif b == 2:
        for y in range(1, 9):
            if y > 4:
                # Create 4x4 on right side
                for x in range(5, 9):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, b)
            else:
                for x in range(1, 9):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, b)

    elif b == 3:
        for y in range(1, 9):
            if y <= 4:
                for x in range(1, 5):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, 4)
            else:
                for x in range(1, 9):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, 4)

    elif b == 4:
        for y in range(1, 9):
            if y <= 4:
                for x in range(5, 9):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, 5)
            else:
                for x in range(1, 9):
                    db.execute("INSERT INTO plot (local_x, local_y, bed) VALUES (?, ?, ?);", x, y, 5)