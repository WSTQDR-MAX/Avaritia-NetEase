# -*- coding: utf-8 -*-
from WSTQDRAvaritiaScript.Script_Functions.Functions import *
from WSTQDRAvaritiaScript.QuModLibs.Server import _loaderSystem
CompFactory = serverApi.GetEngineCompFactory()

@AllowCall
def OnNeutroniumCompressorTick(args={}):
    blockPos = args["blockPos"]
    Pos = (blockPos[0] + 0.5, blockPos[1] + 1.0, blockPos[2] + 0.5)
    playerId = args["playerId"]
    dimensionId = compFactory.CreateDimension(playerId).GetEntityDimensionId()
    BlockEntityData = CompFactory.CreateBlockEntityData(levelId).GetBlockEntityData(dimensionId, blockPos)
    if BlockEntityData:
            PlayerUIItem = CompFactory.CreateItem(playerId).GetPlayerUIItem(playerId, 0, False, True)
            if PlayerUIItem:
                if BlockEntityData["input"]:
                    if BlockEntityData["input"].get("newItemName") != PlayerUIItem.get("newItemName"):#与已经分解的方块不同类返回
                        return
                if PlayerUIItem["newItemName"] not in NeutroniumCompressorRecipe:#与配方方块不同类返回
                    return
                #压缩成奇点需要分解的方块数量
                if not BlockEntityData["required_count"]:
                    BlockEntityData["required_count"] = NeutroniumCompressorRecipe[PlayerUIItem["newItemName"]].get("required_count")
                #没有分解则直接赋值
                Item_Input = BlockEntityData["input"]
                if not Item_Input:
                    BlockEntityData["input"] = PlayerUIItem
                    CompFactory.CreateItem(playerId).SetPlayerUIItem(playerId, 0, {}, False, True)
                #分解则累加
                else:
                    Item_Input["count"] += PlayerUIItem["count"]
                    #如果大于最大所需，则取需要的部分，剩下部分先留着
                    if Item_Input["count"] > BlockEntityData["required_count"]:
                        otherCount = Item_Input["count"] - BlockEntityData["required_count"]
                        Item_Input["count"] = BlockEntityData["required_count"]
                        otherItemDict = {"newItemName":BlockEntityData["input"]["newItemName"],"count":otherCount}
                        CompFactory.CreateItem(playerId).SetPlayerUIItem(playerId, 0, otherItemDict, False, True)
                    #如果小于最大所需，直接清空玩家合成容器格子    
                    else:
                        CompFactory.CreateItem(playerId).SetPlayerUIItem(playerId, 0, {}, False, True)
                    BlockEntityData["input"] = Item_Input
                #如果没有输出
                if not BlockEntityData["output"]:
                    BlockEntityData["output"] = NeutroniumCompressorRecipe[PlayerUIItem["newItemName"]].get("output")
                #数量满足输出一个奇点
                if BlockEntityData["input"]["count"] == BlockEntityData["required_count"]:
                    GetContainerItem = CompFactory.CreateItem(levelId).GetContainerItem(blockPos, 0, dimensionId, True)
                    output = NeutroniumCompressorRecipe[PlayerUIItem["newItemName"]].get("output")
                    if  GetContainerItem:
                        if GetContainerItem["newItemName"] != output.get("newItemName"):
                            _loaderSystem.CreateEngineItemEntity(GetContainerItem, dimensionId, Pos)
                            ToAllPlayerPlaySound(dimensionId, blockPos, "random.pop", 0.5, 0.8)
                            CompFactory.CreateItem(levelId).SpawnItemToContainer(output, 0, blockPos, dimensionId)
                        else:
                            if GetContainerItem["count"] < 64:
                                GetContainerItem["count"] += 1
                                CompFactory.CreateItem(levelId).SpawnItemToContainer(GetContainerItem, 0, blockPos, dimensionId)
                            else:
                                _loaderSystem.CreateEngineItemEntity(output, dimensionId, Pos)
                                ToAllPlayerPlaySound(dimensionId, blockPos, "random.pop", 0.5, 0.8)
                    else:   
                        CompFactory.CreateItem(levelId).SpawnItemToContainer(output, 0, blockPos, dimensionId)
                    BlockEntityData["input"] = None
                    BlockEntityData["required_count"] = None
                    BlockEntityData["output"] = None
