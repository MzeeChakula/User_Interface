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

        # 3. Check user's profile status
        profile = request.profile or {}
        has_profile = bool(profile.get('name') and profile.get('ageRange'))
        
        # Build profile context for the AI
        if has_profile:
            profile_summary = f"""
CURRENT USER PROFILE:
- Elder's Name: {profile.get('name', 'Not set')}
- Age Range: {profile.get('ageRange', 'Not set')}
- Gender: {profile.get('gender', 'Not set')}
- Health Conditions: {', '.join(profile.get('healthConditions', [])) or 'None specified'}
- Medications: {', '.join(profile.get('medications', [])) or 'None specified'}
- Dietary Preferences: {', '.join(profile.get('dietaryPreferences', [])) or 'None specified'}
- Allergies: {', '.join(profile.get('allergies', [])) or 'None specified'}
- Region: {profile.get('region', 'Not set')}

The user has already set up their profile. Start by greeting them and summarizing the profile above.
Then ask: "What would you like to do today? I can help with:
- Generate a personalized meal plan
- Answer nutrition questions
- Suggest local food alternatives
- Update your profile"
"""
        else:
            profile_summary = """
NO PROFILE SET UP YET.

Start by welcoming the user and explain you'd like to learn about the elderly person they're caring for.
Ask ONE question at a time in this order:
1. First, ask for the elderly person's NAME only.
2. Wait for response, then ask about their AGE RANGE (60-70, 70-80, 80+).
3. Wait for response, then ask about any HEALTH CONDITIONS (diabetes, hypertension, heart issues, etc.)
4. Wait for response, then ask about FOOD PREFERENCES (favorite Ugandan foods they enjoy)
5. After collecting info, summarize what you learned and ask if it's correct.

IMPORTANT: Ask ONLY ONE question per message. Be patient and conversational.
"""

        # Construct messages for LLM
        messages = [
            {"role": "system", "content": f"""You are Mzee Chakula, a warm and caring nutritional assistant for elderly care in Uganda.

{profile_summary}

CONVERSATION RULES:
1. Be warm, friendly, and patient - like a caring family member
2. Ask ONE question at a time, never multiple questions in one message
3. Listen to the user's response before moving to the next question
4. Use simple, clear language
5. When ready to generate a meal plan, ask for confirmation first
6. Use local Ugandan foods: matooke, beans, nakati, posho, cassava, sweet potatoes, groundnuts, millet, fish, sukuma wiki

WHEN USER CONFIRMS TO GENERATE MEAL PLAN (says "yes", "please", "go ahead", "ready", "generate"):
Create a 7-day meal plan in this format:

**7-Day Meal Plan for [Name]**
**Daily Caloric Target:** ~[calories] kcal based on age and conditions

**Monday:**
- Breakfast: [Meal]
- Lunch: [Meal]
- Dinner: [Meal]
[Continue for all 7 days...]

**Shopping List:**
[List of items needed]

**Health Tips:**
[3-4 relevant tips based on their conditions]

Be conversational, ask one thing at a time, and make the user feel comfortable!"""}
        ]
        
        # Load history
        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})
            
        messages.append({"role": "user", "content": request.message})
        
        # 4. Search uploaded documents for relevant context
        document_context = ""
        try:
            from api.services.rag_service import get_rag_service
            rag_service = get_rag_service()
            
            # Search for relevant documents
            search_results = await rag_service.search_knowledge_base(request.message, k=3)
            
            if search_results:
                document_context = "\n\n---UPLOADED DOCUMENT CONTEXT---\n"
                document_context += "The user has uploaded documents. Here are relevant excerpts:\n\n"
                for i, result in enumerate(search_results, 1):
                    source = result.get('metadata', {}).get('source', 'Unknown document')
                    content = result.get('content', '')[:500]  # Limit content length
                    document_context += f"[Document: {source}]\n{content}\n\n"
                document_context += "---END DOCUMENT CONTEXT---\n"
                document_context += "\nUse this document information to help answer the user's question. "
                document_context += "If they ask about the document, summarize what you see and explain how it could be used for meal planning.\n"
                
                # Add document context to the last user message
                messages[-1]["content"] = document_context + "\nUser question: " + request.message
        except Exception as e:
            # If RAG search fails, continue without document context
            import logging
            logging.warning(f"RAG search failed: {e}")
        
        # 5. Check if we should generate meal plan based on conversation
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
            # 5. Call Groq API via LLM Service (using LangChain)
            response_content = await llm_service.generate_response(messages)

        # 6. Translate response if needed
        final_response = response_content
        import logging
        logging.info(f"Language requested: '{request.language}' (will translate: {request.language and request.language != 'eng'})")
        
        if request.language and request.language != 'eng':
            try:
                # Map language codes
                lang_code_map = {'lg': 'lug', 'sw': 'swh', 'en': 'eng'}
                target_lang = lang_code_map.get(request.language, request.language)
                logging.info(f"Translating to: {target_lang}")

                translation = await sunbird_service.translate(
                    text=response_content,
                    source_lang='eng',
                    target_lang=target_lang
                )
                logging.info(f"Translation result: {translation}")

                # Ensure we get a string result
                translated_text = translation.get('translated_text', response_content)
                if isinstance(translated_text, str):
                    final_response = translated_text
                    logging.info(f"Using translated response")
                else:
                    logging.warning(f"Translation returned non-string: {type(translated_text)}")
                    final_response = response_content
            except Exception as e:
                # If translation fails, return original response
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
    
    Only triggers when user CONFIRMS they want the plan generated.
    Returns: (should_generate, extracted_info_dict)
    """
    # Get the last user message
    last_user_msg = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user_msg = msg.get("content", "").lower()
            break
    
    # Check for EXPLICIT confirmation in the LAST message only
    confirmation_phrases = [
        "yes", "go ahead", "generate now", "create it", "make it",
        "please do", "yes please", "sure", "ready", "proceed",
        "generate the plan", "create the plan", "make the plan"
    ]
    
    has_confirmation = any(phrase in last_user_msg for phrase in confirmation_phrases)
    
    if not has_confirmation:
        return False, {}
    
    # Join all conversation text for info extraction
    conversation_text = " ".join([m.get("content", "") for m in messages]).lower()

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
        age_match = re.search(r'(\d+)\s*-\s*(\d+)', conversation_text)  # Age range like 70-80
        if age_match:
            extracted['age'] = (int(age_match.group(1)) + int(age_match.group(2))) // 2
    if age_match and extracted['age'] is None:
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
    name_match = re.search(r'(?:name|called|grandfather|grandpa|granny|grandmother)(?:\s+is)?\s+([A-Z][a-z]+)', " ".join([m.get("content", "") for m in messages]))
    if name_match:
        extracted['name'] = name_match.group(1)

    return True, extracted


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
