# -*- coding: utf-8 -*-
from WSTQDRAvaritiaScript.Script_Functions.Functions import *
from WSTQDRAvaritiaScript.QuModLibs.Server import _loaderSystem
CompFactory = serverApi.GetEngineCompFactory()

#初始化玩家点击冷却属性
@Listen("AddServerPlayerEvent")
def OnAddServerPlayerEvent(args={}):
    playerId = args["id"]
    ResetPlayerUsedCD(playerId)

# 地蕴复生之锄
@AllowCall
def OnInfinityHoeServerUse(args={}):
    entityId = args["entityId"]
    blockPos = (args["x"], args["y"], args["z"])
    dimensionId = CompFactory.CreateDimension(entityId).GetEntityDimensionId()
    blockName = args["blockName"]
    tags = CompFactory.CreateBlockInfo(levelId).GetBlockBasicInfo(blockName).get("tags")
    print(blockName,tags)
    x, y, z = blockPos
    if not tags or not ("grass" in tags or "dirt" in tags):
        return
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            pos = (x + dx, y, z + dz)
            block = CompFactory.CreateBlockInfo(levelId).GetBlockNew(pos, dimensionId)
            if not block:
                continue
            bName = block.get("name")
            bTags = CompFactory.CreateBlockInfo(levelId).GetBlockBasicInfo(bName).get("tags")
            if bTags and ("grass" in bTags or "dirt" in bTags):
                CompFactory.CreateBlockInfo(levelId).SetBlockNew(pos, {"name": "minecraft:farmland", "aux": 0}, 0, dimensionId)
    if SetPlayerUsedCD(entityId, 0.2):
        return
    ToAllPlayerPlaySound(dimensionId, blockPos, "use.gravel", 1, 0.8)

#星球吞噬之铲和世界崩解之镐切换模式
@Listen("ServerItemTryUseEvent")
def InfinityChangeModel(args={}):
    playerId = args["playerId"]
    itemDict = args["itemDict"]
    isSneaking = CompFactory.CreatePlayer(playerId).isSneaking()
    if not isSneaking:
        return
    if itemDict.get("newItemName") == "avaritia:infinity_pickaxe":
        newItemDict = copy.deepcopy(itemDict)
        newItemDict["newItemName"] = "avaritia:infinity_hammer"
        CompFactory.CreateItem(playerId).SetEntityItem(2, newItemDict, 0)
    elif itemDict.get("newItemName") == "avaritia:infinity_hammer":
        newItemDict = copy.deepcopy(itemDict)
        newItemDict["newItemName"] = "avaritia:infinity_pickaxe"
        CompFactory.CreateItem(playerId).SetEntityItem(2, newItemDict, 0)
    elif itemDict.get("newItemName") == "avaritia:infinity_shovel":
        newItemDict = copy.deepcopy(itemDict)
        newItemDict["newItemName"] = "avaritia:infinity_destroyer"
        CompFactory.CreateItem(playerId).SetEntityItem(2, newItemDict, 0)
    elif itemDict.get("newItemName") == "avaritia:infinity_destroyer":
        newItemDict = copy.deepcopy(itemDict)
        newItemDict["newItemName"] = "avaritia:infinity_shovel"
        CompFactory.CreateItem(playerId).SetEntityItem(2, newItemDict, 0)

#星球吞噬之铲和世界崩解之镐吞噬并生成物质团
@Listen("DestroyBlockEvent")
def OnInfinityToolsEngulfBlock(args={}):#17*17破坏不吞噬
    playerId = args["playerId"]
    FootPos = CompFactory.CreatePos(playerId).GetFootPos()
    blockPos = (args["x"], args["y"], args["z"])
    blockName = args["fullName"]
    tags = CompFactory.CreateBlockInfo(levelId).GetBlockBasicInfo(blockName).get("tags")
    dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    itemDict = CompFactory.CreateItem(playerId).GetEntityItem(2, 0)
    if not itemDict:
        return
    itemName = itemDict.get("newItemName")
    extend = 8
    PosList = []
    gameType = CompFactory.CreateGame(playerId).GetPlayerGameType(playerId)
    model = None
    if gameType == 1:
        model = "clean"
    if itemName == "avaritia:infinity_hammer":
        PosList = DestroyBlocksByTags(blockPos, dimensionId, extend, None, model)
    elif itemName == "avaritia:infinity_destroyer":
        Tags = ["minecraft:is_shovel_item_destructible"]
        if "minecraft:is_shovel_item_destructible" in tags:
            PosList = DestroyBlocksByTags(blockPos, dimensionId, extend, Tags, model)
    if PosList:
        CreateMatterCluster(PosList, dimensionId, FootPos)   

