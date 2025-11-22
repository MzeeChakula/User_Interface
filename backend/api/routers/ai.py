from fastapi import APIRouter, HTTPException, status, UploadFile, File
from api.models.ai import (
    TranslateRequest, TranslateResponse,
    LanguageDetectRequest, LanguageDetectResponse,
    RAGQuery, RAGResponse
)
from api.services.sunbird import sunbird_service
from api.services.rag_service import get_rag_service
import PyPDF2
from io import BytesIO
import docx

router = APIRouter(
    prefix="/ai",
    tags=["AI Services"],
    responses={404: {"description": "Not found"}},
)

@router.post("/detect-language", response_model=LanguageDetectResponse)
async def detect_language(request: LanguageDetectRequest):
    """
    Detect the language of the given text using Sunbird AI.
    Supports all Ugandan languages (Luganda, Runyankole, Acholi, Ateso, Lugbara).
    """
    try:
        result = await sunbird_service.detect_language(request.text)
        
        return LanguageDetectResponse(
            language=result["language"],
            language_name=result["language_name"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Language detection failed: {str(e)}"
        )

@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported Ugandan languages.
    """
    try:
        languages = await sunbird_service.get_supported_languages()
        return {"languages": languages}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch languages: {str(e)}"
        )

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text using Sunbird AI.
    Supports all Ugandan languages: Luganda, Runyankole, Acholi, Ateso, Lugbara.
    Auto-detects source language if not provided.
    """
    try:
        result = await sunbird_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return TranslateResponse(
            translated_text=result["translated_text"],
            source_language=result["source_language"],
            target_language=result["target_language"],
            source_language_name=result.get("source_language_name"),
            target_language_name=result.get("target_language_name")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )

@router.post("/rag", response_model=RAGResponse)
async def rag_query(query: RAGQuery):
    """
    Answer a query using RAG with ChromaDB and Tavily search.
    """
    try:
        # Get service instance
        rag_service = get_rag_service()

        result = await rag_service.answer_query(
            query=query.query,
            chat_history=query.chat_history,
            use_search=query.use_search
        )

        return RAGResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG query failed: {str(e)}"
        )

@router.post("/rag/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, DOCX, TXT) for RAG processing.
    The document will be processed and added to the knowledge base.
    """
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
        file_ext = '.' + file.filename.split('.')[-1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not supported. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Read file content
        content = await file.read()

        # Extract text based on file type
        text_content = ""

        if file_ext == '.pdf':
            # Extract text from PDF
            pdf_file = BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"

        elif file_ext in ['.docx', '.doc']:
            # Extract text from DOCX
            doc_file = BytesIO(content)
            doc = docx.Document(doc_file)
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"

        elif file_ext == '.txt':
            # Read text file
            text_content = content.decode('utf-8')

        if not text_content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text content found in the document"
            )

        # Get RAG service and add document to vector store
        rag_service = get_rag_service()

        # Split text into chunks (simple chunking by paragraphs)
        chunks = [chunk.strip() for chunk in text_content.split('\n\n') if chunk.strip()]

        # Create metadata for each chunk
        metadata = [{"source": file.filename, "chunk_index": i} for i in range(len(chunks))]

        # Add to vector store (synchronous operation)
        rag_service.add_documents(texts=chunks, metadatas=metadata)

        return {
            "message": "Document uploaded and processed successfully",
            "filename": file.filename,
            "chunks_added": len(chunks),
            "text_length": len(text_content)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

