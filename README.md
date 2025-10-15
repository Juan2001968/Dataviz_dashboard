
# 💼 Finanzas de Empresas — Streamlit + Docker + Render

## Ejecutar local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Docker local
```bash
docker build -t finanzas-app .
docker run -p 8501:8501 -v $PWD:/app finanzas-app
```

## Despliegue en Render
1. Sube este repo a GitHub.
2. En Render -> **New** -> **Web Service** -> **Build & deploy from repository**.
3. Render detectará `Dockerfile`. No cambies el start command.
4. Cuando esté listo, comparte el **URL público**.
```

Estructura mínima:
```
.
├── app.py
├── pages/
│   ├── 1_🏠_Contexto.py
│   ├── 2_📊_Analisis.py
│   └── 3_🗺️_Mapa.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── render.yaml
```