@Listen("StartDestroyBlockServerEvent")
def OnInfinityToolsGetNFR_BLOCK(args={}):#生存模式获取基岩等（此时不吞噬）
    playerId = args["playerId"]
    itemDict = CompFactory.CreateItem(playerId).GetEntityItem(2, 0)
    if not itemDict:
        return
    itemName = itemDict.get("newItemName")
    if itemName != "avaritia:infinity_hammer" and itemName != "avaritia:infinity_pickaxe":
        return
    dimensionId = args["dimensionId"]
    x, y, z = args["pos"]
    blockName = args["blockName"]
    tags = CompFactory.CreateBlockInfo(levelId).GetBlockBasicInfo(blockName).get("tags")
    if tags and "not_feature_replaceable" in tags:
        CompFactory.CreateBlockInfo(levelId).SetBlockNew((x, y, z),{"name":"minecraft:air", "aux":0}, 1, dimensionId)
        n_f_r_Dict = {"newItemName":blockName, "count":1}
        _loaderSystem.CreateEngineItemEntity(n_f_r_Dict, dimensionId, (x + 0.5, y + 0.5, z + 0.5))   

# 自然荒芜之斧破坏树木
# 模式一        
@Listen("ServerPlayerTryDestroyBlockEvent")
def OnInfinityAxeDestroyBlock(args={}):#创造模式连锁
    playerId = args["playerId"]
    blockPos = (args["x"], args["y"], args["z"])
    dimensionId = args["dimensionId"]
    itemDict = CompFactory.CreateItem(playerId).GetEntityItem(2, 0)
    if not itemDict:
        return
    itemName = itemDict.get("newItemName")
    if itemName == "avaritia:infinity_axe":
        isSneaking = CompFactory.CreatePlayer(playerId).isSneaking()
        if isSneaking:
            return
        gameType = CompFactory.CreateGame(playerId).GetPlayerGameType(playerId)
        extend = 8
        if gameType == 1:
            DestroyBlocksByTags(blockPos, dimensionId, extend, ["minecraft:is_axe_item_destructible"], "clean")
        else:
            DestroyBlocksByTags(blockPos, dimensionId, extend, ["minecraft:is_axe_item_destructible"])

# 模式二（生成物质团)
CompFactory.CreateItem(serverApi.GetLevelId()).GetUserDataInEvent("ServerItemTryUseEvent")
@Listen("ServerItemTryUseEvent")
def OnInfinityAxeTryUse(args={}):
    playerId = args["playerId"]
    itemDict = args["itemDict"]
    Pos = CompFactory.CreatePos(playerId).GetPos()
    FootPos = CompFactory.CreatePos(playerId).GetFootPos()
    blockPos = (int(Pos[0]), int(Pos[1]), int(Pos[2]))
    if itemDict["newItemName"] != "avaritia:infinity_axe":
        return
    isSneaking = CompFactory.CreatePlayer(playerId).isSneaking()
    if not isSneaking:
        return
    Call(playerId, "PlaySwing")
    dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    extend = 8
    Tags = ["minecraft:is_axe_item_destructible"]
    gameType = CompFactory.CreateGame(playerId).GetPlayerGameType(playerId)
    model = None
    if gameType == 1:
        model = "clean"
    PosList = DestroyBlocksByTags(blockPos, dimensionId, extend, Tags, model)
    # 生成物质团
    if PosList:
        CreateMatterCluster(PosList, dimensionId, FootPos)

