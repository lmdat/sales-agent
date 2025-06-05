from langchain_core.messages import HumanMessage
from genai.sales_agent.agent import build_graph
from logger import logger
from datetime import datetime
from termcolor import colored


def main():
    configurable = {
        "configurable": {
            "thread_id": "1"
        }
    }

    graph = build_graph()

    while True:
        try:
            user_input = input(">>> User: ")
            print(end="\n")
            if user_input.lower().strip() in ['q', 'quit', 'exit']:
                print(colored(">>> Assistant: Bye!", 'yellow'), end="\n\n")
                exit(0)
            
            response = graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input, additional_kwargs={"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    ]
                },
                config=configurable
            )
            ai_reply = response.get('ai_reply', None)
            if ai_reply is None:
                print(colored(">>> Assistant: ---Unknown---", 'yellow'), end="\n\n")
            else:
                print(colored(f">>> Assistant: {ai_reply.content}", "yellow"), end="\n\n")
        except KeyboardInterrupt:
            print("\n.::.Service terminated!")
            exit(0)

if __name__ == "__main__":
    main()