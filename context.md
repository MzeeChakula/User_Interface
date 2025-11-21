# **Mzee Chakula: Full System Architecture Summary**

Mzee Chakula is a comprehensive, AI-powered nutritional assistant designed as a Progressive Web App (PWA) to provide conversational, culturally relevant, and medically sound meal planning advice for elderly care in Uganda. The system is architected with a clean separation between the user-facing frontend and the powerful, multi-tool backend.

---

## **Part 1: The Frontend - Vue/Vite PWA**

The frontend is a lightweight, installable, and offline-capable Progressive Web App built with **Vite** and **Vue.js**. Its primary focus is on providing a simple, intuitive, and memorable user experience, especially for users with varying levels of digital literacy.

### **Key Technologies:**

* **Framework:** Vue.js 3 (Composition API)
* **Build Tool:** Vite
* **PWA Functionality:** `vite-plugin-pwa` for service workers, offline caching, and home screen installation.
* **State Management:** Pinia (the official state management library for Vue).
* **HTTP Client:** Axios for communicating with the backend API.

#### **User Interface (UI) Screens & Functionality (5-Screen Flow):**

#### **0. App Loader & Splash Screen**

* **Objective:** To provide an engaging visual experience while the app's initial resources are loading, and to handle slow network conditions gracefully. This replaces a generic, static loading spinner.
* **UI & Animation:**
  * **Page Loader:** When the app first loads or is fetching significant data, instead of a simple spinner, the screen displays a subtle, clean animation of the app's core icons. For example, the icons for **Food (🍽️), Health (🏥), and Community (👥)** could gently fade in and out or pulse softly in sequence. This animation is smooth and lightweight, designed to reduce user frustration during wait times.
  * **Color Palette:** The animation uses the app's soothing and professional theme colors.

* **Functionality:**
  * This loader is shown instantly when the PWA is launched, providing immediate visual feedback.
  * It serves as the default loading state for any major navigation or data-fetching operation within the app.

#### **1. Introductory Brand Animation Screen (First-Time Use Only)**

* **Objective:** To create a memorable, polished, and creative first impression that introduces the user to the Mzee Chakula brand, replacing a standard static welcome screen.
* **UI & Animation:**
  * Upon first launch (after the initial page loader), the user is greeted with a short, beautiful horizontal animation.
  * **The Animation Flow:**
        1. A series of soft, horizontal bars or waves of your theme colors (e.g., warm yellow, calming blue, earthy green) gracefully slide across the screen from left to right.
        2. As the colored waves settle, they elegantly reveal the app name, **"Mzee Chakula,"** which animates into place with a creative effect (e.g., letters fading in, writing on-screen, or assembling from small particles).
        3. The app's tagline, such as "Nourishing our Elders, Together," fades in subtly below the name.
  * **Duration:** The entire animation is brief, lasting no more than 3-4 seconds to avoid delaying the user.
  * **Action:** After the animation completes, the app automatically transitions to the **Welcome & Onboarding Screen** with the interactive tutorial.

* **Functionality:**
  * This screen runs only once, on the very first time a user opens the app after installation.
  * It's designed to build an immediate positive emotional connection and establish the app as a high-quality, professional tool.

---

### **Updated User Flow (First Time Experience):**

1. **Launch App:** User taps the Mzee Chakula icon on their home screen.
2. **Page Loader (1-2 seconds):** The animated icons appear instantly, reassuring the user that the app is loading.
3. **Brand Animation (3-4 seconds):** The horizontal color wave animation plays, creatively revealing the "Mzee Chakula" name.
4. **Welcome & Tutorial Screen:** The app transitions to the interactive onboarding guide.
5. **Authentication Screen:** User signs up or logs in.
6. **Main App:** User lands on the Chat Interface, ready to start their first conversation.

**Subsequent Launches:** The flow will be much faster, skipping steps 3 and 4:

1. **Launch App:** User taps the icon.
2. **Page Loader (1-2 seconds):** The animated icons appear.
3. **Main App:** User is taken directly to the Chat Interface, already logged in.

