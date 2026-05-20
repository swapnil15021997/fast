from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status

from app.core.config import settings
from app.repositories.token import UserAITokenRepository
from app.schemas.token import TokenUsageResponse


class TokenService:
    def __init__(self, repo: UserAITokenRepository) -> None:
        self._repo = repo

    def _current_period(self) -> tuple[str, str]:
        now = datetime.now(timezone.utc)
        period_start = now.strftime("%Y-%m-%d")
        period_end = (now + timedelta(days=settings.rate_limit_period_days)).strftime("%Y-%m-%d")
        return period_start, period_end

    async def get_usage(self, user_id: str) -> TokenUsageResponse:
        period_start, period_end = self._current_period()
        token_record = await self._repo.get_or_create(user_id, period_start, period_end)
        return TokenUsageResponse(
            tokens_used=token_record.tokens_used,
            tokens_limit=token_record.tokens_limit,
            tokens_remaining=max(0, token_record.tokens_limit - token_record.tokens_used),
            period_start=token_record.period_start,
            period_end=token_record.period_end,
        )

    async def check_and_consume(self, user_id: str, amount: int = 1) -> TokenUsageResponse:
        period_start, period_end = self._current_period()
        token_record = await self._repo.get_or_create(user_id, period_start, period_end)
        if token_record.tokens_used + amount > token_record.tokens_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Token quota exhausted for this period.",
            )
        await self._repo.add_tokens(token_record, amount)
        return TokenUsageResponse(
            tokens_used=token_record.tokens_used + amount,
            tokens_limit=token_record.tokens_limit,
            tokens_remaining=max(0, token_record.tokens_limit - (token_record.tokens_used + amount)),
            period_start=token_record.period_start,
            period_end=token_record.period_end,
        )
