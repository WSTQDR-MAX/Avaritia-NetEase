# -*- coding: utf-8 -*-
import math
import random
from WSTQDRAvaritiaScript.Script_Functions.Functions import *
from WSTQDRAvaritiaScript.QuModLibs.Server import _loaderSystem
CompFactory = serverApi.GetEngineCompFactory()

def getVoidScale(grouth_age):
    """
    根据年龄返回虚空比例，在黑洞成长周期内从0线性增长到1。
    """
    return grouth_age / 176.0

serverApi.AddEntityTickEventWhiteList('avaritia:black_hole')
@Listen("EntityTickServerEvent")
def OnBlackHoleTick(args={}):
    entityId = args["entityId"]
    identifier = args["identifier"]
    # 如果不是黑洞则直接返回
    if identifier != 'avaritia:black_hole':
        return
    # 确保黑洞向量为0
    BlackHoleMotion = CompFactory.CreateActorMotion(entityId).GetMotion()
    if BlackHoleMotion:
        if BlackHoleMotion[0] != 0 or BlackHoleMotion[1] != 0 or BlackHoleMotion[0] != 0:
            CompFactory.CreateActorMotion(entityId).SetMotion((0, 0, 0))
    srcId = CompFactory.CreateExtraData(entityId).GetExtraData("srcId")
    Pos = CompFactory.CreateExtraData(entityId).GetExtraData("blockPos")
    x, y, z = Pos
    dimensionId = CompFactory.CreateDimension(entityId).GetEntityDimensionId()
    despawnTime = CompFactory.CreateExtraData(entityId).GetExtraData("despawnTime")
    if despawnTime is None:
        CompFactory.CreateExtraData(entityId).SetExtraData("despawnTime", 186)
    elif despawnTime is not None and despawnTime > 0:
        CompFactory.CreateExtraData(entityId).SetExtraData("despawnTime", despawnTime - 1)
        age = 186 - despawnTime
        grouth_age = 176 - despawnTime
        if age < 10:
            grouth_age = age
        voidScale = getVoidScale(grouth_age)
        radius = 1 + voidScale * 4
        suckrange = 20.0
        startPos = (x - suckrange, y - suckrange, z - suckrange)
        endPos = (x + suckrange, y + suckrange, z + suckrange)
        entityList = CompFactory.CreateGame(levelId).GetEntitiesInSquareArea(None, startPos, endPos, dimensionId)
        if entityList:
            for Id in entityList:
                Id_identifier = CompFactory.CreateEngineType(Id).GetEngineTypeStr()
                if Id == entityId or Id_identifier == identifier:
                    continue  # 跳过黑洞自身
                suckeePos = CompFactory.CreatePos(Id).GetPos()
                dx = x - suckeePos[0]
                dy = y - suckeePos[1]
                dz = z - suckeePos[2]
                len_val = math.sqrt(dx**2 + dy**2 + dz**2)
                if len_val <= suckrange and len_val > 0:
                    lenn = len_val / suckrange
                    strength = (1 - lenn)**2
                    power = 0.75 * radius
                    currentMotion = CompFactory.CreateActorMotion(Id).GetMotion()
                    newMotionX = currentMotion[0] + (dx / len_val) * strength * power
                    newMotionY = currentMotion[1] + (dy / len_val) * strength * power
                    newMotionZ = currentMotion[2] + (dz / len_val) * strength * power
                    NewMotion = (newMotionX, newMotionY, newMotionZ)
                    if len_val < 2: # 实体位于黑洞中心，向量骤降
                        NewMotion = (newMotionX / 10, newMotionY / 10, newMotionZ / 10)
                        if len_val < 1.0:
                            NewMotion = (newMotionX / 10**2, newMotionY / 10**2, newMotionZ / 10**2)
                        elif len_val < 0.5:
                            NewMotion = (newMotionX / 10**3, newMotionY / 10**3, newMotionZ / 10**3)
                        elif len_val < 0.25:
                            NewMotion = (newMotionX / 10**4, newMotionY / 10**4, newMotionZ / 10**4)
                    entityIdentifier = CompFactory.CreateEngineType(Id).GetEngineTypeStr()
                    if entityIdentifier != "minecraft:player":
                        CompFactory.CreateActorMotion(Id).SetMotion(NewMotion)
                    else:
                        GameType = CompFactory.CreateGame(Id).GetPlayerGameType(Id)
                        if GameType != 1:
                            CompFactory.CreateActorMotion(Id).SetPlayerMotion(NewMotion)

        # 执行方块破坏
        if grouth_age % 10 == 0 and grouth_age < 150:
            nomrange = radius * 1.5
            blockrange = int(math.ceil(nomrange))
            for bx in range(-blockrange, blockrange + 1):
                for by in range(-blockrange, blockrange + 1):
                    for bz in range(-blockrange, blockrange + 1):
                        dist = math.sqrt(bx**2 + by**2 + bz**2)
                        if dist <= nomrange:
                            blockPos = (x + bx, y + by, z + bz)
                            blockDict = CompFactory.CreateBlockInfo(levelId).GetBlockNew(blockPos,dimensionId)
                            if blockDict:
                                if blockDict.get("name") != "minecraft:air":
                                    CompFactory.CreateBlockInfo(levelId).SetBlockNew(blockPos, {"name": "minecraft:air", "aux": 0}, 1, dimensionId)
            a_Pos = (x - nomrange, y - nomrange, z - nomrange)
            b_Pos = (x + nomrange, y + nomrange, z + nomrange)
            DamageList = CompFactory.CreateGame(levelId).GetEntitiesInSquareArea(None, a_Pos, b_Pos, dimensionId)
            if DamageList:
                for Id in DamageList:
                    Id_identifier = CompFactory.CreateEngineType(Id).GetEngineTypeStr()
                    if Id == entityId or Id_identifier == identifier:
                        continue  # 跳过黑洞自身
                    CompFactory.CreateHurt(Id).Hurt(4.0, "void", srcId, entityId, False)

    elif despawnTime is not None and despawnTime <= 0:
        #黑洞坍缩爆炸并秒杀一般生物
        CompFactory.CreateExplosion(levelId).CreateExplosion(Pos, 6, True, True, entityId, srcId)
        DestroyEntity(entityId)
        killrange = 5
        ka_Pos = (x - killrange, y - killrange, z - killrange)
        kb_Pos = (x + killrange, y + killrange, z + killrange)
        killList = CompFactory.CreateGame(levelId).GetEntitiesInSquareArea(None, ka_Pos, kb_Pos, dimensionId)
        if killList:
            for Id in killList:
                Id_identifier = CompFactory.CreateEngineType(Id).GetEngineTypeStr()
                if Id == entityId or Id_identifier == identifier:
                    continue  # 跳过黑洞自身
                CompFactory.CreateGame(levelId).KillEntity(Id)