## next flow as planned

1. **Welcome & Onboarding Screen:**
    * **Purpose:** To provide a warm introduction to new users and guide them through a one-time interactive tutorial.
    * **Functionality:**
        * Displays a clean, welcoming message and the Mzee Chakula logo.
        * Initiates a simple, skippable tutorial that swipes through 3-4 cards explaining the app's core functions (e.g., "Chat to get a plan," "View your history," "Update your profile").
        * A prominent "Get Started" button leads to the authentication screen.

2. **Authentication Screen:**
    * **Purpose:** To provide simple, secure access for users.
    * **Functionality:**
        * Offers easy sign-up/login options, prioritizing methods common in the region (e.g., "Sign in with Google," "Sign in with Phone Number").
        * Keeps the user logged in for a seamless experience on subsequent visits.

3. **Chat Interface Screen (The "ChatGPT-like" Core):**
    * **Purpose:** This is the main interactive screen where users have a conversation with the nutritional assistant.
    * **Functionality:**
        * **Chat History Panel:** A persistent, scrollable sidebar (on wider screens) or a slide-out menu (on mobile) lists previous conversations, titled by date or topic (e.g., "Hypertension Plan - Oct 28"). This allows users to easily recall past advice.
        * **Main Chat Window:** The primary view where the conversation takes place. User prompts and AI responses appear in a familiar message-bubble format.
        * **Input Box:** A simple text input field at the bottom with a "Send" button. It will include a microphone icon for future voice-to-text input.
        * **Example Prompts:** Above the input box, clickable prompt suggestions guide the user (e.g., "Create a weekly plan for diabetes," "What foods are affordable this week?").

4. **Profile Screen:**
    * **Purpose:** To manage the user's and the elder's core information, which provides context for all AI-generated recommendations.
    * **Functionality:**
        * Allows the user to input and edit key details using simple forms and selectors:
            * Elder's Age Range.
            * Known Health Conditions (multi-select list).
            * Current Medications.
            * Dietary Preferences or Allergies.
            * Geographic Region within Uganda (for food availability).
        * This data is saved and automatically sent with every request to the backend, so the user doesn't have to repeat themselves.

5. **Settings Screen:**
    * **Purpose:** To manage app preferences and user account settings.
    * **Functionality:**
        * **Language Preference:** A dropdown to select the app's display language (English, Luganda, etc.).
        * **Notifications:** Toggles for receiving reminders or tips.
        * **Account:** "Log Out," "Delete Account" options.
        * **Help & Feedback:** A link to a simple FAQ or a form to send feedback.

---

## **Part 2: The Backend - AI Agent & API Services**

The backend is an intelligent, multi-tool AI agent served via a **FastAPI** application. It is deployed as a **Docker container** to a scalable cloud platform (e.g., Google Cloud Run). This backend is the "brain" of the operation, orchestrating multiple specialized services to construct a single, comprehensive response.

## **Key Technologies 2:**

* **API Framework:** FastAPI
* **Containerization:** Docker
* **Deployment:** Google Cloud Run (or similar serverless container platform).
* **Database:** Neo4j (hosted on AuraDB or a separate virtual machine).

### **Backend Services & Their Roles in the "Chain of Thought":**

1. **Conversational Orchestrator (Groq API):**
    * **Role:** The central nervous system. It receives the user's raw query from the frontend.
    * **Function:** Its high-speed Large Language Model (LLM) analyzes the user's intent, breaks down the query into sub-tasks, and decides which of the other specialized tools to call in what order.

2. **Multilingual Translator (Sunbird AI - Sunflower API):**
    * **Role:** The communication expert.
    * **Function:** Called by the Groq orchestrator at the beginning and end of the process. It translates the user's native language query into English for the system to process and translates the final English answer back into the user's native language.

3. **Core Nutritional Reasoner (Your Trained Models & Knowledge Graph):**
    * **Role:** The domain expert and safety-checker.
    * **Function:** The orchestrator sends a structured query (e.g., `{"condition": "Hypertension"}`) to this service. Your API connects to the **Neo4j graph** and uses your **GNN model** to identify safe, effective, and culturally relevant foods. This provides the factual, evidence-based core of the nutritional recommendation.

