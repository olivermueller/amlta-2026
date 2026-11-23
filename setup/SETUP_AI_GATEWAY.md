# Using the AI-Gateway of Paderborn University

**In short: request access once, create an API key, paste it into `.env`, and set `"provider": "ai-gateway"` in the notebooks.**

The **AI-Gateway** gives you access to large language models with your university account. It speaks the OpenAI-compatible API, so the notebooks talk to it with LangChain's `ChatOpenAI`, like to every other provider.

| Step | What you do | Once or every time? |
|---|---|---|
| 1 | Request access | once |
| 2 | Create an API key | once (again when the key expires) |
| 3 | Paste the key into `.env` | once |
| 4 | Set `"provider": "ai-gateway"` in the notebook | every notebook |

---

## Step 1: Request access

1. Open the [Service-Portal](https://sp.upb.de) and log in with your university account.
2. Go to **Benutzerverwaltung** → **Weitere Dienste** → tab **Lehre und Studium**.
3. Find **KI-Chat-Oberfläche**, click **Optionen** → **Beantragen**. Access is granted automatically.

The full instructions, including the terms of use: [hilfe.uni-paderborn.de/AI-Gateway#Beantragen](https://hilfe.uni-paderborn.de/AI-Gateway#Beantragen)

After that, you can log in with your university account on two pages:

| Page | What it is for |
|---|---|
| [ai-gateway.upb.de](https://ai-gateway.upb.de) | API keys, for using the models from code (the notebooks) |
| [ai-chat.upb.de](https://ai-chat.upb.de) | chatting with the models in the browser |

---

## Step 2: Create an API key

1. Connect to the university network or the VPN.
2. Open [ai-gateway.upb.de](https://ai-gateway.upb.de) and log in.
3. Click **API-Key erstellen** and copy the key.

Treat the key like a password. Keys expire after a while; then you simply create a new one.

---

## Step 3: Paste the key into `.env`

In the repo folder (the one that contains `Session_04`, `Session_05`, ...), copy `.env.example` to `.env`, if you have not done so yet:

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Open `.env` and paste your key behind `AI_GATEWAY_KEY=` (no quotes, no spaces). The block for the gateway then looks like this:

```
# provider "ai-gateway": AI-Gateway of Paderborn University
AI_GATEWAY_KEY=<your key>
AI_GATEWAY_BASE=https://ai-gateway.uni-paderborn.de/v1
```

| Name in `.env` | What it is |
|---|---|
| `AI_GATEWAY_KEY` | your key from Step 2 |
| `AI_GATEWAY_BASE` | the address of the gateway; keep it as it is |

All notebooks of the course read the key from this one file. **Never commit or share `.env`.** It is listed in `.gitignore`, so Git ignores it.

---

## Step 4: Set the provider in the notebook

In the cell after `setup_model()`, write:

```python
MODEL = {"model_name": "gwdg.qwen3.8-27b-no-think", "provider": "ai-gateway"}
```

`gwdg.qwen3.8-27b-no-think` is Qwen3.8 with 27 billion parameters, with thinking switched off. For thinking, use `gwdg.qwen3.8-27b`: on the gateway, the model name decides, not `reasoning_effort`. `setup_model()` prints the model and what to keep in mind; the key is never printed.

| Good to know | |
|---|---|
| **Network** | The gateway only answers in the university network or the VPN. |
| **Colab** | Google Colab runs outside the university network and cannot reach the gateway. Run the notebooks on your own computer, or use the provider `"colab"` (Ollama on Colab). |
| **Requests per minute** | The gateway allows about 10 requests per minute per model. If a cell pauses, the client is waiting and then continues by itself. |
| **Other models** | The gateway has more models. Put another id into `"model_name"`; `llm.root_client.models.list()` in a notebook lists the ids your account can use. |

An error in the setup cell or with the first request? Check the VPN, and check that the key in `.env` is complete and not expired.
