# 🌱 KrishiMitra
### AI-Powered Crop Health, Soil Monitoring and Agricultural Advisory Platform

KrishiMitra is an AI-powered agricultural assistance platform designed to help farmers monitor crop health, evaluate soil conditions, understand weather-related risks, and make informed farming decisions.

The platform combines machine learning, agricultural knowledge retrieval, weather information, and a farmer-friendly interface.

## Key Features

- **Crop Disease Detection:** Identifies supported plant diseases from uploaded leaf images using a deep learning model.
- **Crop Recommendation:** Recommends suitable crops based on soil nutrients and environmental conditions.
- **Soil Health Analysis:** Evaluates soil parameters and provides rule-based recommendations.
- **Weather Monitoring:** Retrieves weather information to support agricultural decisions.
- **AI Agricultural Assistant:** Answers farming questions using agricultural knowledge resources.
- **Multilingual Support:** Provides English and Malayalam interface support.
- **Farmer Community:** Includes features for farmer interaction and communication.

## Technologies Used

- Python
- Streamlit
- PyTorch
- Scikit-learn
- ONNX Runtime
- Pandas and NumPy
- Open-Meteo API

## Project Structure

```text
KrishiMitra/
├── app.py
├── pages/
├── services/
├── models/
├── data/
├── scripts/
├── assets/
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

   `git clone https://github.com/ma-mba/KrishiMitra.git`

2. Navigate to the project directory:

   `cd KrishiMitra`

3. Create and activate a Python virtual environment.

4. Install dependencies:

   `pip install -r requirements.txt`

5. Start the application:

   `streamlit run app.py`

**Note:** Some model files are excluded from GitHub because of their size. Additional model setup may be required before all features work.

## Project Objectives

- Support early identification of crop diseases.
- Recommend suitable crops using machine learning.
- Help farmers understand soil conditions.
- Provide agricultural guidance based on weather and knowledge resources.
- Improve accessibility through multilingual support.

## Contributors

- Mekha Sindhu
- Mariya T Thomas

## Project Status

Academic project under active development. Some features require additional testing and deployment configuration.