#this code is using playwright
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email_generator import EmailGenerator
from browser_automation import send_email_with_playwright
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

import sys
import asyncio

import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class EmailRequest(BaseModel):
    sender_email: str
    recipient_email: str
    subject: str
    body: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        print(f"Received request: {request.message}")
        email_generator = EmailGenerator()
        response = await email_generator.process_message(request.message)
        print(f"Email generator raw reply: {response}")

        email_details = response.get("reply")
        if isinstance(email_details, dict) and "recipient_email" in email_details:
            sender_email = os.getenv("GMAIL_ADDRESS", "mounikatestbanthry@gmail.com")
            app_password = os.getenv("GMAIL_APP_PASSWORD")

            # ✅ Await the async Playwright function
            screenshots = await send_email_with_playwright(
                sender_email,
                app_password,
                email_details["recipient_email"],
                email_details.get("subject", "Test Subject"),
                email_details.get("body", "Test Body")
            )

            response["screenshots"] = screenshots
            response["reply"] = f"Email sent successfully to {email_details['recipient_email']}!"
        return response

    except Exception as e:
        print("Error in chat endpoint:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/send-email")
async def send_email(request: EmailRequest):
    sender_email = os.getenv("GMAIL_ADDRESS", "mounikatestbanthry@gmail.com")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not app_password:
        raise HTTPException(status_code=500, detail="Missing APP_PASSWORD in .env file.")

    try:
        screenshots = await send_email_with_playwright(
            sender_email,
            app_password,
            request.recipient_email,
            request.subject,
            request.body
        )
        return {
            "status": "Email sent successfully",
            "screenshots": screenshots,
            "reply": f"Email sent to {request.recipient_email}!"
        }
    except Exception as e:
        print("Error in send-email endpoint:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")





# with smtp


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from email_generator import EmailGenerator
# from email_sender import send_email_smtp
# from fastapi.middleware.cors import CORSMiddleware
# import traceback

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str

# class EmailRequest(BaseModel):
#     sender_email: str
#     recipient_email: str
#     subject: str
#     body: str

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     try:
#         email_generator = EmailGenerator()
#         response = await email_generator.process_message(request.message)

#         email_content = response.get("reply")
#         if isinstance(email_content, str) and "To: " in email_content and "Subject: " in email_content:
#             success, screenshots = send_email_smtp(email_content)
#             response["reply"] = "✅ Email sent!" if success else f"❌ Failed to send email: {screenshots}"
#             response["screenshots"] = screenshots
#         return response
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))  
    