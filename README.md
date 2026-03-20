# Backup Automatizado para Nuvem
*Proteja seus arquivos importantes de forma simples e eficiente automatizando o envio de dados para o Google Drive com Python.*
## Sobre o Projeto
Este repositório apresenta uma solução prática para quem busca segurança e praticidade.[1] O script central **backup_para_drive.py** gerencia a autenticação e o fluxo de upload, permitindo que você mantenha uma rotina de backup robusta sem esforço manual.[1]
## Funcionalidades

- Integração direta com a API do Google Cloud.
- Upload automatizado de arquivos individuais ou pastas inteiras.
- Sistema de autenticação seguro via OAuth2.
- Facilidade para agendamento de tarefas automáticas (Cron/Task Scheduler).
[1]
## Requisitos
É necessário instalar as bibliotecas de cliente do Google para Python:
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`[1]
## Como Utilizar
```python

Após configurar suas credenciais.json, basta rodar:
python backup_para_drive.py

```[1]
## Estrutura do Repositório
| Arquivo | Descrição |
| --- | --- |
| backup_para_drive.py | Script principal de automação |
| credentials.json | Arquivo de autenticação (não incluso/necessário configurar) |
> [!TIP]
> Lembre-se de nunca subir seu arquivo 'credentials.json' ou 'token.json' para repositórios públicos para manter a segurança da sua conta.[1]
## Status de Desenvolvimento
- [x] Conexão com Google Drive API
- [x] Lógica de upload de arquivos
- [ ] Implementação de compactação .zip antes do envio
- [ ] Suporte para múltiplos provedores (AWS S3 / Azure)