#选择区域内带有指定标签的方块(当Tags == None时表示不分种类)
def DestroyBlocksByTags(blockPos, dimensionId, extend, Tags = None, model = None):
    '''
    选择区域内带有指定标签的方块并破坏，返回一个方块坐标列表
    
    extend: 中心点延展的距离
    Tags: 方块标签
    model: 填"clean"则清除掉落物，一旦选择此模式，后续无法生成物质团
    '''
    x, y, z = blockPos
    destroyed_positions = {blockPos}
    for dx in range(-extend, extend+1):
        for dy in range(-extend, extend+1):
            for dz in range(-extend, extend+1):
                nx, ny, nz = x+dx, y+dy, z+dz
                blockName = CompFactory.CreateBlockInfo(levelId).GetBlockNew((nx, ny, nz), dimensionId).get("name")
                if blockName == "mincraft:air":
                    continue
                tags = CompFactory.CreateBlockInfo(levelId).GetBlockBasicInfo(blockName).get("tags")
                if not Tags and tags and "not_feature_replaceable" in tags:
                    n_f_r_Dict = {"newItemName":blockName, "count":1}
                    _loaderSystem.CreateEngineItemEntity(n_f_r_Dict, dimensionId, (nx + 0.5, ny + 0.5, nz + 0.5))
                if Tags is None or (tags and any(tag in tags for tag in Tags)) or (Tags is None and not tags):
                    CompFactory.CreateBlockInfo(levelId).SetBlockNew((nx, ny, nz),{"name":"minecraft:air", "aux":0}, 1, dimensionId)
                    # 根据model判断是否清理掉落物, 如果清理了就不能打包物质团
                    if model == "clean":
                        startPos = (nx, ny, nz)
                        endPos = (startPos[0] + 1, startPos[1] + 1, startPos[2] + 1)
                        Entities = CompFactory.CreateGame(levelId).GetEntitiesInSquareArea(None, startPos, endPos, dimensionId)
                        for id in Entities:
                            DestroyEntity(id)
                    if (nx, ny, nz) not in destroyed_positions:
                        destroyed_positions.add( (nx, ny, nz) )
    return list(destroyed_positions)

def normalize_nbt_for_merge(nbt):
    normalized = copy.deepcopy(nbt)
    normalized["Item"]["Count"]["__value__"] = 1
    normalized["UniqueID"]["__value__"] = 1
    normalized["Pos"][0]["__value__"] = 1
    normalized["Pos"][1]["__value__"] = 1
    normalized["Pos"][2]["__value__"] = 1
    normalized["Motion"][0]["__value__"] = 1
    normalized["Motion"][1]["__value__"] = 1
    normalized["Motion"][2]["__value__"] = 1
    normalized["internalComponents"]["EntityStorageKeyComponent"]["StorageKey"]["__value__"] = 1
    return normalized

