import os
import shutil
import datetime
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# --- CONFIGURAÇÕES DO USUÁRIO ---

# 1. Configure o caminho para a pasta que você quer fazer backup
#    Path.home() pega o diretório principal do seu usuário (ex: /home/usuario ou C:/Users/Usuario)
#    Altere "Documents" e "TCC" conforme necessário.
SOURCE_PATH = Path.home() / "Documents" / "TCC"

# 2. Prefixo do nome do arquivo de backup
BACKUP_PREFIX = "Backup_TCC"

# 3. (MUITO IMPORTANTE) ID da pasta no Google Drive para onde o backup será enviado.
#    Veja as instruções abaixo do script para saber como obter este ID.
#    Se for None, o backup será salvo na raiz do "Meu Drive".
GDRIVE_FOLDER_ID = "SEU_ID_DA_PASTA_DO_GOOGLE_DRIVE_VAI_AQUI" 

# ---------------------------------

def authenticate_gdrive():
    """
    Autentica com o Google Drive.
    Na primeira execução, abrirá um navegador para autorização.
    Ele salvará as credenciais em 'mycreds.txt' para usos futuros.
    """
    gauth = GoogleAuth()
    try:
        # Tenta carregar credenciais salvas
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Autentica se não houver credenciais
            print("Autenticação necessária. Abrindo navegador...")
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Atualiza se as credenciais expiraram
            print("Atualizando token de acesso...")
            gauth.Refresh()
        else:
            # Inicializa se as credenciais são válidas
            gauth.Authorize()
        
        # Salva as credenciais (ou o token atualizado) para a próxima vez
        gauth.SaveCredentialsFile("mycreds.txt")
        
        print("Autenticação com Google Drive bem-sucedida.")
        return GoogleDrive(gauth)
        
    except Exception as e:
        print(f"Erro durante a autenticação: {e}")
        print("Verifique se o arquivo 'client_secrets.json' está no mesmo diretório.")
        return None

def compress_folder(source_dir_path, zip_name_base):
    """
    Compacta a pasta de origem (source_dir_path) em um arquivo zip.
    Retorna o caminho (Path) para o arquivo zip criado.
    """
    print(f"Iniciando compactação de: {source_dir_path}")
    try:
        # base_name: Onde salvar o zip (sem a extensão .zip)
        # root_dir: O diretório "pai" da pasta que queremos zipar (ex: Documents)
        # base_dir: O nome da pasta que queremos zipar (ex: TCC)
        zip_file_path_str = shutil.make_archive(
            base_name=str(zip_name_base),
            format='zip',
            root_dir=source_dir_path.parent,
            base_dir=source_dir_path.name
        )
        
        final_zip_path = Path(zip_file_path_str)
        print(f"Pasta compactada com sucesso: {final_zip_path.name}")
        return final_zip_path
        
    except FileNotFoundError:
        print(f"Erro: A pasta de origem não foi encontrada em: {source_dir_path}")
        return None
    except Exception as e:
        print(f"Erro ao compactar pasta: {e}")
        return None

def upload_to_gdrive(drive, file_path, folder_id=None):
    """
    Faz o upload do arquivo (file_path) para o Google Drive.
    Se folder_id for fornecido, faz o upload para dentro dessa pasta.
    """
    file_name = file_path.name
    print(f"Iniciando upload de: {file_name}")
    
    metadata = {'title': file_name}
    if folder_id:
        metadata['parents'] = [{'id': folder_id, 'kind': 'drive#parentReference'}]
        
    try:
        file_drive = drive.CreateFile(metadata)
        file_drive.SetContentFile(str(file_path)) # Define o conteúdo do arquivo
        file_drive.Upload() # Faz o upload
        
        print(f"Upload concluído com sucesso!")
        print(f"Nome do arquivo: {file_drive['title']}")
        print(f"Link: {file_drive['alternateLink']}")
        return True
        
    except Exception as e:
        print(f"Erro durante o upload para o Google Drive: {e}")
        return False

def main():
    # 1. Validar pasta de origem
    if not SOURCE_PATH.exists() or not SOURCE_PATH.is_dir():
        print(f"Erro: A pasta de origem não existe ou não é um diretório.")
        print(f"Caminho verificado: {SOURCE_PATH}")
        return

    # 2. Preparar nomes e caminhos
    today_str = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    zip_name = f"{BACKUP_PREFIX}_{today_str}"
    
    # O zip será salvo temporariamente no mesmo diretório do script
    zip_path_base = Path.cwd() / zip_name 

    # 3. Compactar a pasta
    final_zip_path = compress_folder(SOURCE_PATH, zip_path_base)
    
    if final_zip_path is None:
        print("Falha na compactação. Abortando.")
        return

    # 4. Autenticar e Fazer Upload
    drive = authenticate_gdrive()
    
    if drive is None:
        print("Falha na autenticação. Abortando.")
        # Limpa o zip local se a autenticação falhar
        final_zip_path.unlink()
        print(f"Arquivo zip local removido: {final_zip_path.name}")
        return

    success = upload_to_gdrive(drive, final_zip_path, GDRIVE_FOLDER_ID)
    
    # 5. Limpeza
    if success:
        print("Limpando arquivo zip local após upload...")
        final_zip_path.unlink() # Remove o arquivo zip local
        print("Limpeza concluída.")
    else:
        print("O upload falhou. O arquivo zip local foi mantido para verificação.")
        print(f"Arquivo local: {final_zip_path}")

if __name__ == "__main__":
    main()