@Listen("ProjectileDoHitEffectEvent")
# 终望珍珠命中生成黑洞
def OnEndestPearlHit(args={}):
    srcId = args["srcId"]
    projectileId = args["id"]
    dimensionId = CompFactory.CreateDimension(projectileId).GetEntityDimensionId()
    projectileIdentifier = CompFactory.CreateEngineType(projectileId).GetEngineTypeStr()
    hitTargetType = args["hitTargetType"]
    # 如果不是终望珍珠则直接返回
    if projectileIdentifier != 'avaritia:endest_pearl':
        return
    if hitTargetType != 'BLOCK':
        return
    blockPos = (args["blockPosX"], args["blockPosY"], args["blockPosZ"])
    Pos = (args["blockPosX"] + 0.5, args["blockPosY"] + 0.5, args["blockPosZ"] + 0.5)
    DestroyEntity(projectileId)
    #生成黑洞
    Id = _loaderSystem.CreateEngineEntityByTypeStr("avaritia:black_hole", Pos, (0, 0), dimensionId)
    if Id:
        CompFactory.CreateExtraData(Id).SetExtraData("blockPos", blockPos)
        CompFactory.CreateExtraData(Id).SetExtraData("srcId", srcId)
        CompFactory.CreateExtraData(Id).SetExtraData("despawnTime", 186)
    
# 终望珍珠投掷
@Listen("ItemUseAfterServerEvent")
def OnEndestPearlUse(args={}):#仿原版投掷音效手势
    entityId = args["entityId"]
    itemDict = args["itemDict"]
    if itemDict["newItemName"] != 'avaritia:endest_pearl':
        return
    DimensionId = CompFactory.CreateDimension(entityId).GetEntityDimensionId()
    Pos = CompFactory.CreatePos(entityId).GetFootPos()
    if SetPlayerUsedCD(entityId) == True:
        return
    ToAllPlayerPlaySound(DimensionId, Pos,"random.bow",random.uniform(0.8,1.0),random.uniform(0.33,0.5))

#终望珍珠和黑洞的不朽
@Listen("HealthChangeBeforeServerEvent")
def OnEternalEndestPearlAndBlackHole(args={}):
    entityId = args["entityId"]
    fromHealth = args["from"]
    toHealth = args["to"]
    EternalIdentifier = CompFactory.CreateEngineType(entityId).GetEngineTypeStr()
    if EternalIdentifier != "avaritia:black_hole" and EternalIdentifier != "avaritia:endest_pearl":
        return
    if toHealth < fromHealth:
        args["cancel"] = True