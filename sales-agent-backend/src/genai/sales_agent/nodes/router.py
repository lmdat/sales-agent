import os
import json
from dotenv import load_dotenv, find_dotenv
from litellm import completion
from ..schemas.topic import TopicSchema
from pydantic.tools import parse_obj_as
from ..states.sales_agent_state import SalesAgentState
from ..utils.helpers import parsing_messages_to_history, remove_think_tag
from logger import logger
from config import LLM_MODELS

load_dotenv(find_dotenv())

TOPIC = {
    "greeting": "greeting",
    "off_topic": "off_topic",
    "company_info": "company_info",
    "product_consulting": "product_consulting",
    "make_order": "make_order",
    "wanna_exit": "wanna_exit"
}

def router_node(state: SalesAgentState):
    user_input = state['messages'][-1].content
    chat_history = parsing_messages_to_history(state.get('messages', ''))

    json_example = {
        "name": f"Một trong các giá trị sau: {', '.join(TOPIC.values())}",
        "confidence": "Score between 0 and 1",
        "context": "User's input"
    }

    prompt = f"""
    # Role
    - Asssistant là một chuyên gia phân tích, trích xuất dữ liệu với 10 năm kinh nghiệm.

    # Skills
    - Assistant có kỹ năng Sales.
    - Assistant có kỹ năng phân tích nội dung văn bản trong lĩnh vực Sales.

    # Context
    ```
    Chat History:
    {chat_history}

    User's input:
    {user_input}

    ```

    # Tasks
    - Assistant MUST đọc thật kỹ nội dung Chat History và User's input trong mục Context để xác định chính xác ý định của User.
    - Assistant MUST phân loại ý định của User theo các topic như sau:
    1. Greeting:
        - Nếu User greets Assistant. Return "{TOPIC.get("greeting")}"
        - Example:
            - Hi
            - Hello
            - Alo
            - Xin chào
            - Chào em
            - Em ơi
            - Em ơi, cho Anh (Chị) hỏi chút
            - Cho Anh (Chị) hỏi một chút
            - Có ai không, cho hỏi chút

    2. Thông tin công ty:
        - Nếu User hỏi Assistant những thông tin chung liên quan đến công ty hoặc những dịch vụ, chính sách của công ty. Return "{TOPIC.get("company_info")}"
        - Example:
            - Công ty em ở đâu.
            - Địa chỉ công ty là gì em?
            - Em cho anh/chị hỏi công ty em ở đâu?
            - Thương hiệu này của ai vậy em?
            - Nhãn hàng này của ai vậy em?
            - Giới thiệu anh về công ty mình nha
            - Brand mình của ai?
            - Thông điệp của nhãn hàng mình là gì á?
            - Chính sách đổi trả
            - Chính sách bảo mật
            - Chính sách vận chuyển
            - Điều khoản và dịch vụ   

    3. Tư vấn sản phẩm:
        - Nếu User hỏi Assistant những thông tin về sản phẩm của công ty. Return "{TOPIC.get("product_consulting")}"
        - Example:
            - Bên mình có sản phẩm nào vậy em?
            - Da anh bị dầu thì dùng sản phẩm nào em?
            - Mặt anh bị mụn thì dùng sản phẩm nào?
            - Dưỡng ẩm da thì dùng sản phẩm nào vậy em?
            - Tư vấn giúp chị sữa rửa mặt.
            - Sữa rửa mặt loại nào tốt
            - Mua nhiều có được giảm giá hok em?
            - Có gì rẻ khoảng 500k hok em?
            - Em có bán nước hoa không?
            - Bên em có bán xà phòng thiên nhiên hok?            
            - xà phòng thiên nhiên là gì vậy em?   

    4. Đặt hàng:
        - Nếu User có ý muốn đặt hàng, mua hàng những sản phẩm mà Assistant đã tư vấn. Return "{TOPIC.get("make_order")}"
        - Example:
            - Anh mua 3 chai tinh dầu bạc hà, 2 cục xà phòng nha.
            - Anh muốn mua sản phẩm này.
            - Anh muốn đặt hàng.
            - Lấy anh sản phẩm này luôn nha.
            - Chốt đơn giúp anh.
            - Lấy anh 2 chai tinh dầu đi.
            - Lấy anh 3 cục xà phòng đi.
            - OK, lấy anh món đó nha.
            - Cho anh order cái đó.
            - Cho đặt hàng 3 dầu gội này nha.   

    5. Off Topic:
        - Nếu câu hỏi không liên quan đến các topic trên. Return "{TOPIC.get("off_topic")}"
        - Example:
            - Làm thơ đi em.
            - Viết code đi em.
            - Viết một bài.
            - Đi nhậu với anh nha.
            - Đi chơi không em.

    6. Exit:
        - Nếu User có ý định không muốn tiếp tục trò chuyện, không muốn tư vấn hoặc không muốn mua sản phẩm. Return "{TOPIC.get("wanna_exit")}"
        - Example:
            - Thôi anh/chị không muốn mua nữa, để khi khác nha.
            - Thôi, lâu lắc quá, không mua nữa.
            - Anh/Chị không muốn đặt hàng nữa.
            - Em hủy đơn hàng giúp anh/chị nha.
            - Thôi để khi khác mua nha.
            - Để anh suy nghĩ thêm.
            - Anh không mua nữa, để lần sau nha.

    # Ouput
    - Assistant MUST trả lời bằng JSON format với các field như sau:
    ```
    {json.dumps(json_example, ensure_ascii=False)}
    ```

    # Constraints
    - Assistant MUST reply by JSON format ONLY như trong mục Output. No need explaination.
    - Assistant MUST return exactly one of the following topics: {', '.join(TOPIC.values())}.
    - Trong trường hợp Assistant không thể xác định được topic, Assistant DO NOT attempt to guess the topic, just return "{TOPIC.get("off_topic")}".
    """

    response = completion(
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLM_MODELS['router']['router_node'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        response_format=TopicSchema
    )

    new_topic = parse_obj_as(TopicSchema, json.loads(remove_think_tag(response.choices[0].message.content)))
    new_topic.name = new_topic.name.lower()

    topic = state.get('topic', None)
    logger.info(f"Topic: {topic}")
    
    if topic is None:
        if new_topic.name != TOPIC.get('off_topic') and new_topic.confidence < 0.5:
            new_topic.name = TOPIC.get('off_topic')

        logger.info(f"New Topic: {new_topic}")
        return {
            "topic": new_topic,
            "human_input": user_input,
            "ai_reply": None
        }

    return {
        "human_input": user_input,
        "ai_reply": None
    }
    