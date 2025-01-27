# run_seeds.py

from scripts.seed import run as run_seed
from scripts.seedParcela import run as run_seedParcela
from scripts.seed_comunidades import run as run_seed_comunidades

def main():

    print("Running seed_comunidades.py")
    run_seed_comunidades()
    
    print("Running seed.py")
    run_seed()

    print("Running seedParcela.py")
    run_seedParcela()

if __name__ == "__main__":
    main()
