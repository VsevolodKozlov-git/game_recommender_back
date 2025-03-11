from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_session
from app.models.question import Question  # Adjust the import according to your project structure
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionRead  # Define these schemas
from typing import Optional, List
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/questions")

@router.post("/", response_model=QuestionRead)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_session)):
    # Créer la nouvelle question
    new_question = Question(survey_id=question.survey_id, game_id=question.game_id)
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    
    # Charger explicitement les relations dont nous avons besoin
    result = await db.execute(
        select(Question)
        .where(Question.question_id == new_question.question_id)
        .options(
            joinedload(Question.survey),
            joinedload(Question.game)
        )
    )
    loaded_question = result.scalars().first()
    
    # Créer l'objet de réponse avec les données chargées
    question_read = QuestionRead.from_orm(loaded_question)
    question_read.survey_name = loaded_question.survey.survey_name
    question_read.game_name = loaded_question.game.gamename
    
    return question_read

@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Question).options(
            selectinload(Question.survey),
            selectinload(Question.game)
        ).where(Question.question_id == question_id)
    )
    question = result.scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Populate survey_name and game_name
    question_read = QuestionRead.from_orm(question)
    question_read.survey_name = question.survey.survey_name
    question_read.game_name = question.game.gamename

    return question_read

@router.get("/", response_model=List[QuestionRead])
async def list_questions(db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Question).options(
            selectinload(Question.survey),
            selectinload(Question.game)
        )
    )
    questions = result.scalars().all()

    # Populate survey_name and game_name for each question
    question_reads = []
    for question in questions:
        question_read = QuestionRead.from_orm(question)
        question_read.survey_name = question.survey.survey_name
        question_read.game_name = question.game.gamename
        question_reads.append(question_read)

    return question_reads

@router.put("/{question_id}", response_model=QuestionRead)
async def update_question(question_id: int, question: QuestionUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Question).options(
            selectinload(Question.survey),
            selectinload(Question.game)
        ).where(Question.question_id == question_id)
    )
    db_question = result.scalar_one_or_none()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    # Update logic can be added here if needed
    await db.commit()
    await db.refresh(db_question)

    # Populate survey_name and game_name
    question_read = QuestionRead.from_orm(db_question)
    question_read.survey_name = db_question.survey.survey_name
    question_read.game_name = db_question.game.gamename

    return question_read

@router.delete("/{question_id}", response_model=QuestionRead)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Question).options(
            selectinload(Question.survey),
            selectinload(Question.game)
        ).where(Question.question_id == question_id)
    )
    db_question = result.scalar_one_or_none()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Populate survey_name and game_name
    question_read = QuestionRead.from_orm(db_question)
    question_read.survey_name = db_question.survey.survey_name
    question_read.game_name = db_question.game.gamename

    await db.delete(db_question)
    await db.commit()

    return question_read