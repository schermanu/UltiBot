from samples.helpers import date_manager

lundi = date_manager.long_str_to_date("Lundi 10 janv.")
mardi = date_manager.compact_str_to_date("02/09")
print(lundi)
print(mardi)
