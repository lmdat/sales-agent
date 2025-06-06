import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

APP_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LLM_MODELS = {
    "router": {
        "router_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    },
    "greeting_subgraph": {
        "greeting_node": os.getenv('GROQ_LLM_MODEL_LLAMA_70B')
    },
    "off_topic_subgraph": {
        "off_topic_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    }
}