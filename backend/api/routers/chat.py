import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.models.chat import ChatRequest, ChatResponse, ChatMessage, ConversationDB, MessageDB
from api.models.user import UserDB
from api.models.database import get_db
from api.core.deps import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)



from api.services.llm_service import get_llm_service
from api.services.meal_plan_service import get_meal_plan_service
from api.services.sunbird import sunbird_service
from api.main import model_loader
import json
import re

@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI assistant.
    """
    try:
        # Get service instance
        llm_service = get_llm_service()
        # 1. Handle Conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            # Create new conversation
            conversation_id = str(uuid.uuid4())
            new_conversation = ConversationDB(
                id=conversation_id,
                user_id=current_user.id,
                title=request.message[:30] + "..." # Simple title from first message
            )
            db.add(new_conversation)
            db.commit()
        else:
            # Verify conversation belongs to user
            conversation = db.query(ConversationDB).filter(
                ConversationDB.id == conversation_id,
                ConversationDB.user_id == current_user.id
            ).first()
            if not conversation:
                # If not found or not owned, create new one (or raise error)
                conversation_id = str(uuid.uuid4())
                new_conversation = ConversationDB(
                    id=conversation_id,
                    user_id=current_user.id,
                    title=request.message[:30] + "..."
                )
                db.add(new_conversation)
                db.commit()

        # 2. Save User Message
        user_msg = MessageDB(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        db.add(user_msg)
        db.commit()

        # 3. Construct messages for LLM
        messages = [
            {"role": "system", "content": """You are Mzee Chakula, a helpful nutritional assistant for elderly care in Uganda.

YOUR GOAL: Understand the caregiver's needs quickly and provide ACTIONABLE SOLUTIONS.

WHEN USER ASKS FOR MEAL PLANS:
Generate immediately in this format:

**7-Day Meal Plan for [Name/Condition]**

**Monday:**
- Breakfast: [Meal]
- Lunch: [Meal]
- Dinner: [Meal]

**Tuesday:**
[Continue for all 7 days...]

**Shopping List:**
- [Item 1]
- [Item 2]

**Tips:**
- [Brief tip 1]
- [Brief tip 2]

CONVERSATION RULES:
1. Ask MAX 2-3 questions to understand their needs (name, health conditions, food preferences)
2. Once you have enough info → GENERATE THE MEAL PLAN immediately
3. Don't keep asking questions in circles
4. Be friendly but ACTION-ORIENTED
5. Use local Ugandan foods: matooke, beans, nakati, posho, cassava, sweet potatoes, groundnuts

RECOGNIZE THESE AS "GENERATE NOW" SIGNALS:
- "make a meal plan"
- "create meal plan"
- "generate the plan"
- "can we get the plan"
- After collecting basic info (foods they like, any conditions)

