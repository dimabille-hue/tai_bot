from config import PREMISES_FILE
from repository.csv_repository import CsvRepository
from services.premise_service import PremiseService

premise_service = PremiseService(CsvRepository(PREMISES_FILE))
