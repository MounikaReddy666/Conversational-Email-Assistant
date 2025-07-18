
# #this above code for playwright browser automation
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_ollama import OllamaLLM
# import os
# from dotenv import load_dotenv
# import re
# import json
# import asyncio

# load_dotenv()

# class EmailGenerator:
#     def __init__(self):
#         self.llm = OllamaLLM(model="llama3.2:1b", base_url="http://localhost:11434")
#         self.history = ChatMessageHistory()
#         self.system_prompt = """
#         You are an email assistant. For every response, return a JSON object with the following fields: recipient_email, subject, body, and sender_email (default to test@assistant.com if not provided). No narrative text, only JSON. Infer details from the input or history. If details are missing, use placeholder values and include a needs_clarification field set to true.

#         Examples of expected output:
#         - Input: "Send a hi mail to test@example.com"
#           Output: {{"recipient_email": "test@example.com", "subject": "Hi", "body": "Hi, this is a test email.", "sender_email": "test@assistant.com", "needs_clarification": false}}

#         - Input: "Send a mail to friend@example.com asking how are you from myemail@test.com, my name is John"
#           Output: {{"recipient_email": "friend@example.com", "subject": "Checking In", "body": "Hi, this is John from myemail@test.com. How are you?", "sender_email": "myemail@test.com", "needs_clarification": false}}

#         - Input: "Yes"
#           Output: {{"recipient_email": "last_recipient@example.com", "subject": "Last Subject", "body": "Last Body", "sender_email": "last_sender@example.com", "needs_clarification": false}}

#         - Input: "Send a mail"
#           Output: {{"recipient_email": "placeholder@example.com", "subject": "Default Subject", "body": "Default body.", "sender_email": "test@assistant.com", "needs_clarification": true}}
#         """
#         self.prompt = ChatPromptTemplate.from_messages([
#             ("system", self.system_prompt),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{input}")
#         ])
#         self.chain = self.prompt | self.llm
#         self.runnable = RunnableWithMessageHistory(
#             runnable=self.chain,
#             get_session_history=lambda session_id: self.history,
#             input_messages_key="input",
#             history_messages_key="history"
#         )

#     async def process_message(self, message):
#         try:
#             response = await self.runnable.ainvoke(
#                 {"input": message, "history": self.history.messages},
#                 config={"configurable": {"session_id": "default"}}
#             )
#             content = str(response).strip()
#             content = content.replace("\n", "").replace(" ", "")
#             if not content.startswith("{") or not content.endswith("}"):
#                 content = content[content.find("{"):content.rfind("}") + 1]

#             try:
#                 email_details = json.loads(content)
#                 if not all(key in email_details for key in ["recipient_email", "subject", "body", "sender_email"]):
#                     raise json.JSONDecodeError("Missing required fields", content, 0)
#                 if email_details.get("needs_clarification", False):
#                     return {"reply": content, "screenshots": []}
#                 return {"reply": email_details, "screenshots": []}
#             except json.JSONDecodeError as e:
#                 print(f"JSON Decode Error: {str(e)} - Response: {content}")
#                 return {"reply": f"Error: Invalid JSON - {str(e)}", "screenshots": []}
#         except Exception as e:
#             print(f"Error in email generation: {str(e)}")
#             return {"reply": f"Error processing message: {str(e)}", "screenshots": []}





# #with smtp

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import OllamaLLM
import os
from dotenv import load_dotenv
import re
import json
import asyncio
from datetime import datetime

load_dotenv()

class EmailGenerator:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2:1b", base_url="http://localhost:11434")
        self.history = ChatMessageHistory()
        self.system_prompt = """
        You are an email assistant. Generate a natural, professional email based on the user's input. Include a recipient email, subject, and body. Ensure the recipient name is spelled correctly based on the input (e.g., "boggarimounikareddy@gmail.com" should be "Mounika Reddy Boggari"). If details are missing, ask a follow-up question in a friendly tone. The body MUST end with "Regards,\nMounika Reddy Boggari" and should not include a separate signature block like "[Your Name]". Return the response as a string in this format:
        "To: [recipient_email]\nSubject: [subject]\n\n[body]\nRegards,\nMounika Reddy Boggari"
        If asking a question, return: "Please provide [missing_detail] (e.g., recipient email, subject, or body)."
        """
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.chain = self.prompt | self.llm
        self.runnable = RunnableWithMessageHistory(
            runnable=self.chain,
            get_session_history=lambda session_id: self.history,
            input_messages_key="input",
            history_messages_key="history"
        )

    async def process_message(self, message):
        response = await self.runnable.ainvoke(
            {"input": message, "history": self.history.messages},
            config={"configurable": {"session_id": "default"}}
        )
        content = str(response).strip()
        print(f"LLM Response: {content}")

        # Ensure the signature is appended if missing
        if "\nRegards,\nMounika Reddy Boggari" not in content:
            lines = content.split('\n')
            if len(lines) >= 3 and lines[0].startswith("To: ") and lines[1].startswith("Subject: "):
                body_start = 2
                body_end = len(lines) - 1
                body = '\n'.join(lines[body_start:body_end]).strip()
                content = f"{lines[0]}\n{lines[1]}\n\n{body}\nRegards,\nMounika Reddy Boggari"

        return {"reply": content, "screenshots": [f"mock_screenshot_{datetime.now().strftime('%H%M%S')}.png"]}


