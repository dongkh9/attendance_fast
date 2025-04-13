from sqlalchemy import create_engine
from models import Base

# SQLite 예시
DATABASE_URL = "sqlite:///./attendance.db"
engine = create_engine(DATABASE_URL, echo=True)

# ⚠️ 전체 테이블 삭제 후 재생성 (테스트 환경만!)
def reset_database():
    print("🚨 전체 테이블 삭제 중...")
    Base.metadata.drop_all(bind=engine)

    print("🛠️ 테이블 재생성 중...")
    Base.metadata.create_all(bind=engine)

    print("✅ DB 초기화 완료")

if __name__ == "__main__":
    reset_database()
