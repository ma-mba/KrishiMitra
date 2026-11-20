
from huggingface_hub import list_repo_files, snapshot_download

model_id = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

print("Checking available model files...")

files = list_repo_files(model_id)

onnx_files = [
    file for file in files
    if file.endswith(".onnx")
]

print("Available ONNX files:", onnx_files)

if onnx_files:
    print("\nDownloading ONNX model and tokenizer...")

    snapshot_download(
        repo_id=model_id,
        local_dir="models/multilingual_minilm",
        allow_patterns=[
            "*.onnx",
            "*.onnx_data",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "config.json",
            "vocab.txt",
            "sentencepiece.bpe.model",
            "1_Pooling/config.json"
        ]
    )

    print("\nDownload complete!")
else:
    print("\nNo ONNX model found in this repository.")
    print("We will use a verified pre-exported alternative.")
   