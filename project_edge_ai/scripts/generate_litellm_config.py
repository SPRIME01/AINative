#!/usr/bin/env python3
import yaml
import argparse
import os

DEFAULT_CONFIG = {
    "proxy_server": True,
    "port": 4000,
    "model_list": [
        {"model_name": "ollama-mistral", "litellm_provider": "ollama", "api_base": "http://localhost:11434", "ollama_model_name": "mistral"},
        {"model_name": "triton-codellama", "litellm_provider": "triton", "api_base": "http://localhost:8001", "triton_model_name": "codellama"},
        {"model_name": "default", "litellm_provider": "ollama", "api_base": "http://localhost:11434", "ollama_model_name": "mistral"}
    ],
    "litellm_settings": {
        "set_verbose": True
    },
    # Add other LiteLLM settings as needed, e.g., telemetry, health checks
    # "telemetry": False,
    # "health_check_models": ["ollama-mistral"]
}

def write_config(output_path: str, config: dict):
    """Writes the LiteLLM configuration to a YAML file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)
    print(f"Wrote LiteLLM config to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a LiteLLM configuration file.")
    parser.add_argument(
        "--output",
        default="project_edge_ai/backend/src/ainative/config/litellm.config.yaml",
        help="Path to output the LiteLLM config file (e.g., config/litellm.config.yaml)"
    )
    # Add more arguments here to customize the config, e.g., port, model details

    args = parser.parse_args()

    # For now, we use the DEFAULT_CONFIG.
    # In a more advanced version, you could modify DEFAULT_CONFIG based on other CLI args.
    current_config = DEFAULT_CONFIG

    write_config(args.output, current_config)
