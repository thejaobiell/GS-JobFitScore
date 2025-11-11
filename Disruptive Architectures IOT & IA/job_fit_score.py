import google.generativeai as genai
import json
import re
import sys
import io
import time

# Corrige encoding no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuração da API
genai.configure(api_key="AIzaSyBXx44UQ3VUYMLbL-oiIyMi12CvpfZ-_SQ")
model = genai.GenerativeModel("gemini-1.5-flash")

dados = {
    "vaga": {
        "titulo": "Desenvolvedor Front-End React Native",
        "empresa": "TechFlow Solutions",
        "requisitos": [
            "React Native",
            "JavaScript",
            "TypeScript",
            "APIs REST",
            "Git",
            "UI/UX básico"
        ],
        "descricao": "Responsável por desenvolver e manter aplicativos móveis usando React Native, garantindo performance e boa experiência do usuário."
    },
    "candidatos": [
        {
            "nome": "Ana Souza",
            "habilidades": ["React Native", "JavaScript", "Figma", "UX Design", "Git"],
            "experiencia": "2 anos como desenvolvedora mobile em React Native",
            "cursos": ["React Native Avançado", "Design de Interfaces"]
        },
        {
            "nome": "Lucas Pereira",
            "habilidades": ["JavaScript", "TypeScript", "Node.js", "ReactJS"],
            "experiencia": "3 anos como desenvolvedor full-stack, iniciando com React Native",
            "cursos": ["ReactJS Completo", "APIs REST com Node.js"]
        },
        {
            "nome": "Mariana Lima",
            "habilidades": ["HTML", "CSS", "React Native", "APIs REST", "Git", "TypeScript"],
            "experiencia": "1 ano como estagiária em desenvolvimento mobile",
            "cursos": ["Introdução ao React Native", "Versionamento com Git"]
        }
    ]
}

prompt = f"""
Você é um avaliador técnico de compatibilidade entre candidatos e vagas de emprego.

Analise os dados abaixo em formato JSON. Compare as habilidades, experiências e cursos dos candidatos com os requisitos da vaga.

Para cada candidato, calcule um score de compatibilidade de 0 a 100 e retorne em formato JSON no seguinte modelo:

{{
  "avaliacoes": [
    {{
      "nome": "Nome do candidato",
      "score": número,
      "feedback": "breve explicação sobre a pontuação"
    }}
  ]
}}

Use os seguintes critérios:
- + pontos para cada habilidade que coincidir com os requisitos da vaga.
- Considere experiência e cursos relacionados como fator positivo.
- Diminua pontos se o candidato não tiver tecnologias essenciais da vaga.
- O score deve refletir a chance real de sucesso na vaga (0 a 100).

IMPORTANTE: Retorne APENAS o JSON, sem markdown ou explicações adicionais.

Dados:
{json.dumps(dados, ensure_ascii=False, indent=2)}
"""

try:
    print("🔄 Gerando avaliação dos candidatos...\n")
    resposta = model.generate_content(prompt)
    
    # Extrai o texto da resposta
    texto_resposta = resposta.text
    
    # Extrai o texto da resposta
    texto_resposta = resposta.text
    
    # Remove markdown se houver (```json ... ```)
    texto_limpo = re.sub(r'```json\s*|\s*```', '', texto_resposta).strip()
    
    # Tenta fazer parse do JSON
    try:
        resultado = json.loads(texto_limpo)
        
        # Exibe os resultados de forma formatada
        print("=" * 60)
        print(f"📋 VAGA: {dados['vaga']['titulo']}")
        print(f"🏢 EMPRESA: {dados['vaga']['empresa']}")
        print("=" * 60)
        print()
        
        for avaliacao in resultado['avaliacoes']:
            print(f"👤 {avaliacao['nome']}")
            print(f"   Score: {avaliacao['score']}/100")
            print(f"   📝 {avaliacao['feedback']}")
            print("-" * 60)
        
        # Salva o resultado em arquivo JSON
        with open('resultado_avaliacao.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print("\n✅ Resultado salvo em 'resultado_avaliacao.json'")
        
    except json.JSONDecodeError as e:
        print("⚠️  Não foi possível interpretar como JSON. Resposta bruta:")
        print(texto_resposta)
        print(f"\nErro: {e}")
        
except Exception as e:
    # Tratamento especial para erro de quota (429)
    erro_str = str(e)
    if "429" in erro_str or "quota" in erro_str.lower():
        print(f"❌ Erro de Quota da API Google Gemini!")
        print(f"\n📋 Detalhes: Você atingiu o limite de uso gratuito da API.")
        print(f"\n💡 Soluções:")
        print(f"   1. Aguarde alguns segundos e tente novamente")
        print(f"   2. Use um modelo diferente (ex: gemini-1.5-flash)")
        print(f"   3. Verifique seu plano em: https://ai.google.dev/pricing")
        print(f"   4. Gere uma nova API Key em: https://aistudio.google.com/apikey")
    else:
        print(f"❌ Erro ao gerar conteúdo: {e}")
