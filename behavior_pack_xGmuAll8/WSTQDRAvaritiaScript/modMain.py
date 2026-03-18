# -*- coding: utf-8 -*-
from QuModLibs.QuMod import *
WSTQDR_Mod = EasyMod(modDirName="WSTQDRAvaritiaScript")
WSTQDR_SERVER = [
    "Script_Server.AvaritiaServerCommon",
    "Script_Server.AvaritiaHeavenArrow",
    "Script_Server.AvaritiaEndestPearl",
    "Script_Server.AvaritiaNeutronCollector",
    "Script_Server.AvaritiaNeutroniumCompressor",
    "Script_Server.AvaritiaExtremeCraftingTable"
]
WSTQDR_CLIERNT = [
    "Script_Client.AvaritiaClientCommon",
    "Script_Client.AvaritiaNeutronCollector",
    "Script_Client.AvaritiaNeutroniumCompressor",
    "Script_Client.AvaritiaExtremeCraftingTable"
]
for Qu in WSTQDR_SERVER:
    WSTQDR_Mod.Server(Qu)
for Qu in WSTQDR_CLIERNT:
    WSTQDR_Mod.Client(Qu)    

