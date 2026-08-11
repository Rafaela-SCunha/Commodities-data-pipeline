import subprocess
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):

    script_path = os.path.join(BASE_DIR, 'src', script_name) 
    print(f"\n{'='*60}\n Executando: {script_path}\n{'='*60}")
    # Chama o script e espera ele terminar
    result = subprocess.run([sys.executable, script_path])
    
    # Se o script der erro (código diferente de 0), interrompe o pipeline
    if result.returncode != 0:
        print(f" Erro crítico ao executar {script_path}. Interrompendo orquestração.")
        sys.exit(1)
    print(f"{script_path} finalizado com sucesso!")

if __name__ == "__main__":
    print("Iniciando o Pipeline Quantitativo de Commodities...")
    
    # Lista com o caminho exato dos seus scripts na ordem cronológica
    scripts_pipeline = [
        "data_collection.py",
        "sliding_window.py",
        "features_extraction.py",
        "crisis_modeling.py",
        "model_validation.py",
        "plot_results.py"
    ]
    
    for script in scripts_pipeline:
        run_script(script)
        
    print("\n Pipeline executado com sucesso de ponta a ponta!")