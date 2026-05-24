#noi dung cua file mo ta
{
    "name":"Game Management", #ten module
    "version": "1.0",
    "author": "Nguyen Huy and Duy Le", #tac gia
    "description": "This module is used to manage game information for user display, search, and interaction.", #mo ta
    "website": "",
    "category":"General",
    "depends":["base"],#khai bao nhung module lien quan
    "init_xml":[],
    "update_xml":["game_view.xml","game_menu.xml"],
    "demo_xml":["game_demo.xml"],
    "active":False,
    "installable":True,
}
