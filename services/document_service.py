from pathlib import Path


class DocumentService:
    def __init__(self, docs_dir: str | Path):
        self.docs_dir = Path(docs_dir)

    def list_documents(self) -> list[Path]:
        if not self.docs_dir.exists():
            return []
        return sorted(
            path
            for path in self.docs_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".pdf"
        )

    def format_documents(self) -> str:
        documents = self.list_documents()
        if not documents:
            return (
                "📄 Документы\n\n"
                f"PDF-файлы не найдены в папке `{self.docs_dir}`. "
                "Положите актуальные документы в эту папку, и бот покажет их в списке."
            )

        lines = ["📄 Документы", "", "Доступные PDF-файлы:"]
        lines.extend(f"{index}. {document.name}" for index, document in enumerate(documents, start=1))
        return "\n".join(lines)
