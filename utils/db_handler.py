from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class VideoSummary(Base):
    __tablename__ = 'video_summaries'
    
    id = Column(Integer, primary_key=True)
    video_id = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    language = Column(String(2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_urls = Column(Text, nullable=False)

class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine(os.environ['DATABASE_URL'])
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_summary(self, video_id: str, title: str, summary: str, language: str, source_urls: str):
        """Save a video summary to the database."""
        try:
            summary_entry = VideoSummary(
                video_id=video_id,
                title=title,
                summary=summary,
                language=language,
                source_urls=source_urls
            )
            self.session.add(summary_entry)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    def get_recent_summaries(self, limit: int = 5):
        """Get recent summaries from the database."""
        try:
            return (
                self.session.query(VideoSummary)
                .order_by(VideoSummary.timestamp.desc())
                .limit(limit)
                .all()
            )
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_summaries_by_language(self, language: str, limit: int = 5):
        """Get summaries filtered by language."""
        try:
            return (
                self.session.query(VideoSummary)
                .filter(VideoSummary.language == language)
                .order_by(VideoSummary.timestamp.desc())
                .limit(limit)
                .all()
            )
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
