from API_CRUD import API_CRUD
from LMSclient_main import menu_provider
import repository

repository.libraryTablesCreate()
repository.initial_data()

menu_provider()

