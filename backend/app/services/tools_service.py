from app.schemas.assistant_schema import ToolRequest, ToolResponse


class ToolsService:
    async def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            status="planned",
            message=(
                "Camada de tools reservada. Nesta etapa nenhuma acao externa e executada."
            ),
            result={
                "tool_name": request.tool_name,
                "dry_run": request.dry_run,
            },
        )
