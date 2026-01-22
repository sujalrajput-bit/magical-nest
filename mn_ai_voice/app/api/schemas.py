"""API request/response schemas for the application."""

from pydantic import BaseModel


class UserTurnRequest(BaseModel):
    """Request schema for user turn API endpoint."""

    text: str