# -*- coding: utf-8 -*-
from WSTQDRAvaritiaScript.Script_Functions.Functions import *
CompFactory = serverApi.GetEngineCompFactory()

serverApi.AddEntityTickEventWhiteList('avaritia:heaven_arrow')
@Listen("EntityTickServerEvent")
def HeavenArrowTickEvent(args={}):
    entityId = args["entityId"]
    identifier = args["identifier"]
    # 如果不是天堂陨落之箭则直接返回
    if identifier != 'avaritia:heaven_arrow':
        return
    despawnTime = CompFactory.CreateExtraData(entityId).GetExtraData("despawnTime")
    if despawnTime is not None and despawnTime > 0:
        CompFactory.CreateExtraData(entityId).SetExtraData("despawnTime", despawnTime - 1)
    elif despawnTime is not None and despawnTime <= 0:
        CompFactory.CreateGame(levelId).KillEntity(entityId)
    
@Listen("ProjectileDoHitEffectEvent")
# 天堂陨落之箭的命中箭雨
def HeavenArrowHitEvent(args={}):
    srcId = args["srcId"] # 创建者id
    projectileId = args["id"]
    targetId = args["targetId"] 
    hitTargetType = args["hitTargetType"]
    projectileIdentifier = CompFactory.CreateEngineType(projectileId).GetEngineTypeStr()
    # 如果不是天堂陨落之箭则直接返回
    if projectileIdentifier != 'avaritia:heaven_arrow':
        return
    if hitTargetType == 'BLOCK':
        # 如果是子箭则返回
        clone = CompFactory.CreateExtraData(projectileId).GetExtraData("clone")
        if clone:
            # 子箭设置20刻后消失
            CompFactory.CreateExtraData(projectileId).SetExtraData("despawnTime",20)
            return
        # 主箭设置100刻后消失
        CompFactory.CreateExtraData(projectileId).SetExtraData("despawnTime",100)
        blockPos = (args["blockPosX"], args["blockPosY"] + 26, args["blockPosZ"])
        blockName = CompFactory.CreateBlockInfo(srcId).GetBlockNew(blockPos).get("name")
        if blockName != "minecraft:air":
            return
        arrow_list = Barrage(args["x"],args["y"],args["z"])
        for arrow in arrow_list:
            Id = CompFactory.CreateProjectile(levelId).CreateProjectileEntity(srcId, 'avaritia:heaven_arrow',
            {'position': arrow['pos'], 'direction': arrow['direction'], 'power': arrow['power']})
            #标记为子箭
            CompFactory.CreateExtraData(Id).SetExtraData("clone",True)
    if hitTargetType == 'ENTITY':
        if targetId == srcId:
            return
        DestroyEntity(projectileId)
        CompFactory.CreateGame(levelId).KillEntity(targetId)

    
def Barrage(arrow_pos_x, arrow_pos_y, arrow_pos_z):
    '''
    生成35支箭矢的参数，用于实现箭雨效果;
    arrow_pos_x: 箭矢X坐标;
    arrow_pos_y: 箭矢Y坐标;
    arrow_pos_z: 箭矢Z坐标;
    '''
    # 存储所有箭矢的计算结果
    arrows_data = []
    # 循环生成35支箭的参数
    for i in range(35):
        # 计算箭矢生成位置
        angle = random.random() * 2 * math.pi
        dist = random.gauss(0, 1) * 0.75
        x = math.sin(angle) * dist + arrow_pos_x
        z = math.cos(angle) * dist + arrow_pos_z
        y = arrow_pos_y + 25.0

        # 计算箭矢飞行方向
        # 轻微水平散射，整体垂直向下
        dx = random.gauss(0, 0.05)  # 水平小范围随机偏移
        dz = random.gauss(0, 0.05)
        dy = -1.0  # 固定向下的方向分量
        direction = (dx, dy, dz)
        power = random.uniform(0.5, 1.5) # 随机飞行速度

        # 3. 把计算结果存入列表
        arrows_data.append({
            'pos': (x, y, z),
            'direction': direction,
            'power': power
        })
    
    return arrows_data