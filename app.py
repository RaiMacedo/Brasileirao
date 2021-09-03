from flask import Flask, render_template, request, redirect
import sqlalchemy as sql
import sqlite3

app = Flask("__name__")
app.debug = True


con = sql.create_engine('sqlite:///./brasileirao.db')
db = con.connect()


#SE QUISER REINICIAR TODOS OS JOGOS E TIMES É SÓ EXCLUÍR O BANCO

db.execute("""CREATE TABLE IF NOT EXISTS time(
    id_time INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL, 
    pontuacao INTERGER,
    partidas INTERGER,
    vitorias INTERGER,
    empates INTERGER,
    derrotas INTERGER,
    golspro INTERGER,
    golscontra INTERGER)
    """)


db.execute("""CREATE TABLE IF NOT EXISTS jogo(
    id_jogo INTEGER PRIMARY KEY AUTOINCREMENT,
    time1 INTEGER NOT NULL, 
    time2 INTEGER NOT NULL,
    golstime1 INTEGER NOT NULL,
    golstime2 INTEGER NOT NULL, 
    resultado VARCHAR(50) NOT NULL, 
    FOREIGN KEY(time1) REFERENCES time(id_time), 
    FOREIGN KEY(time2) REFERENCES time(id_time));
    """)


db.execute("""CREATE TABLE IF NOT EXISTS usuario(
    id_time INTEGER PRIMARY KEY AUTOINCREMENT, 
    usuario VARCHAR(50) NOT NULL, 
    pontuacao INTERGER NOT NULL);
    """)


#index--
@app.route("/")
def index():
    return render_template("index.html")




#Times-------------------------------------------------------------------------------
@app.route("/times")
def time():
    some = "some"
    some1 = "some"
    return render_template("times.html", titulo="time", some=some, some1=some1)

@app.route("/cadastrarTime", methods=["POST"])
def cadastrarTime():
    nome = request.form.get("nome")
    if not nome:
        mensagem = "Para realizar o cadastro o time precisa ter nome"
        return render_template("times.html", mensagem=mensagem)
    pontuacao = request.form.get("pontuacao")

    con.execute("INSERT INTO time (nome, pontuacao, partidas, vitorias, \
    empates, derrotas, golspro, golscontra) \
    values(?, 0, 0, 0, 0, 0, 0, 0)", nome)
    mensagem = "Cadastro realizado com sucesso"
    return redirect("/tabela")


@app.route("/alterarTime", methods=["POST"])
def alterarTime():
    if request.form['submitalter'] == 'Buscar':
        codigo = request.form.get("codigo")
        if not codigo:
            mensagem = "Para realizar a busca informe o codigo"
            return render_template("times.html", mensagem=mensagem)

        infoT = "selected"
        some = ""
        infoT1 = ""
        some1 = "some"
        pesquisa = con.execute(f"SELECT id_time, nome, pontuacao, partidas, vitorias, empates, derrotas, golspro, golscontra, golspro - golscontra as saldogols FROM time where id_time = {codigo}")
        return render_template("times.html", codigo=codigo, pesquisa=pesquisa, infoT=infoT, some=some, infoT1=infoT1, some1=some1)
    else:
        codigo = request.form.get("codigo")
        
        nome = request.form.get("nome")
        if not nome:
            mensagem = "Para realizar a alterção informe o nome"
            return render_template("times.html", mensagem=mensagem)
        
        pontuacao = request.form.get("pontuacao")
        if not pontuacao:
            mensagem = "Para realizar a alterção informe a pontuacao"
            return render_template("times.html", mensagem=mensagem)
        
        partidas = request.form.get("partidas")
        if not partidas:
            mensagem = "Para realizar a alterção informe as partidas"
            return render_template("times.html", mensagem=mensagem)
        
        vitorias = request.form.get("vitorias")
        if not vitorias:
            mensagem = "Para realizar a alterção informe as vitorias"
            return render_template("times.html", mensagem=mensagem)
        
        empates = request.form.get("empates")
        if not empates:
            mensagem = "Para realizar a alterção informe os empates"
            return render_template("times.html", mensagem=mensagem)
        
        derrotas = request.form.get("derrotas")
        if not derrotas:
            mensagem = "Para realizar a alterção informe as derrotas"
            return render_template("times.html", mensagem=mensagem)
        
        golspro = request.form.get("golspro")
        if not golspro:
            mensagem = "Para realizar a alterção informe os gols pro"
            return render_template("times.html", mensagem=mensagem)
        
        golscontra = request.form.get("golscontra")
        if not golscontra:
            mensagem = "Para realizar a alterção informe os gols contra"
            return render_template("times.html", mensagem=mensagem)
    
        con.execute(f"UPDATE time set nome = '{nome}', pontuacao = {pontuacao}, partidas = {partidas},\
        vitorias = {vitorias}, empates = {empates}, derrotas = {derrotas}, golspro = {golspro}, golscontra = {golscontra}\
        WHERE id_time = {codigo}")
        mensagem = "Alteração feita com sucesso"
        infoT = "selected"
        some = ""
        infoT1 = ""
        some1 = "some"
        return render_template("times.html", codigo=codigo, mensagem=mensagem, infoT=infoT, some=some, infoT1=infoT1, some1=some1)

