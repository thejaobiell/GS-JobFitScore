# API JobFitScore - Documentação de Endpoints

## Base URL
```
http://127.0.0.1:8000
```

## Endpoints disponíveis

### 1. GET /health
Verifica status da API e configurações.

**Response:**
```json
{
  "status": "ok",
  "use_model_default": true,
  "ollama_model": "llama3.2:3b",
  "ollama_url": "http://127.0.0.1:11434/api/generate"
}
```

---

### 2. POST /evaluate
Avalia candidatos estruturados contra uma vaga estruturada.

**Request:**
```json
{
  "vaga": {
    "titulo": "Desenvolvedor Front-End React Native",
    "empresa": "TechFlow Solutions",
    "requisitos": ["React Native", "JavaScript", "TypeScript", "APIs REST", "Git"],
    "descricao": "Responsável por desenvolver aplicativos móveis..."
  },
  "candidatos": [
    {
      "nome": "Ana Souza",
      "habilidades": ["React Native", "JavaScript", "Figma", "Git"],
      "experiencia": "2 anos como desenvolvedora mobile",
      "cursos": ["React Native Avançado"]
    }
  ],
  "use_model": true
}
```

**Response:**
```json
{
  "avaliacoes": [
    {
      "nome": "Ana Souza",
      "score": 78,
      "feedback": "Habilidades presentes: react native, javascript, git. Faltando: typescript, apis rest. Cursos relacionados: 1."
    }
  ]
}
```

---

### 3. POST /extract-resume
Extrai dados estruturados de um currículo em PDF.

**Request:** `multipart/form-data`
- `file`: arquivo PDF

**Response:**
```json
{
  "nome": "João Silva",
  "habilidades": ["Python", "Django", "PostgreSQL"],
  "experiencia": "3 anos como desenvolvedor backend",
  "cursos": ["Django para Produção", "SQL Avançado"]
}
```

---

### 4. POST /extract-self
Converte auto-descrição em texto livre para candidato estruturado.

**Request:**
```json
{
  "text": "Sou Ana, tenho 2 anos de experiência com React Native, TypeScript e Git. Fiz curso avançado de React Native.",
  "use_model": true
}
```

**Response:**
```json
{
  "nome": "Ana",
  "habilidades": ["React Native", "TypeScript", "Git"],
  "experiencia": "2 anos de experiência com React Native, TypeScript e Git",
  "cursos": ["React Native Avançado"]
}
```

---

### 5. POST /evaluate-self
Avalia auto-descrição contra vaga estruturada.

**Request:**
```json
{
  "vaga": {
    "titulo": "Desenvolvedor React Native",
    "empresa": "TechFlow",
    "requisitos": ["React Native", "TypeScript", "Git"]
  },
  "self_text": "Tenho 3 anos com React Native e Git, estou aprendendo TypeScript.",
  "use_model": true
}
```

**Response:**
```json
{
  "avaliacoes": [
    {
      "nome": "...",
      "score": 75,
      "feedback": "Habilidades presentes: react native, git. Faltando: typescript. Cursos relacionados: 0."
    }
  ]
}
```

---

### 6. POST /extract-job
Converte descrição de vaga em texto livre para vaga estruturada.

**Request:**
```json
{
  "text": "Procuramos Desenvolvedor React Native com conhecimento em TypeScript, Git e APIs REST para atuar na TechFlow Solutions desenvolvendo apps móveis.",
  "use_model": true
}
```

**Response:**
```json
{
  "titulo": "Desenvolvedor React Native",
  "empresa": "TechFlow Solutions",
  "requisitos": ["React Native", "TypeScript", "Git", "APIs REST"],
  "descricao": "Desenvolver apps móveis"
}
```

---

### 7. POST /evaluate-texts ⭐ (Mais simples para o front)
Recebe descrição da vaga E auto-descrição do candidato em texto livre. Extrai tudo via IA e retorna a avaliação.

**Request:**
```json
{
  "job_text": "Vaga para Desenvolvedor React Native com TypeScript e Git na empresa TechFlow.",
  "self_text": "Sou Lucas, 2 anos com React Native e TypeScript, experiência com Git.",
  "use_model": true
}
```

**Response:**
```json
{
  "avaliacoes": [
    {
      "nome": "Lucas",
      "score": 85,
      "feedback": "Habilidades presentes: react native, typescript, git. Faltando: nenhuma. Cursos relacionados: 0."
    }
  ]
}
```

---

## Parâmetro `use_model`

- `true` (padrão): Usa Ollama para extração/avaliação inteligente
- `false`: Usa fallback determinístico (sempre funciona, mesmo sem IA)

Se o Ollama não estiver disponível, a API automaticamente cai no fallback.

---

## Fluxo recomendado para o front

### Opção 1: Mais simples (texto para texto)
```
Empresa digita descrição → POST /extract-job → Vaga estruturada
Candidato digita auto-descrição → POST /evaluate-texts → Score + Feedback
```

### Opção 2: Upload de PDF
```
Candidato faz upload de PDF → POST /extract-resume → Candidato estruturado
Empresa digita descrição → POST /extract-job → Vaga estruturada
Front envia ambos → POST /evaluate → Score + Feedback
```

### Opção 3: Candidato digita texto
```
Empresa digita descrição → POST /extract-job → Vaga estruturada
Candidato digita auto-descrição → POST /extract-self → Candidato estruturado
Front envia ambos → POST /evaluate → Score + Feedback
```

### Opção 4: Tudo em um endpoint (RECOMENDADO)
```
Front coleta:
- job_text (da empresa)
- self_text (do candidato)

POST /evaluate-texts → Score + Feedback direto
```

---

## CORS

Por padrão aceita todas as origens (`*`). Para restringir ao seu front:

```powershell
.\run_api.ps1 -Cors "http://localhost:3000,http://localhost:5173"
```

Ou via variável de ambiente:
```powershell
$env:CORS_ORIGINS = "http://localhost:3000"
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000
```

---

## Rodar a API

**Duplo clique:**
- `run_api.ps1`

**Terminal:**
```powershell
.\run_api.ps1
# ou
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000
```

**Documentação interativa:**
- http://127.0.0.1:8000/docs (Swagger UI)
- http://127.0.0.1:8000/redoc
