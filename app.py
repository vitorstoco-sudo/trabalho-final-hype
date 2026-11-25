from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-jogo-da-forca"

from random import choice


PALAVRAS = [
    "python",
    "flask",
    "programacao",
    "desenvolvimento",
    "web",
    "jogo",
    "velha",
    "codigo",
    "aplicacao",
    "funcao",
]

def criar_jogo():
    session["palavra_secreta"] = choice(PALAVRAS)
    session["letras_acertadas"] = []
    session["letras_erradas"] = []

    for a, b, c in combinacoes:
        if tabuleiro[a] and tabuleiro[a] == tabuleiro[b] == tabuleiro[c]:
            return tabuleiro[a]
    return None


@app.route("/")
def index():
    if "tabuleiro" not in session:
        criar_jogo()

    tabuleiro = session["tabuleiro"]
    vencedor = obter_vencedor(tabuleiro)
    empate = vencedor is None and "" not in tabuleiro

    return render_template(
        "index.html",
        tabuleiro=tabuleiro,
        jogador=session["jogador"],
        vencedor=vencedor,
        empate=empate,
    )


@app.route("/jogar/<int:posicao>")
def jogar(posicao):
    if "tabuleiro" not in session:
        criar_jogo()

    tabuleiro = session["tabuleiro"]

    if 0 <= posicao < 9 and tabuleiro[posicao] == "":
        if obter_vencedor(tabuleiro) is None:
            tabuleiro[posicao] = session["jogador"]
            session["tabuleiro"] = tabuleiro

            if obter_vencedor(tabuleiro) is None:
                session["jogador"] = "O" if session["jogador"] == "X" else "X"

    return redirect(url_for("index"))


@app.route("/reiniciar")
def reiniciar():
    criar_jogo()
    return redirect(url_for("index"))


@app.route("/regras")
def regras():
    return render_template("regras.html")


if __name__ == "__main__":
    app.run(debug=True)