#生成物质团通用
def CreateMatterCluster(PosList, dimensionId, FootPos):
    entityList = set()
    for startPos in PosList:
        endPos = (startPos[0] + 1, startPos[1] + 1, startPos[2] + 1)
        Entities = CompFactory.CreateGame(levelId).GetEntitiesInSquareArea(None, startPos, endPos, dimensionId)
        for id in Entities:
            NBT_Tags = CompFactory.CreateEntityDefinitions(id).GetEntityNBTTags()
            if NBT_Tags:
                name = NBT_Tags.get("Item",{}).get("Name",{}).get("__value__")
                if name == "avaritia:matter_cluster":#防止物质团无限套娃
                    continue
            entityList.add(id)
    # 收集所有物品数据
    all_items = []
    for entityId in entityList:
        NBT_Tags = CompFactory.CreateEntityDefinitions(entityId).GetEntityNBTTags()
        if not NBT_Tags:
            continue
        Tags_Item = NBT_Tags.get("Item",{})
        name = Tags_Item.get("Name",{}).get("__value__")
        count = Tags_Item.get("Count",{}).get("__value__", 0)
        if Tags_Item and name and count > 0:
            all_items.append((NBT_Tags, count))
    if not all_items:
        return  # 没有物品，不生成物质团
    # 删除所有实体
    for entityId in entityList:
        DestroyEntity(entityId)
    # 现在生成物质团，每个最多4096个物品
    cluster_index = 0
    while all_items:
        NBTDict = {}
        index = 0
        item_Totals = 0
        merge_dict = {}  # 键：标准化nbt哈希，值：可用空间索引列表
        items_to_process = all_items[:]
        all_items = []
        for NBT_Tags, count in items_to_process:
            remaining = count
            Tags_Item = NBT_Tags.get("Item",{})
            name = Tags_Item.get("Name",{}).get("__value__")
            t_I_maxStackSize = 64
            t_I_BasicInfo = CompFactory.CreateItem(levelId).GetItemBasicInfo(name)
            if t_I_BasicInfo:
                t_I_maxStackSize = t_I_BasicInfo.get("maxStackSize", 64)
            # 计算标准化键
            normalized = normalize_nbt_for_merge(NBT_Tags)
            key = str(normalized)  # 直接使用字符串表示唯一性
            # 尝试合并到现有槽位
            merged = False
            if key in merge_dict:
                for idx in merge_dict[key][:]:  # 复制列表以避免修改问题
                    if remaining <= 0:
                        break
                    slot_nbt = NBTDict[str(idx)]
                    slot_count = slot_nbt["Item"]["Count"]["__value__"]
                    space = t_I_maxStackSize - slot_count
                    if space > 0:
                        add = min(space, remaining)
                        if item_Totals + add > 4096:
                            add = 4096 - item_Totals
                        if add > 0:
                            slot_nbt["Item"]["Count"]["__value__"] += add
                            remaining -= add
                            item_Totals += add
                            if slot_count + add >= t_I_maxStackSize:
                                merge_dict[key].remove(idx)  # 没有更多空间
                            merged = True
            # 如果未完全合并，添加新槽位
            while remaining > 0 and item_Totals < 4096:
                add = min(remaining, t_I_maxStackSize)
                if item_Totals + add > 4096:
                    add = 4096 - item_Totals
                if add <= 0:
                    break
                new_NBT_Tags = copy.deepcopy(NBT_Tags)
                new_NBT_Tags["Item"]["Count"]["__value__"] = add
                NBTDict[str(index)] = new_NBT_Tags
                if add < t_I_maxStackSize:
                    if key not in merge_dict:
                        merge_dict[key] = []
                    merge_dict[key].append(index)
                index += 1
                remaining -= add
                item_Totals += add
            # 如果还有剩余，放到下一个物质团
            if remaining > 0:
                all_items.append((NBT_Tags, remaining))
        # 生成物质团
        if NBTDict:
            print(len(NBTDict))
            # 计算customTips，汇总同种物品的数量，不受maxStackSize堆叠限制
            item_totals = {}
            for key in NBTDict.items():
                idx, nbt = key
                Tags_Item = nbt.get("Item")
                name = Tags_Item.get("Name").get("__value__")
                count = Tags_Item.get("Count").get("__value__")
                if name in item_totals:
                    item_totals[name] += count
                else:
                    item_totals[name] = count
            total_sum = sum(item_totals.values())
            text = "\n".join(["§l§i%s§l§8 x %s" % (name, total) for name, total in item_totals.items()])
            customTips = '%%name%%%%category%%\n§l§i%d / §l§i%d items\n%s\n%%enchanting%%%%attack_damage%%' % (total_sum, 4096, text)
            matterCluster = {
            "newItemName": "avaritia:matter_cluster",
            "newAuxValue": 0,
            "count": 1,
            "userData": {"StorageVein":NBTDict},
            "customTips": customTips
            }
            _loaderSystem.CreateEngineItemEntity(matterCluster, dimensionId, FootPos)
            cluster_index += 1

