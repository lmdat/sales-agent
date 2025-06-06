import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import AIMessage
from ...states.sales_agent_state import SalesAgentState
from litellm import completion
from logger import logger
from ...utils.helpers import parsing_messages_to_history, remove_think_tag
from ...utils.const_prompts import (
    CONST_ASSISTANT_ROLE,
    CONST_ASSISTANT_SKILLS,
    CONST_ASSISTANT_TONE,
    CONST_FORM_ADDRESS_IN_VN,
    CONST_ASSISTANT_SCOPE_OF_WORK,
    CONST_ASSISTANT_PRIME_JOB
)
from config import LLM_MODELS

load_dotenv(find_dotenv())


def greeting_node(state: SalesAgentState):
    logger.info("greeting_node called.")
    user_input = state['messages'][-1].content
    chat_history = parsing_messages_to_history(state.get('messages', ''))

    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}

    # Tasks
    - User will greet Assistant to start the conversation. Assistant MUST kindly greet User back.
    - Then Assistant introduces about yourself, as well as what Asssistant can support:
        {CONST_ASSISTANT_SCOPE_OF_WORK}
    {CONST_ASSISTANT_PRIME_JOB}

    # Constraints
    - Assistant's works MUST be formatted in an easy to read manner. Highly recommend list in bullet point format.
    - When User says "sticker", "emoji", "icon" or something undefined, Assistant MUST greet User again.
    - Keep the answers concise and under 200 words.
    - Assistant MUST use the same language as the User's language to reply.   
    {CONST_FORM_ADDRESS_IN_VN}

    Chat History:
    ```
    {chat_history}
    ```

    User's input: {user_input}
    Answer:
    """

    response = completion(
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLM_MODELS['greeting_subgraph']['greeting_node'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    ai_message = AIMessage(
        content=remove_think_tag(response.choices[0].message.content),
        additional_kwargs={"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )

    return {
        "messages": ai_message,
        "ai_reply": ai_message
    }

