
from pathlib import Path
from huggingface_hub import hf_hub_download

MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_FILE = "onnx/model_quint8_avx2.onnx"

model_dir = Path(__file__).resolve().parent / "models" / "multilingual_minilm"
model_path = model_dir / MODEL_FILE

if model_path.exists():
    print("ONNX model already exists.")
else:
    print("Downloading required ONNX model...")

    hf_hub_download(
        repo_id=MODEL_ID,
        filename=MODEL_FILE,
        local_dir=model_dir
    )

    print("Model downloaded successfully!")

print(f"Model location: {model_path}")
