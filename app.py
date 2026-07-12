from flask import Flask , render_template , request , url_for , redirect
import mysql.connector
app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = '',
    database = 'ligue_foot'
)






@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/equipes' , methods = ['GET' ,'POST'])
def equipes():
    if request.method == 'POST':
        nom = request.form['nom']
        ville = request.form['ville']
        mycursor = mydb.cursor()
        if ville and nom:
            mycursor.execute("INSERT INTO EQUIPES (nom,ville) VALUES (%s,%s)",(nom,ville))
        else:
            return "les champs doit etre remplis"
        mydb.commit()
        mycursor.close()
        return redirect(url_for('equipes'))
    mycursor = mydb.cursor()
    mycursor.execute("select * from EQUIPES")
    resultat = mycursor.fetchall()   
    mycursor.close()   
    return render_template('equipes.html' , equipes = resultat)


@app.route('/classement')
def classement():
    mycursor = mydb.cursor()
    query ="""SELECT 
    E.nom,
    COUNT(*) AS matchs_joues,
    SUM(CASE 
        WHEN (E.equipe_id = M.equipe_domicile AND M.score_domicile > M.score_exterieur)
          OR (E.equipe_id = M.equipe_exterieur AND M.score_exterieur > M.score_domicile)
        THEN 1 ELSE 0 
    END) AS victoires,
    SUM(CASE 
        WHEN M.score_domicile = M.score_exterieur 
        THEN 1 ELSE 0 
    END) AS nuls,  
    SUM(CASE 
        WHEN (E.equipe_id = M.equipe_domicile AND M.score_domicile < M.score_exterieur)
          OR (E.equipe_id = M.equipe_exterieur AND M.score_exterieur < M.score_domicile)
        THEN 1 ELSE 0 
    END) AS defaites,
    SUM(CASE 
        WHEN (E.equipe_id = M.equipe_domicile AND M.score_domicile > M.score_exterieur)
          OR (E.equipe_id = M.equipe_exterieur AND M.score_exterieur > M.score_domicile)
        THEN 3 
        WHEN M.score_domicile = M.score_exterieur THEN 1 
        ELSE 0 
    END) AS points
    FROM MATCHS M
    JOIN EQUIPES E ON (E.equipe_id = M.equipe_domicile OR E.equipe_id = M.equipe_exterieur)
    GROUP BY E.equipe_id
    ORDER BY points DESC, victoires DESC;"""
    mycursor.execute(query)
    resultat = mycursor.fetchall()
    return render_template('classement.html', classement= resultat)


@app.route('/matchs',methods = ["GET","POST"])
def matchs():
    if request.method == 'POST':
        print(request.form)
        equipe_domicile = request.form['equipe_domicile']
        equipe_exterieur = request.form['equipe_exterieur']
        score_domicile = request.form['score_domicile']
        score_exterieur = request.form['score_exterieur']
        if equipe_domicile == equipe_exterieur:
            return "Une équipe ne peut pas jouer contre elle-même"
        mycursor = mydb.cursor()
        if score_domicile and score_exterieur :
            mycursor.execute("INSERT INTO MATCHS (equipe_domicile,equipe_exterieur,score_domicile , score_exterieur) VALUES(%s,%s,%s,%s)",(equipe_domicile,equipe_exterieur,score_domicile,score_exterieur))
        else:    
            return "les champs doivent etre remplis"
        mydb.commit()
        mycursor.close()
        return redirect(url_for('matchs'))
    mycursor = mydb.cursor()
    mycursor.execute("SELECT MATCHS.match_id, E1.nom, MATCHS.score_domicile, E2.nom, MATCHS.score_exterieur FROM MATCHS, EQUIPES E1, EQUIPES E2 WHERE MATCHS.equipe_domicile = E1.equipe_id AND MATCHS.equipe_exterieur = E2.equipe_id")
    resultat = mycursor.fetchall()
    mycursor.execute("SELECT * FROM EQUIPES")
    res2 = mycursor.fetchall()    
    mycursor.close()
    return render_template('matchs.html',matchs = resultat , equipes = res2 )

@app.route('/supprimer_match/<int:match_id>', methods=['POST'])
def supprimer_match(match_id):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM MATCHS WHERE match_id = %s", (match_id,))
    mydb.commit()
    mycursor.close()
    return redirect(url_for('matchs'))

if  __name__== "__main__":
    app.run(debug = True)
    

