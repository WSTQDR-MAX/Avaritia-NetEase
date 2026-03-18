# -*- coding: utf-8 -*-
from WSTQDRAvaritiaScript.Script_Functions.Functions import *
from WSTQDRAvaritiaScript.QuModLibs.Server import _loaderSystem
CompFactory = serverApi.GetEngineCompFactory()

@Listen("ServerBlockEntityTickEvent")
def OnNeutronCollectorTick(args={}):
    blockName = args["blockName"]
    dimensionId = args["dimension"]
    blockPos = (args["posX"], args["posY"], args["posZ"])
    Pos = (args["posX"] + 0.5, args["posY"] + 1.0, args["posZ"] + 0.5)
    if blockName != "avaritia:neutron_collector":
        return
    BlockEntityData = CompFactory.CreateBlockEntityData(levelId).GetBlockEntityData(dimensionId, blockPos)
    if not BlockEntityData:
        return
    if not BlockEntityData["progress"]:
        BlockEntityData["progress"] = 1
    if BlockEntityData["progress"]:
        if BlockEntityData["progress"] < 7111:
            BlockEntityData["progress"] += 1
        else:
            BlockEntityData["progress"] = 0
            GetContainerItem = CompFactory.CreateItem(levelId).GetContainerItem(blockPos, 0, dimensionId, True)
            if GetContainerItem:
                if GetContainerItem["newItemName"] != "avaritia:neutron_pile":
                    _loaderSystem.CreateEngineItemEntity(GetContainerItem, dimensionId, Pos)
                    ToAllPlayerPlaySound(dimensionId, blockPos, "random.pop", 0.5, 0.8)
                    CompFactory.CreateItem(levelId).SpawnItemToContainer({"newItemName":"avaritia:neutron_pile","count":1}, 0, blockPos, dimensionId)
                else:
                    if GetContainerItem["count"] < 64:
                        GetContainerItem["count"] += 1
                        CompFactory.CreateItem(levelId).SpawnItemToContainer(GetContainerItem, 0, blockPos, dimensionId)
                    else:
                        _loaderSystem.CreateEngineItemEntity({"newItemName":"avaritia:neutron_pile","count":1}, dimensionId, Pos)
                        ToAllPlayerPlaySound(dimensionId, blockPos, "random.pop", 0.5, 0.8)
            else:   
                CompFactory.CreateItem(levelId).SpawnItemToContainer({"newItemName":"avaritia:neutron_pile","count":1}, 0, blockPos, dimensionId)
            