#打开物质团
@Listen("ServerItemTryUseEvent")
def OnOpenMatterCluster(args={}):
    playerId = args["playerId"]
    itemDict = args["itemDict"]
    Pos = CompFactory.CreatePos(playerId).GetFootPos()
    dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    if not itemDict:
        return
    itemName = itemDict.get("newItemName")
    if itemName == "avaritia:matter_cluster":
        userData = itemDict.get("userData")
        if not userData:
            return
        NBTDict = userData.get("StorageVein")
        if not NBTDict:
            return
        for key in NBTDict.items():
            index, NBT_Tags = key
            _loaderSystem.CreateEngineEntityByNBT(NBT_Tags, Pos, None, dimensionId)
        # 减少物质团数量
        SpawnLessItemsToPlayer(itemDict, playerId)

#炽焰之啄颅剑百分百掉落骷髅头
@Listen("EntityDieLoottableServerEvent")
def OnFierySwordKill(args={}):
    dieEntityId = args["dieEntityId"]
    attacker = args["attacker"]
    itemList = args["itemList"]
    dieEntityIdentifier = CompFactory.CreateEngineType(dieEntityId).GetEngineTypeStr()
    if dieEntityIdentifier == "minecraft:wither_skeleton":
        itemDict = CompFactory.CreateItem(attacker).GetEntityItem(2, 0)
        if not itemDict:
            return
        itemName = itemDict.get("newItemName")
        if itemName == "avaritia:fiery_sword":
            found = False
            for item in itemList:
                if item["newItemName"] =="minecraft:wither_skeleton_skull":
                    found = True
            if not found:
                itemList.append({"newItemName":"minecraft:wither_skeleton_skull", "count": 1})
                args["dirty"] = True

# 寰宇支配之剑秒杀
@Listen("DamageEvent")# 不能选中创造玩家
def OnInfinitySwordDamage(args={}):
    srcId = args["srcId"]
    entityId = args["entityId"]
    itemDict = CompFactory.CreateItem(srcId).GetEntityItem(2, 0)
    if not itemDict:
        return
    itemName = itemDict.get("newItemName")
    if itemName == "avaritia:infinity_sword":
        helmet = CompFactory.CreateItem(entityId).GetEntityItem(3, 0)
        chestplate = CompFactory.CreateItem(entityId).GetEntityItem(3, 1)
        leggings = CompFactory.CreateItem(entityId).GetEntityItem(3, 2)
        boots = CompFactory.CreateItem(entityId).GetEntityItem(3, 3)
        if helmet and chestplate and leggings and boots:
            if helmet["newItemName"] == "avaritia:infinity_helmet" and chestplate["newItemName"] == "avaritia:infinity_chestplate"\
            and leggings["newItemName"] == "avaritia:infinity_leggings" and boots["newItemName"] == "avaritia:infinity_boots":
                CompFactory.CreateHurt(entityId).Hurt(1, "override", srcId, None, True)
                return
        kill = CompFactory.CreateGame(levelId).KillEntity(entityId)
        if not kill:
            DestroyEntity(entityId)        

@Listen("PlayerAttackEntityEvent")# 选中创造玩家
def OnInfinitySwordAttack(args={}):
    playerId = args["playerId"]
    victimId = args["victimId"]
    Identifier = CompFactory.CreateEngineType(victimId).GetEngineTypeStr()
    if Identifier != "minecraft:player":
        return
    PlayerGameType = CompFactory.CreateGame(levelId).GetPlayerGameType(victimId)
    if PlayerGameType != 1:
        return
    itemDict = CompFactory.CreateItem(playerId).GetEntityItem(2, 0)
    if not itemDict:
        return
    itemName = itemDict.get("newItemName")
    if itemName == "avaritia:infinity_sword":
        helmet = CompFactory.CreateItem(victimId).GetEntityItem(3, 0)
        chestplate = CompFactory.CreateItem(victimId).GetEntityItem(3, 1)
        leggings = CompFactory.CreateItem(victimId).GetEntityItem(3, 2)
        boots = CompFactory.CreateItem(victimId).GetEntityItem(3, 3)
        if helmet and chestplate and leggings and boots:
            if helmet["newItemName"] == "avaritia:infinity_helmet" and chestplate["newItemName"] == "avaritia:infinity_chestplate"\
            and leggings["newItemName"] == "avaritia:infinity_leggings" and boots["newItemName"] == "avaritia:infinity_boots":
                return
        CompFactory.CreateGame(levelId).KillEntity(victimId)