4. **Real-Time Information Retriever (LangChain RAG):**
    * **Role:** The field researcher.
    * **Function:** If the user asks about up-to-date information (e.g., market prices, new health guidelines), the orchestrator calls this service. LangChain RAG queries its vector database or external APIs to find and retrieve the most current, relevant text snippets.

5. **Final Response Synthesizer (Groq API):**
    * **Role:** The final author.
    * **Function:** After gathering the structured recommendations from your system and the real-time context from RAG, the Groq orchestrator synthesizes all these pieces of information into a single, coherent, natural-language response.

This complete architecture ensures your Mzee Chakula app is not only intelligent and accurate but also user-friendly, accessible, and highly practical for its intended audience.


  📊 Existing Backend Analysis Summary

  ✅ What You Already Have (40% of Backend)

  Your existing backend is a solid FastAPI foundation with:

  1. Working ML Model System
    - Predicts daily caloric needs for elderly
    - 3 models: HuggingFace XGBoost (R²=0.6710), Local XGBoost, HistGradient
    - Auto model selection with offline fallback
    - Model from: Shakiran/MzeeChakula_Model
  2. Production-Ready Infrastructure
    - ✓ FastAPI with proper structure
    - ✓ Docker multi-stage build
    - ✓ Docker Compose orchestration
    - ✓ CORS middleware
    - ✓ Health checks & monitoring
    - ✓ Comprehensive logging
  3. API Endpoints
    - /health - Health check
    - /health/models - Model status
    - /predict - Single prediction
    - /predict/batch - Batch predictions
    - /health/encoding - Feature mappings
  4. Data Models
    - Region, Condition, AgeGroup, Season enums
    - Nutrition input/output schemas
    - All aligned with Uganda context

  🔄 What We Can Reuse

  Directly Reusable:
  - ✓ Docker infrastructure (Dockerfile, docker-compose)
  - ✓ ModelLoader pattern
  - ✓ Health check system
  - ✓ FastAPI app structure
  - ✓ Logging & monitoring setup
  - ✓ Region/Condition/Age enums

  Reusable with Modifications:
  - Pydantic schemas (extend for chat, auth, profile)
  - Requirements.txt (add LangChain, Neo4j, Groq, JWT libs)
  - Router pattern (add auth, chat, profile routers)

  ❌ What We Need to Build (60% of Backend)

  Phase 1 - Authentication (20%)
  - JWT token system
  - User registration/login
  - Password hashing
  - Session management

  Phase 2 - Chat System (30%)
  - Conversation management
  - Message storage
  - WebSocket for real-time
  - Groq API orchestration

  Phase 3 - AI Integration (25%)
  - Groq API (LLM orchestrator)
  - Sunbird AI (translation)
  - Neo4j (knowledge graph)
  - LangChain RAG (documents)

  Phase 4 - Additional Features (15%)
  - Profile management
  - Document upload/processing
  - Feedback system
  - Settings API

  Phase 5 - Testing & Deploy (10%)
  - Unit tests
  - Integration tests
  - Cloud deployment
  - CI/CD pipeline

  📈 Project Status Update

  Frontend:        95% Complete ✅
  Backend Foundation: 40% Complete ⚙️
  Full Backend:     0% Complete (needs new components)
  Overall Project:  55% Complete

  🛠️ Recommended Next Steps

  1. Set up databases:
    - PostgreSQL (user data, conversations)
    - Neo4j AuraDB (knowledge graph)
    - Vector DB (Chroma/Pinecone for RAG)
  2. Get API keys:
    - Groq API
    - Sunbird AI
    - Hugging Face token
  3. Start with Authentication:
    - Implement JWT system
    - Connect frontend to backend auth
    - Test registration/login flow
  4. Then Chat System:
    - Basic Groq integration
    - Conversation storage
    - Simple chat flow

  Estimated Timeline: 10 weeks (2.5 months) to complete full backend
