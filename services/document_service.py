from pathlib import Path

from maxapi.types.input_media import InputMedia


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

    def get_document(self, index: int) -> Path | None:
        documents = self.list_documents()
        if index < 0 or index >= len(documents):
            return None
        return documents[index]

    def format_documents(self) -> str:
        documents = self.list_documents()
        if not documents:
            return (
                "📄 Документы\n\n"
                f"PDF-файлы не найдены в папке `{self.docs_dir}`. "
                "Положите актуальные документы в эту папку, и бот покажет кнопки для скачивания."
            )

        return "📄 Документы\n\nВыберите файл для скачивания:"

    async def send_document(self, bot, chat_id: int, index: int) -> bool:
        document = self.get_document(index)
        if not document:
            return False

        await bot.send_message(
            chat_id=chat_id,
            text=f"📄 {document.name}",
            attachments=[InputMedia(str(document))],
        )
        return True