@Listen("ItemReleaseUsingServerEvent")
# 天堂陨落长弓发射箭矢
def OnInfinityBowUsing(args={}):
    playerId, itemDict = args['playerId'], args['itemDict']
    # 如果右键时间太短，或不是自定义弓则直接返回
    if args['maxUseDuration'] - args['durationLeft'] < 3 or itemDict['newItemName'] != 'avaritia:infinity_bow':
        return
    # 计算power并发射箭矢，算法和原版代码一致
    power = (args['maxUseDuration']-args['durationLeft'])/20.0
    pos = CompFactory.CreatePos(playerId).GetPos()
    dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    CompFactory.CreateProjectile(levelId).CreateProjectileEntity(playerId, 'avaritia:heaven_arrow',
    {'position': (pos[0], pos[1]-0.1, pos[2]), 'power': max(5.0*min(power*(power+2)/3, 1.0), 0.5)})
    ToAllPlayerPlaySound(dimensionId, pos, 'random.bow', 1, 1)

# 无尽套装无敌效果
@Listen("HealthChangeBeforeServerEvent")
def OnInfinityArmorInvulnerable(args={}):
    entityId = args["entityId"]
    fromHealth = args["from"]
    toHealth = args["to"]
    helmet = CompFactory.CreateItem(entityId).GetEntityItem(3, 0)
    chestplate = CompFactory.CreateItem(entityId).GetEntityItem(3, 1)
    leggings = CompFactory.CreateItem(entityId).GetEntityItem(3, 2)
    boots = CompFactory.CreateItem(entityId).GetEntityItem(3, 3)
    if not helmet or not chestplate or not leggings or not boots:
        return
    if helmet["newItemName"] != "avaritia:infinity_helmet" or chestplate["newItemName"] != "avaritia:infinity_chestplate"\
    or leggings["newItemName"] != "avaritia:infinity_leggings" or boots["newItemName"] != "avaritia:infinity_boots":
        return
    if toHealth < fromHealth:
        args["cancel"] = True

