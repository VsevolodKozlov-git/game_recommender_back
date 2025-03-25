from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_session
from app.models.game import Game
from app.models.user import User
from app.schemas.game import GameInfoResponse  
from app.core.auth import get_current_user
from datetime import datetime
from decimal import Decimal
import csv

router = APIRouter(prefix="/game")

@router.get("/{game_id}", response_model=GameInfoResponse)
async def get_game(
    id_game: int, 
    db: AsyncSession = Depends(get_session),
):
    # Execute async query
    result = await db.execute(
        select(Game).where(Game.id_game == id_game)
    )
    game = result.scalar_one_or_none()

    # Handle not found case
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    # Return only required fields using the response model
    return GameInfoResponse(
        title=game.title,
        header_image=game.header_image,
        short_description=game.short_description
    )



@router.post("/upload-games-csv/")
async def upload_games_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files accepted")

    content = await file.read()
    decoded_content = content.decode("utf-8").splitlines()
    csv_reader = csv.DictReader(decoded_content)

    required_columns = {
        "app_id", "title", "date_release", "win", "mac", "linux",
        "rating", "positive_ratio", "user_reviews", "price_final",
        "header_image", "short_description"
    }
    
    # Validate headers
    if not required_columns.issubset(csv_reader.fieldnames):
        missing = required_columns - set(csv_reader.fieldnames)
        raise HTTPException(400, f"Missing columns: {missing}")

    valid_games = []
    error_rows = []
    
    for row_idx, row in enumerate(csv_reader, start=2):
        try:
            # Skip empty rows
            if not any(row.values()): continue

            # Validate app_id is numeric
            if not row["app_id"].strip().isdigit():
                raise ValueError(f"Invalid app_id: {row['app_id']}")

            # Validate required fields
            required_fields = ["title", "header_image", "date_release"]
            for field in required_fields:
                if not row.get(field):
                    raise ValueError(f"Missing {field}")

            game_data = Game(
                id_game=int(row["app_id"]),
                title=row["title"].strip(),
                header_image=row["header_image"].strip(),
                date_release=datetime.strptime(row["date_release"], "%Y-%m-%d").date(),
                win=row["win"].strip().lower() == "true",
                mac=row["mac"].strip().lower() == "true",
                linux=row["linux"].strip().lower() == "true",
                rating=row["rating"].strip(),
                positive_ratio=int(row["positive_ratio"]),
                user_reviews=int(row["user_reviews"]),
                price_final=Decimal(row["price_final"]),
                short_description=row["short_description"].strip()
            )
            valid_games.append(game_data)
            
        except Exception as e:
            error_rows.append({
                "row": row_idx,
                "error": str(e),
                "app_id": row.get("app_id"),
                "title": row.get("title")
            })
            continue

    # Insert valid records
    if valid_games:
        try:
            db.add_all(valid_games)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(500, f"Database error: {str(e)}")

    return {
        "message": f"Inserted {len(valid_games)} games",
        "errors": error_rows,
        "error_count": len(error_rows)
    }