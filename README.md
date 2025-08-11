# Monitoramento de Gateways Power BI com Notificação via WhatsApp e E-mail

Este programa monitora o status dos gateways do Power BI e envia alertas quando algum gateway estiver **offline** (status diferente de `Live` ou `Online`).  

As notificações são enviadas via **Evolution API (WhatsApp)** e, caso falhem, é feito um **fallback por e-mail**.  
Se o e-mail também falhar, a mensagem é salva no arquivo `alert_fallback.log`.

---

## 📦 Funcionalidades

- Consulta status dos gateways do Power BI via API.
- Envia alerta via **WhatsApp (Evolution API)**.
- Fallback para **e-mail** se o WhatsApp falhar.
- Fallback final para **arquivo `.log`** se o e-mail falhar.
- Log estruturado no console.
- Pode ser executado manualmente ou agendado para execução automática.

---

## ⚙️ Pré-requisitos

- Python 3.10+ instalado.
- Conta no Power BI com permissão para ler status dos gateways.
- Evolution API ativa e configurada para envio de mensagens.
- Conta de e-mail SMTP para envio dos alertas por e-mail.

---

## 📂 Estrutura do Projeto

```plaintext
├───app/
    ├── config.py             # Leitura de variáveis de ambiente e configurações
    ├── powerbi.py            # Funções de integração com API do Power BI
    ├── whatsapp.py           # Funções para envio de mensagens via Evolution API
    ├── email_notifier.py     # Funções para envio de e-mails via SMTP
├── main.py               # Script de execução
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente
└── alert_fallback.log    # Log de fallback (gerado em caso de falha de envio)
```

---

## 📄 Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# --- Power BI ---
PBI_BEARER=Bearer SEU_TOKEN_AQUI
SVD_DOMINIO=ID_GATEWAY_DOMINIO
SVD2_AUXILIAR=ID_GATEWAY_AUXILIAR

# --- Evolution API (WhatsApp) ---
EVOLUTION_URL=http://seu-endereco-evolution
EVOLUTION_INSTANCE=INSTANCIA
EVOLUTION_TOKEN=SUA_APIKEY
WHATSAPP_TO=5511999999999, 5511888888888  # múltiplos números separados por vírgula

# --- E-mail (SMTP) ---
EMAIL_USER=usuario@dominio.com
EMAIL_PASS=senha
EMAIL_TO=destinatario1@dominio.com, destinatario2@dominio.com
EMAIL_HOST=smtp.seuprovedor.com
EMAIL_PORT=587
```

> **Atenção**: O `PBI_BEARER` expira rápido. O ideal é implementar autenticação via Microsoft Entra ID para gerar tokens automaticamente.

---

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone https://seu-repositorio.git
   cd AvisoGatewayPBI
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # no Windows
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` conforme o exemplo acima.

---

## ▶️ Execução Manual

No terminal, execute:
```bash
venv\Scripts\python.exe main.py
```

---

## ⏱️ Agendamento Automático (Windows)

Para rodar automaticamente **a cada 15 minutos, de segunda a sábado, das 08:00 às 18:30**:

1. Abra o **Agendador de Tarefas** (`taskschd.msc`).
2. Crie uma nova tarefa:
   - Ação: executar o Python do seu ambiente virtual com caminho completo do `main.py`.
   - Disparador: repetir a cada 15 minutos dentro do intervalo desejado.
3. Salve e teste a tarefa.

---

## 📜 Licença

Este projeto é de uso interno do Grupo Top Fama.