serverApi.AddEntityTickEventWhiteList('minecraft:player')
# 无尽套装各种效果
@Listen("EntityTickServerEvent")
def OnInfinityChestplateTick(args={}):
    entityId = args["entityId"]
    #判断是否开启翅膀
    Fly = CompFactory.CreateFly(entityId).IsPlayerFlying()
    if Fly:
        data = {"entityId":entityId, "Molang":"query.mod.avaritia_wing", "Value":1.0}
        Call(entityId, "SetMolang", data)
    else:
        data = {"entityId":entityId, "Molang":"query.mod.avaritia_wing", "Value":0.0}
        Call(entityId, "SetMolang", data)
    helmet = CompFactory.CreateItem(entityId).GetEntityItem(3, 0)
    chestplate = CompFactory.CreateItem(entityId).GetEntityItem(3, 1)
    leggings = CompFactory.CreateItem(entityId).GetEntityItem(3, 2)
    boots = CompFactory.CreateItem(entityId).GetEntityItem(3, 3)
    # 无尽护腿熄灭火焰
    if leggings and leggings["newItemName"] == "avaritia:infinity_leggings":
        if CompFactory.CreateAttr(entityId).IsEntityOnFire():
            CompFactory.CreateAttr(entityId).SetEntityOnFire(0, 0)
    # 无尽靴子跳跃速度提升
    if boots and boots["newItemName"] == "avaritia:infinity_boots":
        CompFactory.CreateEffect(entityId).AddEffectToEntity("speed", 15.1, 3, False)
        CompFactory.CreateEffect(entityId).AddEffectToEntity("jump_boost", 15.1, 3, False)
    # 无尽头盔无限夜视15秒,无限饥饿饱和度，无限氧气300, 快速消耗饱食度回血
    if helmet and helmet["newItemName"] == "avaritia:infinity_helmet":
        CompFactory.CreateEffect(entityId).AddEffectToEntity("night_vision", 15.1, 0, False)
        Huger = CompFactory.CreateAttr(entityId).GetAttrValue(4)
        if Huger < 20.0:
            CompFactory.CreateAttr(entityId).SetAttrValue(4, 20.0, 0)
        Saturation = CompFactory.CreateAttr(entityId).GetAttrValue(5)
        if Saturation < 20.0:
            CompFactory.CreateAttr(entityId).SetAttrValue(5, 20.0, 0)
        AirSupply = CompFactory.CreateBreath(entityId).GetCurrentAirSupply()
        if AirSupply < 300:
            CompFactory.CreateBreath(entityId).SetCurrentAirSupply(300)
        OmegaHealTick = CompFactory.CreateExtraData(entityId).GetExtraData("OmegaHealTick")
        if not OmegaHealTick:
            CompFactory.CreatePlayer(entityId).SetPlayerHealthTick(10)
            #标记寰宇之力加速回血
            OmegaHealTick = CompFactory.CreateExtraData(entityId).SetExtraData("OmegaHealTick", True)
    elif not helmet or helmet["newItemName"] != "avaritia:infinity_helmet":
        # 取消寰宇之力加速回血
        OmegaHealTick = CompFactory.CreateExtraData(entityId).GetExtraData("OmegaHealTick")
        if OmegaHealTick:
            CompFactory.CreatePlayer(entityId).SetPlayerHealthTick(80)
            CompFactory.CreateExtraData(entityId).CleanExtraData("OmegaHealTick")
    # 无尽胸甲免疫负面效果,飞行
    if chestplate and chestplate["newItemName"] == "avaritia:infinity_chestplate":
        # 移除所有负面效果
        for effectName in [
            "slowness","mining_fatigue","instant_damage","nausea","blindness",
            "hunger","weakness","wither","poison","fatal_poison","levitation",
            "darkness","wind_charged","weaving","oozing","infested"
            ]:
            if CompFactory.CreateEffect(entityId).HasEffect(effectName):
                CompFactory.CreateEffect(entityId).RemoveEffectFromEntity(effectName)
        CanFly = CompFactory.CreateFly(entityId).IsPlayerCanFly()
        if not CanFly:
            CompFactory.CreateFly(entityId).ChangePlayerFlyState(True, False)
    elif not chestplate or chestplate["newItemName"] != "avaritia:infinity_chestplate":
        gameType = CompFactory.CreateGame(entityId).GetPlayerGameType(entityId)
        if gameType == 1:#创造模式不取消
            return
        # 取消飞行能力
        CanFly = CompFactory.CreateFly(entityId).IsPlayerCanFly()
        if CanFly:
            CompFactory.CreateFly(entityId).ChangePlayerFlyState(False)
            
# 防止无尽套装飞行时掉落
@Listen("AddServerPlayerEvent")# 防止存档重载时飞行掉落
def OnAddServerPlayerEvent(args={}):
    playerId = args["id"]
    x, y, z =CompFactory.CreatePos(playerId).GetPos()
    Pos = (x, y - 1.62, z)
    dimesionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    chestplate = CompFactory.CreateItem(playerId).GetEntityItem(3, 1)
    if not chestplate or chestplate["newItemName"] != "avaritia:infinity_chestplate":
        return
    Fly = CompFactory.CreateFly(playerId).IsPlayerFlying()
    if not Fly:
        CompFactory.CreateFly(playerId).ChangePlayerFlyState(True, True)
        CompFactory.CreateDimension(playerId).ChangePlayerDimension(dimesionId, Pos)

@Listen("GameTypeChangedServerEvent")# 防止切换模式时飞行掉落
def OnGameTypeChangedServerEvent(args={}):
    playerId = args["playerId"]
    x, y, z =CompFactory.CreatePos(playerId).GetPos()
    Pos = (x, y - 1.62, z)
    dimesionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    Fly = CompFactory.CreateFly(playerId).IsPlayerFlying()
    if Fly:
        compFactory.CreateGame(playerId).AddTimer(0.0, CompFactory.CreateFly(playerId).ChangePlayerFlyState,True, True)
        compFactory.CreateGame(playerId).AddTimer(0.0, CompFactory.CreateDimension(playerId).ChangePlayerDimension, dimesionId, Pos)