Be warm, brief, and GET THINGS DONE."""}
        ]
        
        # Load history from DB if not provided in request, or trust request?
        # Better to load from DB for consistency, but for now let's use request history + current message
        # Actually, let's use the DB history for context if we want true persistence
        # For simplicity in this step, we'll stick to the request history but append the new message
        
        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})
            
        messages.append({"role": "user", "content": request.message})
        
        # 4. Check if we should generate meal plan based on conversation
        should_generate_plan, extracted_info = _should_generate_meal_plan(messages)

        if should_generate_plan and extracted_info:
            # Generate meal plan using ML models
            meal_plan_service = get_meal_plan_service(model_loader)

            result = meal_plan_service.generate_meal_plan(
                age=extracted_info.get('age', 75),
                health_conditions=extracted_info.get('conditions', []),
                preferred_foods=extracted_info.get('foods', []),
                name=extracted_info.get('name', 'Patient')
            )

            if result['success']:
                # Format meal plan as readable text
                response_content = _format_meal_plan_response(result)
            else:
                # Fallback to LLM
                response_content = await llm_service.generate_response(messages)
        else:
            # 4. Call Groq API via LLM Service (using LangChain)
            response_content = await llm_service.generate_response(messages)

        # 5. Translate response if needed
        final_response = response_content
        if request.language and request.language != 'en':
            try:
                # Map language codes
                lang_code_map = {'lg': 'lug', 'sw': 'swh', 'en': 'eng'}
                target_lang = lang_code_map.get(request.language, request.language)

                translation = await sunbird_service.translate(
                    text=response_content,
                    source_lang='eng',
                    target_lang=target_lang
                )

                # Ensure we get a string result
                translated_text = translation.get('translated_text', response_content)
                if isinstance(translated_text, str):
                    final_response = translated_text
                else:
                    import logging
                    logging.warning(f"Translation returned non-string: {type(translated_text)}")
                    final_response = response_content
            except Exception as e:
                # If translation fails, return original response
                import logging
                logging.warning(f"Translation failed: {str(e)}")
                final_response = response_content

        # 6. Save Assistant Response (save original English for consistency)
        assistant_msg = MessageDB(
            conversation_id=conversation_id,
            role="assistant",
            content=response_content  # Save English version
        )
        db.add(assistant_msg)
        db.commit()

        return ChatResponse(
            response=final_response,  # Return translated version to user
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service error: {str(e)}"
        )


def _should_generate_meal_plan(messages: list) -> tuple[bool, dict]:
    """
    Determine if we should generate a meal plan based on conversation history

    Returns: (should_generate, extracted_info_dict)
    """
    # Join all conversation text
    conversation_text = " ".join([m.get("content", "") for m in messages]).lower()

    # Check for meal plan triggers
    triggers = ["make a meal plan", "create meal plan", "generate plan", "meal plan for", "create a plan"]
    has_trigger = any(trigger in conversation_text for trigger in triggers)

    if not has_trigger:
        return False, {}

    # Extract information from conversation
    extracted = {
        'age': None,
        'conditions': [],
        'foods': [],
        'name': None
    }

    # Extract age
    age_match = re.search(r'(\d+)\s*(years?|yrs?)\s*old', conversation_text)
    if not age_match:
        age_match = re.search(r'age[:\s]*(\d+)', conversation_text)
    if not age_match:
        age_match = re.search(r'he.*?(\d+)', conversation_text)
    if age_match:
        extracted['age'] = int(age_match.group(1))

    # Extract health conditions
    if 'diabetes' in conversation_text or 'diabetic' in conversation_text:
        extracted['conditions'].append('diabetes')
    if 'hypertension' in conversation_text or 'high blood pressure' in conversation_text or 'bp' in conversation_text:
        extracted['conditions'].append('hypertension')
    if 'heart' in conversation_text:
        extracted['conditions'].append('heart condition')

    # Extract preferred foods
    ugandan_foods = ['matooke', 'beans', 'nakati', 'posho', 'cassava', 'sweet potato', 'groundnut', 'fish', 'sukuma']
    for food in ugandan_foods:
        if food in conversation_text:
            extracted['foods'].append(food.replace(' ', '_'))

    # Extract name if mentioned
    name_match = re.search(r'(?:name|called|grandfather|grandpa|granda)(?:\s+is)?\s+([A-Z][a-z]+)', " ".join([m.get("content", "") for m in messages]))
    if name_match:
        extracted['name'] = name_match.group(1)

    # Check if we have minimum info to generate (at least age or conditions)
    has_enough_info = extracted['age'] is not None or len(extracted['conditions']) > 0

    return has_trigger and has_enough_info, extracted


def _format_meal_plan_response(result: dict) -> str:
    """Format meal plan result as readable text"""
    name = result.get('patient_name', 'Patient')
    calories = result.get('caloric_needs', 1800)
    meal_plan = result.get('meal_plan', {})
    shopping_list = result.get('shopping_list', [])
    tips = result.get('tips', [])

    response = f"**7-Day Meal Plan for {name}**\n\n"
    response += f"Daily Caloric Target: ~{calories} kcal\n\n"

    # Add meal plan
    for day, meals in meal_plan.items():
        response += f"**{day}:**\n"
        response += f"- Breakfast: {meals.get('breakfast', 'N/A')}\n"
        response += f"- Lunch: {meals.get('lunch', 'N/A')}\n"
        response += f"- Dinner: {meals.get('dinner', 'N/A')}\n\n"

    # Add shopping list
    response += "**Shopping List:**\n"
    for item in shopping_list:
        response += f"- {item}\n"

    response += "\n**Health Tips:**\n"
    for tip in tips:
        response += f"- {tip}\n"

    response += "\n---\n*Generated using ML models for personalized nutrition*"

    return response
