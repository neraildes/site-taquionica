# -*- coding: utf-8 -*-
"""Confere a pasta `import` antes da importacao no Google Ads Editor.

Tres defeitos custam dinheiro e nao aparecem na tela do Editor:

1. **Palavra-chave anulada pela propria negativa.** Uma negativa em frase mata
   qualquer busca que contenha aquela sequencia, inclusive a palavra-chave que
   voce comprou. O anuncio simplesmente nao aparece, e nada no Editor avisa.
2. **URL final que nao existe.** O anuncio e reprovado ou, pior, o clique cai
   em pagina de erro, e voce paga por ele.
3. **Termo repetido em grupos diferentes da mesma campanha.** Os dois grupos
   disputam o mesmo leilao e o relatorio fica ilegivel.

Rode depois de `gerar_campanha.py`.
"""
import csv, io, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(BASE)
IMPORT = os.path.join(BASE, "import")


def le(nome):
    caminho = os.path.join(IMPORT, nome)
    with io.open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    kws = le("3-keywords.csv")
    negs_grupo = le("4-negativas-por-grupo.csv")
    negs_globais = le("negativas-lista-global.csv")
    anuncios = le("5-anuncios.csv")
    sitelinks = le("6-extensoes-sitelinks.csv")

    problemas = []

    # ---------------------------------------------- 1. negativa contra a propria kw
    por_grupo = {}
    for r in negs_grupo:
        chave = (r["Campaign"], r["Ad Group"])
        por_grupo.setdefault(chave, []).append((r["Keyword"], r["Criterion Type"]))

    globais = [r["Keyword"] for r in negs_globais]
    globais_por_campanha = {}
    for r in negs_globais:
        globais_por_campanha.setdefault(r["Campaign"], set()).add(r["Keyword"])

    for r in kws:
        termo = r["Keyword"]
        chave = (r["Campaign"], r["Ad Group"])
        for neg, tipo in por_grupo.get(chave, []):
            if tipo == "Negative Phrase" and neg in termo:
                problemas.append("negativa de grupo mata a palavra-chave: "
                                 "[%s] %s <- \"%s\"" % (r["Ad Group"], termo, neg))
            elif tipo == "Negative Exact" and neg == termo:
                problemas.append("negativa exata mata a palavra-chave: "
                                 "[%s] %s" % (r["Ad Group"], termo))
        for neg in globais_por_campanha.get(r["Campaign"], ()):
            if neg in termo:
                problemas.append("negativa global mata a palavra-chave: "
                                 "[%s] %s <- \"%s\"" % (r["Ad Group"], termo, neg))

    # ------------------------------------------------------- 2. URLs que existem
    def existe(url):
        if not url.startswith("https://taquionica.com.br"):
            return False
        caminho = url.replace("https://taquionica.com.br", "").split("#")[0].strip("/")
        if caminho == "":
            return os.path.isfile(os.path.join(SITE_DIR, "index.html"))
        return os.path.isfile(os.path.join(SITE_DIR, caminho, "index.html"))

    for r in anuncios:
        if not existe(r["Final URL"]):
            problemas.append("anúncio aponta para página inexistente: [%s] %s"
                             % (r["Ad Group"], r["Final URL"]))
    for r in sitelinks:
        if not existe(r["Final URL"]):
            problemas.append("sitelink aponta para página inexistente: %s"
                             % r["Final URL"])

    # -------------------------------------------- 3. termo repetido entre grupos
    visto = {}
    for r in kws:
        chave = (r["Campaign"], r["Keyword"], r["Criterion Type"])
        if chave in visto and visto[chave] != r["Ad Group"]:
            problemas.append("termo em dois grupos da mesma campanha: %s (%s e %s)"
                             % (r["Keyword"], visto[chave], r["Ad Group"]))
        visto[chave] = r["Ad Group"]

    # ------------------------------------------------------------------ resumo
    campanhas = {}
    for r in kws:
        campanhas.setdefault(r["Campaign"], set()).add(r["Ad Group"])
    print("%d critérios, %d grupos, %d campanhas"
          % (len(kws), sum(len(v) for v in campanhas.values()), len(campanhas)))
    print("%d negativas de grupo, %d termos na lista global"
          % (len(negs_grupo), len(set(globais))))

    if problemas:
        print("\n*** %d PROBLEMAS ***" % len(problemas))
        for p in sorted(set(problemas)):
            print("  " + p)
        sys.exit(1)
    print("\nOK: nenhuma palavra-chave anulada, todas as páginas existem.")


if __name__ == "__main__":
    main()
