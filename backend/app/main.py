from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from sqlalchemy.orm import Session
from app.schemas import VoterCreate, VoterResponse, DraftResult
from app.services.draft import run_draft
from app.database import SessionLocal, engine, get_db
from app.models import Base, Voter, DraftResult as DBM_DraftResult # DBM_DraftResultとしてインポート

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for voters and draft results
@app.post("/voters", response_model=VoterResponse)
async def create_voter(voter: VoterCreate, db: Session = Depends(get_db)):
    """
    Creates a new voter.

    Args:
        voter (VoterCreate): The voter data.

    Returns:
        VoterResponse: The created voter.

    Raises:
        HTTPException: If the voter email already exists or choices are invalid.
    """
    db_voter = db.query(Voter).filter(Voter.name == voter.name).first()
    if db_voter:
        raise HTTPException(
            status_code=400, detail="この投票者名はすでに登録されています"
        )

    # Validate choices (1-32 and no duplicates per voter)
    choices = [voter.choice1, voter.choice2, voter.choice3]
    if not all(1 <= c <= 32 for c in choices) or len(set(choices)) != 3:
        raise HTTPException(
            status_code=400,
            detail="Invalid choices. Must be unique and between 1 and 32.",
        )

    new_voter = Voter(**voter.dict())
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return VoterResponse(**new_voter.__dict__)


@app.post("/draft/run", response_model=DraftResult)
async def trigger_draft_run(db: Session = Depends(get_db)):
    """
    Triggers the land draft algorithm and stores the results.

    Returns:
        DraftResult: The results of all four rounds.
    """
    voters = db.query(Voter).all()
    if len(voters) < 10:
        raise HTTPException(
            status_code=400, detail="ドラフトを実行するには最低10名の投票者が必要です。"
        )

    voters_list = [v.__dict__ for v in voters]
    results = run_draft(voters_list)

    # Store results in database
    for round_key, round_results in results.items():
        db_draft_result = DBM_DraftResult(
            round_num=int(round_key.replace("round", "")),
            results=[v.to_dict() for v in round_results] # Voterオブジェクトを辞書に変換
        )
        db.merge(db_draft_result) # 既存のレコードがあれば更新、なければ挿入
    db.commit()

    return DraftResult(**results)


@app.get("/draft/{round_num}", response_model=List[VoterResponse])
async def get_draft_results(round_num: int, db: Session = Depends(get_db)):
    """
    Retrieves the stored draft results for a specific round.

    Args:
        round_num (int): The round number (1-4).

    Returns:
        List[VoterResponse]: The list of voters with their assigned lands for the specified round.

    Raises:
        HTTPException: If the round number is invalid or results are not available.
    """
    if not 1 <= round_num <= 4:
        raise HTTPException(
            status_code=400, detail="Invalid round number. Must be between 1 and 4."
        )

    db_draft_result = db.query(DBM_DraftResult).filter(DBM_DraftResult.round_num == round_num).first()
    if not db_draft_result:
        raise HTTPException(
            status_code=404,
            detail=f"Results for round{round_num} not found. Run the draft first.",
        )

    return [VoterResponse(**v) for v in db_draft_result.results]


@app.get("/voters/count", response_model=int)
async def get_voters_count(db: Session = Depends(get_db)):
    """
    Returns the current number of registered voters.
    """
    return db.query(Voter).count()
