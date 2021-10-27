from my_pyds import Masse, str_to_set

def main():
    omega = str_to_set('p c o s')
    sources = []
    sources.append( Masse({'pc' : 0.65, 'o' : 0.24, 'ps' : 0}, omega) )
    sources.append( Masse({'s' : 0.48}, omega) )
    sources.append( Masse({'p' : 1.0/3, 'c' : 1.0/3, 's' : 1.0/3}, omega) )
    sources.append( Masse({'pcos' : 1}, omega) )

    for i, s in enumerate(sources):
        print('resource', i+1,':')
        print(s)

if __name__ == '__main__':
    main()