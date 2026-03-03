# Car Make Guesser (Streamlit + Python)

A Streamlit app that guesses the **car make** from an uploaded photo.

## 1) Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL shown in your terminal (usually `http://localhost:8501`).

## 2) Deploy to Azure App Service

### Prerequisites
- Azure subscription
- Azure CLI installed
- Git installed

### Azure deploy steps

```bash
az login
az group create --name rg-car-make-guesser --location westeurope
az appservice plan create --name asp-car-make-guesser --resource-group rg-car-make-guesser --sku B1 --is-linux
az webapp create --resource-group rg-car-make-guesser --plan asp-car-make-guesser --name <your-unique-app-name> --runtime "PYTHON|3.11"
az webapp config set --resource-group rg-car-make-guesser --name <your-unique-app-name> --startup-file "sh -c 'streamlit run app.py --server.port $PORT --server.address 0.0.0.0'"
```

Deploy your current folder:

```bash
az webapp up --resource-group rg-car-make-guesser --name <your-unique-app-name> --runtime "PYTHON|3.11"
```

Open your app:

```bash
az webapp browse --resource-group rg-car-make-guesser --name <your-unique-app-name>
```

## Notes
- First startup can take longer because model files are downloaded.
- For better prediction quality, upload a clear photo of one car.
- The app performs make-level guessing (not exact model/year).
