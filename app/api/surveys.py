from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_session
from app.models.survey import Survey  # Adjust the import according to your project structure
from app.models.question import Question
from app.schemas.survey import SurveyCreate, SurveyUpdate, SurveyRead  # Define these schemas
from typing import Optional, List

router = APIRouter(prefix="/surveys")

@router.post("/", response_model=SurveyRead)
async def create_survey(survey: SurveyCreate, db: AsyncSession = Depends(get_session)):
    new_survey = Survey(survey_name=survey.survey_name)
    db.add(new_survey)
    await db.commit()
    await db.refresh(new_survey)
    return new_survey

@router.get("/{survey_id}", response_model=SurveyRead)
async def get_survey(survey_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Survey).options(
            selectinload(Survey.questions).options(
                selectinload(Question.game)  # Load the game for each question
            )
        ).where(Survey.survey_id == survey_id)
    )
    survey = result.scalar_one_or_none()
    
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")

    # Convert ORM Survey to Pydantic SurveyRead
    survey_read = SurveyRead.from_orm(survey)
    
    # Pair ORM questions with Pydantic questions to transfer game_name
    for orm_question, read_question in zip(survey.questions, survey_read.questions):
        read_question.survey_name = survey.survey_name  # From parent survey
        read_question.game_name = orm_question.game.gamename  # From ORM-loaded game
    
    return survey_read

@router.get("/", response_model=List[SurveyRead])
async def list_surveys(db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Survey).options(
            selectinload(Survey.questions).options(
                selectinload(Question.game)  # Charger le jeu pour chaque question
            )
        )
    )
    surveys = result.scalars().all()
    
    # Convertir les objets ORM Survey en objets Pydantic SurveyRead
    survey_reads = []
    for survey in surveys:
        survey_read = SurveyRead.from_orm(survey)
        
        # Transférer survey_name aux questions et game_name depuis le jeu associé
        for orm_question, read_question in zip(survey.questions, survey_read.questions):
            read_question.survey_name = survey.survey_name  # Du survey parent
            read_question.game_name = orm_question.game.gamename  # Du jeu chargé via ORM
        
        survey_reads.append(survey_read)
    
    return survey_reads

@router.put("/{survey_id}", response_model=SurveyRead)
async def update_survey(survey_id: int, survey: SurveyUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Survey).options(selectinload(Survey.questions)).where(Survey.survey_id == survey_id)
    )
    db_survey = result.scalar_one_or_none()
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    for key, value in survey.dict(exclude_unset=True).items():
        setattr(db_survey, key, value)
    await db.commit()
    await db.refresh(db_survey)

    # Populate survey_name
    survey_read = SurveyRead.from_orm(db_survey)
    survey_read.survey_name = db_survey.survey_name  # Ensure this field is populated

    return survey_read

@router.delete("/{survey_id}", response_model=SurveyRead)
async def delete_survey(survey_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Survey).options(selectinload(Survey.questions)).where(Survey.survey_id == survey_id)
    )
    db_survey = result.scalar_one_or_none()
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")

    # Populate survey_name
    survey_read = SurveyRead.from_orm(db_survey)
    survey_read.survey_name = db_survey.survey_name  # Ensure this field is populated

    await db.delete(db_survey)
    await db.commit()

    return survey_read