@app.route("/excluirTime", methods=["POST"])
def excluirTime():
    if request.form['submitalter1'] == 'Buscar':
        codigo = request.form.get("codigo")
        if not codigo:
            mensagem = "Para realizar a busca informe o codigo"
            return render_template("times.html", mensagem=mensagem)

        infoT = ""
        some = "some"
        infoT1 = "selected"
        some1 = ""
        pesquisa = con.execute(f"SELECT id_time, nome, pontuacao, partidas, vitorias, empates, derrotas, golspro, golscontra, golspro - golscontra as saldogols FROM time where id_time = {codigo}")
        return render_template("times.html", codigo=codigo, pesquisa1=pesquisa, infoT=infoT, some=some, infoT1=infoT1, some1=some1)  
    else:
        codigo = request.form.get("codigo")
        excluir = con.execute(f"DELETE FROM time WHERE id_time = {codigo}")
        mensagem = "Time excluido com sucesso"
        infoT = ""
        some = "some"
        infoT1 = "selected"
        some1 = ""
        return render_template("times.html", codigo=codigo, mensagem=mensagem, infoT=infoT, some=some, infoT1=infoT1, some1=some1)

#---------------------------------------------------------------------------------------------

#Jogos----------------------------------------------------------------------------------------
@app.route("/jogos")
def jogos():
    return render_template("jogos.html", titulo="jogos")

