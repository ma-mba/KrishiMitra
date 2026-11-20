
from pathlib import Path
import json
import onnxruntime as ort

model_dir = Path("models/multilingual_minilm")

print("AVAILABLE ONNX MODELS")
print("=" * 60)

onnx_files = sorted(model_dir.rglob("*.onnx"))

if not onnx_files:
    print("No ONNX files found.")
    raise SystemExit(1)

for file in onnx_files:
    size_mb = file.stat().st_size / (1024 * 1024)
    print(f"{file} | {size_mb:.2f} MB")

print("\nPOOLING CONFIGURATION")
print("=" * 60)

pooling_path = model_dir / "1_Pooling" / "config.json"

if pooling_path.exists():
    with open(pooling_path, encoding="utf-8") as f:
        print(json.dumps(json.load(f), indent=2))
else:
    print("Pooling configuration not found.")

print("\nMODEL INPUTS AND OUTPUTS")
print("=" * 60)

# Inspect the smallest ONNX file first
model_path = min(
    onnx_files,
    key=lambda file: file.stat().st_size
)

print("Inspecting:", model_path)

try:
    session = ort.InferenceSession(
        str(model_path),
        providers=["CPUExecutionProvider"]
    )

    print("\nInputs:")
    for item in session.get_inputs():
        print(item.name, item.shape, item.type)

    print("\nOutputs:")
    for item in session.get_outputs():
        print(item.name, item.shape, item.type)

except Exception as e:
    print("Model could not be loaded:")
    print(type(e).__name__, str(e))
