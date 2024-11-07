from huggingface_hub import snapshot_download
from pathlib import Path

# Set the custom path for saving the model
mistral_models_path = Path("D:\\Projects\\MotorMate\\Model")
mistral_models_path.mkdir(parents=True, exist_ok=True)

# Download the model files to the custom directory
snapshot_download(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    allow_patterns=["params.json", "consolidated.safetensors", "tokenizer.model.v3"],
    local_dir=mistral_models_path
)
