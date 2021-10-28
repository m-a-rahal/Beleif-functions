from my_pyds import Sources

def main():
    global sources
    # exercice 1
    # on écrit Ω comme étant des mots séparés par des virgules
    omega = 'p, c, s'

    # on stockes nos sources d'information dans une classe appelée 'Sources'
    sources = Sources(omega)
    sources.add({'p,c' : 0.65, 's' : 0.24})
    sources.add({'s' : 0.48})
    sources.add({'p' : 1.0/3, 'c' : 1.0/3, 's' : 1.0/3})
    sources.add({'p,c,s' : 1})

    # afficher les masses des sources
    print(sources)

    # affaiblir la source 1 (indice 0) avec un taux α = 0.12
    source_infiable = 0
    alpha = 0.12
    sources.affaiblir(source_infiable, alpha)
    print(f'--- après affaiblissement ------ α = {alpha} ---------------------\n')
    sources.show_source(source_infiable)

    # combiner les sources (en ignorant celles avec m(Ω) = 1)
    print(f'--- combinaison des sources ---------------------------\n')
    m = sources.combine(show_steps = True)
    print(f'--- après combinaison ---------------------------\n')
    print(m)

if __name__ == '__main__':
    main()