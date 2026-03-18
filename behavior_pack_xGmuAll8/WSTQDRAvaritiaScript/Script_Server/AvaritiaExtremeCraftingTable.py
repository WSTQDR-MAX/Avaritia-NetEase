# -*- coding: utf-8 -*-
from WSTQDRAvaritiaScript.Script_Functions.Functions import *
from WSTQDRAvaritiaScript.QuModLibs.Server import _loaderSystem
CompFactory = serverApi.GetEngineCompFactory()

@AllowCall
def OnExtremeCraftingTableTick(args={}):
    playerId = args["playerId"]
    levelId = serverApi.GetLevelId()
    Result = CompFactory.CreateModAttr(playerId).GetAttr("AvaritiaExtremeCraftingTableResult")
    if Result:
        CompFactory.CreateModAttr(playerId).SetAttr("AvaritiaExtremeCraftingTableResult", None)
    # 构建9x9网格
    grid = []
    for row in range(9):
        row_items = []
        for col in range(9):
            slot = row * 9 + col
            item = CompFactory.CreateItem(playerId).GetPlayerUIItem(playerId, slot, False, True)
            row_items.append(item)
        grid.append(row_items)
    # 检查配方
    for recipe in ExtremeCraftingTableRecipe:
        match = False
        if "ingredients" in recipe:
            # 无序配方
            required_counts = {}
            for ing in recipe["ingredients"]:
                item_name = ing["newItemName"]
                count = ing["count"]
                required_counts[item_name] = count
            # 统计网格中的物品数量（每个格子算1个）
            actual_counts = {}
            for row in grid:
                for item in row:
                    if item:
                        item_name = item.get("newItemName")
                        if item_name:
                            actual_counts[item_name] = actual_counts.get(item_name, 0) + 1
            # 检查是否完全匹配
            if actual_counts == required_counts:
                match = True
        elif "pattern" in recipe:
            # 有序配方：支持形状平移
            pattern_rows = len(recipe["pattern"])
            pattern_cols = max(len(row) for row in recipe["pattern"]) if pattern_rows > 0 else 0
            # 遍历所有可能的起始位置
            for row_offset in range(10 - pattern_rows):
                for col_offset in range(10 - pattern_cols):
                    match = True
                    for pr in range(pattern_rows):
                        pattern_row = recipe["pattern"][pr]
                        for pc in range(len(pattern_row)):
                            char = pattern_row[pc]
                            grid_r = row_offset + pr
                            grid_c = col_offset + pc
                            if grid_r >= 9 or grid_c >= 9:
                                match = False
                                break
                            actual = grid[grid_r][grid_c]
                            if char == ' ':
                                if actual is not None:
                                    match = False
                                    break
                            else:
                                expected = recipe["key"][char]
                                if actual is None:
                                    match = False
                                    break
                                actual_name = actual.get("newItemName")
                                if "newItemName" in expected:
                                    if actual_name != expected["newItemName"]:
                                        match = False
                                        break
                                elif "tags" in expected:
                                    # 标签匹配
                                    if actual_name:
                                        block_info = CompFactory.CreateBlockInfo(levelId).GetBlockBasicInfo(actual_name)
                                        actual_tags = block_info.get("tags", [])
                                        required_tags = expected["tags"]
                                        if not all(tag in actual_tags for tag in required_tags):
                                            match = False
                                            break
                                    else:
                                        match = False
                                        break
                        if not match:
                            break
                    # 检查超出pattern的部分是否为空
                    if match:
                        for r in range(9):
                            for c in range(9):
                                if r < row_offset or r >= row_offset + pattern_rows or c < col_offset or c >= col_offset + pattern_cols:
                                    if grid[r][c] is not None:
                                        match = False
                                        break
                            if not match:
                                break
                    if match:
                        break
                if match:
                    break
        if match:
            CompFactory.CreateModAttr(playerId).SetAttr("AvaritiaExtremeCraftingTableResult", recipe["result"])
            break

@AllowCall
def OnExtremeCraftingTableResult(args={}):
    blockPos = args["blockPos"]
    Pos = (blockPos[0] + 0.5, blockPos[1] + 1.0, blockPos[2] + 0.5)
    playerId = args["playerId"]
    dimensionId = CompFactory.CreateDimension(playerId).GetEntityDimensionId()
    Result = CompFactory.CreateModAttr(playerId).GetAttr("AvaritiaExtremeCraftingTableResult")
    if not Result:
        return
    GetContainerItem = CompFactory.CreateItem(levelId).GetContainerItem(blockPos, 0, dimensionId, True)
    if  GetContainerItem:
        if GetContainerItem["newItemName"] != Result.get("newItemName"):
            _loaderSystem.CreateEngineItemEntity(GetContainerItem, dimensionId, Pos)
            ToAllPlayerPlaySound(dimensionId, blockPos, "random.pop", 0.5, 0.8)
            CompFactory.CreateItem(levelId).SpawnItemToContainer(Result, 0, blockPos, dimensionId)
        else:
            ItemBasicInfo = CompFactory.CreateItem(playerId).GetItemBasicInfo(GetContainerItem["newItemName"])
            maxStackSize = ItemBasicInfo.get("maxStackSize")
            if GetContainerItem["count"] < maxStackSize:
                GetContainerItem["count"] += 1
                CompFactory.CreateItem(levelId).SpawnItemToContainer(GetContainerItem, 0, blockPos, dimensionId)
            else:
                _loaderSystem.CreateEngineItemEntity(Result, dimensionId, Pos)
                ToAllPlayerPlaySound(dimensionId, blockPos, "random.pop", 0.5, 0.8)
    else:   
        CompFactory.CreateItem(levelId).SpawnItemToContainer(Result, 0, blockPos, dimensionId)
    #减去原材料
    for slot in range(0, 81):
        item = CompFactory.CreateItem(playerId).GetPlayerUIItem(playerId, slot, False, True)
        if item:
            item["count"] -= 1
            if item["count"] > 0:
                CompFactory.CreateItem(playerId).SetPlayerUIItem(playerId, slot, item, False, True)
            else:
                CompFactory.CreateItem(playerId).SetPlayerUIItem(playerId, slot, {}, False, True)