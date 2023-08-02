from flask import Flask, redirect, url_for, render_template, request
import sqlite3

# conn = sqlite3.connect("polling.db")

# cur = conn.cursor()

##############################################################
# We have already created the table by using the below command
##############################################################
# cur.execute('''

#             CREATE TABLE footballer(
#                 code TEXT, count INT
#             )

#             ''')
# conn.commit()
##############################################################

# We have already added the data(Code and votes) in footballer

# player_data = [

#     ("CR", 0),
#     ("LM", 0),
#     ("KM", 0),
#     ("EH", 0)
# ]

# cur.executemany(" INSERT INTO footballer VALUES (?,?) ", player_data)
# conn.commit()
##############################################################


################ SOME ERROR HANDLING ##############
#cur.execute("DELETE FROM footballer WHERE ROWID>4")


##############################################################
# NOW WE WILL CREATE WISKEY TABLE
##############################################################
# cur.execute('''

#             CREATE TABLE wiskey(
#                 code TEXT, count INT
#             )

#             ''')
##############################################################
# NOW WE WILL ADD DATA

# wiskey_data = [

#     ("JD", 0),
#     ("JS", 0),
#     ("JW", 0),
#     ("TS", 0)
# ]

# cur.executemany(" INSERT INTO wiskey VALUES (?,?) ", wiskey_data)


# cur.execute("DELETE FROM wiskey WHERE ROWID>4")
# conn.commit()

# cur.execute("SELECT * FROM wiskey")
# print(cur.fetchall())

# NOW OUR TABLES WITH DATA ARE READY.....

# conn.commit()

# cur.close()
# conn.close()

def update_db(table,cd):
    if table=="F":
        conn = sqlite3.connect("polling.db")
        cur = conn.cursor()
        cur.execute("UPDATE footballer SET count=count+1 WHERE code=?",(cd,))
        conn.commit()
        cur.close()
        conn.close()

    else:
        conn = sqlite3.connect("polling.db")
        cur = conn.cursor()
        cur.execute("UPDATE wiskey SET count=count+1 WHERE code=?",(cd,))
        conn.commit()
        cur.close()
        conn.close()


app = Flask(__name__)
 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/footballer', methods = ['POST','GET'])
def footballer():
    if request.method=='POST':
        # Here we need to make the backend of the application
        option = request.form['option']
        #print(option)
        update_db("F",option)
        return redirect('/thankyou')
    else:
        return render_template('footballer.html')


@app.route('/wiskey', methods = ['POST','GET'])
def wiskey():
    if request.method=='POST':
        # Here we need to make the backend of the application
        option = request.form['option']
        update_db("W",option)
        return redirect('/thankyou')
    else:
        return render_template('wiskey.html')
    
@app.route('/results')
def results():
    conn = sqlite3.connect("polling.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM footballer")
    f_data = cur.fetchall()
    cur.execute("SELECT * FROM wiskey")
    w_data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    #print(f_data)
    #print(w_data)
    # now we need to make the results html page ans send data to it...
    f_data = {"Cristiano Ronaldo": f_data[0][1], "Leonel Messi": f_data[1][1], "Kylian Mbappe": f_data[2][1], "Erling Haaland": f_data[3][1]}
    w_data = {"Jack Daniel's": w_data[0][1], "Jameson": w_data[1][1], "Johnnie Walker": w_data[2][1], "Teacher's": w_data[3][1]}
    return render_template('results.html',f_data=f_data,w_data=w_data)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)


