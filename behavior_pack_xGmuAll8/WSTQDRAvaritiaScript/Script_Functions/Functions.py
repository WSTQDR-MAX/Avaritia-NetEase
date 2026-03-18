# -*- coding: utf-8 -*-
import math
import copy
import random
from WSTQDRAvaritiaScript.QuModLibs.Server import *
import mod.server.extraServerApi as ServerApi
from WSTQDRAvaritiaScript.QuModLibs.Server import _loaderSystem
from WSTQDRAvaritiaScript.Script_Config.modConfig import *
levelId = ServerApi.GetLevelId()
CompFactory = ServerApi.GetEngineCompFactory()         

#概率判断
def ProbabilityFunc(Probability):
    '''概率返回布尔值'''
    randomList = []
    for i in range(Probability):
        randomList.append(1)
    for x in range(100 - Probability):
        randomList.append(0)
    extract = random.choice(randomList)
    if extract == 1:
        return True
    else:
        return False

#方块下面坐标    
def IsBelow(pos, neighPos):
        '''
        返回是否为方块下面坐标,布尔值.
        '''
        return pos[0] == neighPos[0] and (pos[1] - 1 == neighPos[1]) and pos[2] == neighPos[2]

def ToAllPlayerPlayParticle(dmId, pos, ParticleName):
    '''
    向所有玩家在世界维度某坐标播放原版或自定义粒子
    '''
    playerList = serverApi.GetPlayerList()
    for playerId in playerList:
        dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
        if dimensionId == dmId:
            data = {"ParticleName":ParticleName, "pos":pos}
            Call(playerId,"PlayParticle", data)
            
def ToAllPlayerPlaySound(dmId, pos, soundName, volume = 1, pitch = 1): 
    '''
    向所有玩家在世界维度某坐标播放原版或自定义音效
    '''
    playerList = serverApi.GetPlayerList()
    for playerId in playerList:
        dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
        if dimensionId == dmId:
            data = {"soundName": soundName, "pos": pos, "volume":volume, "pitch":pitch}
            Call(playerId,"OnPlaySound", data)  

def ResetPlayerUsedCD(playerId):
    # 重置CD
    CompFactory.CreateModAttr(playerId).SetAttr("WSTQDRPlayerUsedCD", False)
    
def SetPlayerUsedCD(playerId, PlayerUsedCD = 0.2):
    # 设置CD
    cd = CompFactory.CreateModAttr(playerId).GetAttr("WSTQDRPlayerUsedCD")
    if cd is False:
        CompFactory.CreateModAttr(playerId).SetAttr("WSTQDRPlayerUsedCD", True)
        CompFactory.CreateGame(levelId).AddTimer(PlayerUsedCD, ResetPlayerUsedCD, playerId)
        Call(playerId,"PlaySwing")
        return False
    else:
        Call(playerId,"PlaySwing")
        return True
                           
#模拟原版MC物品的使用减少                
def SpawnLessItemsToPlayer(itemDict,playerId):
        '''
        模拟原版MC物品的使用减少;
        itemDict是要减少的自定义的物品字典;
        playerId是玩家的ID.
        '''
        gameType = CompFactory.CreateGame(playerId).GetPlayerGameType(playerId)
        if gameType != 1:
            itemDict["count"] -= 1
            CompFactory.CreateItem(playerId).SetEntityItem(2, itemDict, 0)

#模拟原版生成到背包，背包满了就生成一个物品掉落物
def SpawnItemToPlayer(itemDict,playerId):
    '''
        模拟原版生成到背包，背包满了就生成一个物品掉落物;
        itemDict是要生成的自定义的物品字典;
        playerId是玩家的ID.
        '''
    Pos = CompFactory.CreatePos(playerId).GetPos()
    dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    SpawnItem = CompFactory.CreateItem(playerId).SpawnItemToPlayerInv(itemDict,playerId)
    if not SpawnItem:
        _loaderSystem.CreateEngineItemEntity(itemDict,dimensionId,Pos)