@app.route("/novoJogo", methods=["POST"])
def novojogo():
    codtime1 = request.form.get("codtime1")
    time1 = request.form.get("time1")
    codtime2 = request.form.get("codtime2")
    time2 = request.form.get("time2")
    radioresutado = request.form.get("radioresutado")
    goltime1 = request.form.get("goltime1")
    goltime2 = request.form.get("goltime2")
    #codigo do time 1---------------------------------------
    if request.form['submitJogo'] == 'Buscar times':
        if not codtime1:
            mensagem = "Para realizar a busca do time 1 informe o codigo"
            return render_template("jogos.html", mensagem=mensagem)
          
        if not codtime2:
            mensagem = "Para realizar a busca do time 2 informe o codigo"
            return render_template("jogos.html", mensagem=mensagem)
        
        if codtime1 == codtime2:
            mensagem = "Os times não podem ser iguais"
            return render_template("jogos.html", mensagem=mensagem)
        
        pesquisa = con.execute(f"SELECT nome FROM time where id_time = {codtime1}")
        sometime1 = "some"
        pesquisa1 = con.execute(f"SELECT nome FROM time where id_time = {codtime2}")
        sometime2 = "some"
        return render_template("jogos.html", codtime2=codtime2, pesquisa1=pesquisa1, sometime2=sometime2, codtime1=codtime1, time1=time1, pesquisa=pesquisa, sometime1=sometime1, time2=time2)
    
    else:
        if not radioresutado:
            mensagem = "Para realizar o jogo informe o resultado"
            return render_template("jogos.html", mensagem=mensagem)
        
        if not goltime1:
            mensagem = "Para realizar o jogo infome o numero de gols do time 1"
            return render_template("jogos.html", mensagem=mensagem)
        
        if not goltime2:
            mensagem = "Para realizar o jogo infome o numero de gols do time 2"
            return render_template("jogos.html", mensagem=mensagem)
        
        trazertime1 = con.execute(f"SELECT  nome, pontuacao, partidas, vitorias, empates, derrotas, golspro, golscontra FROM time where id_time = {codtime1}")
        for i in trazertime1:
            nometime1 = i.nome
            pontuacaotime1 = i.pontuacao
            partidastime1 = i.partidas
            vitoriastime1 = i.vitorias
            empatestime1 = i.empates
            derrotastime1 = i.derrotas
            golsprotime1 = i.golspro
            golscontraime1 = i.golscontra
        
        trazertime2 = con.execute(f"SELECT  nome, pontuacao, partidas, vitorias, empates, derrotas, golspro, golscontra FROM time where id_time = {codtime2}")
        for i in trazertime2:
            nometime2 = i.nome
            pontuacaotime2 = i.pontuacao
            partidastime2 = i.partidas
            vitoriastime2 = i.vitorias
            empatestime2 = i.empates
            derrotastime2 = i.derrotas
            golsprotime2 = i.golspro
            golscontraime2 = i.golscontra

        if radioresutado == "Time 1 venceu":
            if goltime1 <= goltime2:
                mensagem = "Os gols não evidenciam que o time 1 ganhou"
                return render_template("jogos.html", mensagem=mensagem)
            con.execute(f"UPDATE time set pontuacao = {int(pontuacaotime1) + 3}, partidas = {int(partidastime1) + 1}, vitorias = {int(vitoriastime1) + 1}, golspro = {int(golsprotime1) + int(goltime1)}, golscontra = {int(golscontraime1) + int(goltime2)} WHERE id_time = {int(codtime1)}")
            con.execute(f"UPDATE time set partidas = {int(partidastime2) + 1}, derrotas = {int(derrotastime2) + 1}, golspro = {int(golsprotime2) + int(goltime2)}, golscontra = {int(golscontraime2) + int(goltime1)} WHERE id_time = {int(codtime2)}")
            con.execute("INSERT INTO jogo (time1, time2, golstime1, golstime2, resultado) values(?, ?, ?, ?, ?)", codtime1, codtime2, goltime1, goltime2, nometime1)
            mensagem = "Cadastro realizado com sucesso"

        elif radioresutado == "Empate":
            if goltime1 != goltime2:
                mensagem = "Os gols não categorizam empate"
                return render_template("jogos.html", mensagem=mensagem)
            con.execute(f"UPDATE time set pontuacao = {int(pontuacaotime1 + 1)}, partidas = {int(partidastime1 + 1)}, empates = {int(empatestime1 + 1)}, golspro = {int(golsprotime1) + int(goltime1)}, golscontra = {int(golscontraime1) + int(goltime2)} WHERE id_time = {codtime1}")
            con.execute(f"UPDATE time set pontuacao = {int(pontuacaotime2) + 1}, partidas = {int(partidastime2) + 1}, empates = {int(empatestime2) + 1}, golspro = {int(golsprotime2) + int(goltime2)}, golscontra = {int(golscontraime2) + int(goltime1)} WHERE id_time = {codtime2}")
            empate = "empate"
            con.execute("INSERT INTO jogo (time1, time2, golstime1, golstime2, resultado) values(?, ?, ?, ?, ?)", codtime1, codtime2, goltime1, goltime2, Empate)
            mensagem = "Cadastro realizado com sucesso"
        else:
            if goltime1 >= goltime2:
                mensagem = "Os gols não evidenciam que o time 2 ganhou"
                return render_template("jogos.html", mensagem=mensagem)
            con.execute(f"UPDATE time set pontuacao = {int(pontuacaotime2) + 3}, partidas = {int(partidastime2) + 1}, vitorias = {int(vitoriastime2) + 1}, golspro = {int(golsprotime2) + int(goltime2)}, golscontra = {int(golscontraime2) + int(goltime1)} WHERE id_time = {codtime2}")
            con.execute(f"UPDATE time set partidas = {int(partidastime1) + 1}, derrotas = {int(derrotastime1) + 1}, golspro = {int(golsprotime1) + int(goltime1)}, golscontra = {int(golscontraime1) + int(goltime2)} WHERE id_time = {codtime1}")
            con.execute("INSERT INTO jogo (time1, time2, golstime1, golstime2, resultado) values(?, ?, ?, ?, ?)", codtime1, codtime2,  goltime1, goltime2, nometime2)
            mensagem = "Jogo realizado com sucesso"

    return render_template("jogos.html", titulo="jogos", mensagem=mensagem)




#Tabela--
@app.route("/tabela")
def tabela():
    times = con.execute("SELECT id_time, nome, pontuacao, partidas, vitorias, empates, derrotas, golspro, golscontra, golspro - golscontra as saldogols FROM time ORDER BY pontuacao DESC, vitorias DESC, partidas ASC, empates ASC, derrotas ASC, golspro DESC, golscontra ASC;")
    jogos1 = con.execute("SELECT id_jogo, nome as time_1, golstime1 as gols_time_1  FROM jogo INNER JOIN time on time.id_time = jogo.time1 ORDER BY id_jogo DESC ")
    jogos2 = con.execute("SELECT golstime2 as gols_time_2, nome as time_2, resultado  FROM jogo INNER JOIN time on time.id_time = jogo.time2 ORDER BY id_jogo DESC")
    return render_template("tabela.html", titulo="Tabela", times=times, jogos1=jogos1, jogos2=jogos2)

@app.route("/telaInicial")
def telaInicial():
    return redirect("/")

@app.route("/telaTabela")
def telaTabela():
    return redirect("/tabela")

@app.route("/telaTimes")
def telaTimes():
    return redirect("/times")

@app.route("/telaJogos")
def telaJogos():
    return redirect("/jogos")

if __name__ == "__main__":
    app.run()