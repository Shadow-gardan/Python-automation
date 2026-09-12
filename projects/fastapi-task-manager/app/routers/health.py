"""Health endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Check API health", response_description="Service status")
def health_check() -> dict[str, str]:
    """Return a simple service health response."""
    return {"status": "ok"}
