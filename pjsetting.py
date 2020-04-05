from typing import Dict
MyCode: str = """anyword"""+  # please change the value of left and delete the "+"
pageNames: Dict[str, str] = {
    "index": "index.html",
    "search": "search.html",
    "update": "update_page.html",
    "Restore": "Restore.html",
}
routerUrls: Dict[str, str] = {
    'index': '/page/index/',
    'index_zh': '/page/index/?language=zh',
    'search': '/page/search/',
    'search_zh': '/page/search/?language=zh',
    'update': '/page/update/',
    'update_zh': '/page/update/?language=zh',
    "Restore": "/page/Restore/",
    "Restore_zh": "/page/Restore/?language=zh",
    "getAccount": "/getAccount/",
    "getPW": "/getPW/",
    "Save_Result_to_sql": "/Save_Result_to_sql/",
    "Search_item": "/Search_item",
    "Update_Text": "/Update_Text",
    "Delete_Item": "/Delete_Item",
    "Login": "/Login/",
}
