from my_pyds import Masse, str_to_set, Sources

def main():
    omega = str_to_set('p c s')
    sources = Sources(omega)
    sources.add({'pc' : 0.65, 's' : 0.24})
    sources.add({'s' : 0.48})
    sources.add({'p' : 1.0/3, 'c' : 1.0/3, 's' : 1.0/3})
    sources.add({'pcs' : 1})

    print(sources)

    alpha = 0.12
    source_infiable = 0
    print(f'--- après affaiblissement ------ α = {alpha} ---------------------\n')
    sources.affaiblir(source_infiable, alpha)
    sources.show_source(source_infiable)

    print(f'--- combinaison des sources ---------------------------\n')
    m = sources.combine(show_steps = True)
    print(f'--- après combinaison ---------------------------\n')
    print(m)

if __name__ == '__main__':
    main()