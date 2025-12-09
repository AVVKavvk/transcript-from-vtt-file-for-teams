import json
from datetime import datetime
from typing import List, Literal, Optional, Dict, cast
from pydantic import BaseModel, Field, SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from fastapi import HTTPException
from app.core.config.setting import LocalSettings
from app.core.models.llm import MeetingExtraction


async def extract_tasks_with_deepseek(
    meeting_title: str,
    meeting_date: str,
    participants: List[Dict],
    transcript: str
) -> MeetingExtraction:
    """Extract tasks using DeepSeek via LangChain with Pydantic structured output"""

    DEEPSEEK_API_KEY = LocalSettings.DEEPSEEK_API_KEY
    DEEPSEEK_BASE_URL = LocalSettings.DEEPSEEK_BASE_URL or "https://api.deepseek.com/v1"

    if not DEEPSEEK_BASE_URL:
        raise HTTPException(status_code=500, detail="DEEPSEEK_BASE_URL not configured")

    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY not configured")

    # Initialize DeepSeek model
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=SecretStr(DEEPSEEK_API_KEY),
        base_url=DEEPSEEK_BASE_URL,
        temperature=0.1,
        max_retries=2
    )

    # 1. Get the Raw Schema to inject into the prompt
    # This ensures the LLM sees exactly what field names (camelCase vs snake_case) are required.
    schema_json = json.dumps(MeetingExtraction.model_json_schema(), indent=2)

    structured_llm = llm.with_structured_output(MeetingExtraction, method="json_mode")

    # 2. Update Prompt: Inject Schema & Fix Priority Instructions
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI assistant that extracts actionable tasks from meeting transcripts.

            INSTRUCTIONS:
            1. Identify all actionable NEXT STEPS.
            2. Assign each task to exactly ONE participant.
            3. Extract participant's email if mentioned.
            4. Determine priority. IMPORTANT: You must use these exact lowercase values:
            - 'high': Urgent, critical, blocking
            - 'medium': Normal work items
            - 'low': Nice-to-have, ideas
            5. Extract due dates (ISO8601) if mentioned.
            6. Provide context.

            CRITICAL: You must output a valid JSON object that strictly matches the following schema.
            Do not make up field names. Use the exact keys defined here:

            {schema}
            """),
                    ("user", """MEETING INFORMATION:
            Title: {meeting_title}
            Date/Time: {meeting_date}

            PARTICIPANTS:
            {participants}

            FULL TRANSCRIPT:
            {transcript}

            Extract all tasks and generate summary in JSON.""")
        ])

    # Format participants
    participant_str = '\n'.join([
        f"- {p['name']}" + (f" ({p['email']})" if p.get('email') else "")
        for p in participants
    ])

    # Generate structured response
    chain = prompt_template | structured_llm

    result = cast(MeetingExtraction, await chain.ainvoke({
        "meeting_title": meeting_title,
        "meeting_date": meeting_date or "Not specified",
        "participants": participant_str,
        "transcript": transcript[:15000],
        "schema": schema_json  # Pass the schema string here
    }))

    return result
