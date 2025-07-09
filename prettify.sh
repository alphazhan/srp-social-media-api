cd backend && uvx ruff check --fix && uvx ruff format && cd ..
cd ml && uvx ruff check --fix && uvx ruff format && cd ..
cd frontend && pnpm dlx prettier . --write && cd ..