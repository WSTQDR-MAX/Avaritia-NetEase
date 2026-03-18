# -*- coding: utf-8 -*-
from WSTQDRAvaritiaScript.QuModLibs.Client import *
CompFactory = clientApi.GetEngineCompFactory()

#几个ui
NativeScreenManager = clientApi.GetNativeScreenManagerCls()
NativeScreenManager.instance().RegisterScreenProxy("NeutronCollector.neutron_collector_screen", "WSTQDRAvaritiaScript.Script_Client.AvaritiaNeutronCollector.AvaritiaNeutronCollector")
NativeScreenManager.instance().RegisterScreenProxy("NeutroniumCompressor.neutronium_compressor_screen", "WSTQDRAvaritiaScript.Script_Client.AvaritiaNeutroniumCompressor.AvaritiaNeutroniumCompressor")
NativeScreenManager.instance().RegisterScreenProxy("ExtremeCraftingTable.extreme_crafting_table_screen", "WSTQDRAvaritiaScript.Script_Client.AvaritiaExtremeCraftingTable.AvaritiaExtremeCraftingTable")

@Listen("ClientBlockUseEvent")
def OnClientBlockUsed(args):
    blockName = args["blockName"]
    blockPos = (args["x"], args["y"], args["z"])
    UI_blockSet = {"avaritia:neutron_collector", "avaritia:neutronium_compressor", "avaritia:extreme_crafting_table"}
    if blockName in UI_blockSet:
        CompFactory.CreateModAttr(playerId).SetAttr("avaritiaOpenUIPos", blockPos)

@AllowCall
def OnPlaySound(args={}):
    soundName = args["soundName"]
    pos = args["pos"]
    volume = args["volume"]
    pitch = args["pitch"]
    CompFactory.CreateCustomAudio(levelId).PlayCustomMusic(soundName, pos, volume, pitch, False, None)

@AllowCall
def PlayParticle(args={}):
    pos = args["pos"]
    ParticleName = args["ParticleName"]
    CompFactory.CreateParticleSystem(None).Create(ParticleName, pos)

@AllowCall
def SetMolang(args={}):
    entityId = args["entityId"]
    Molang = args["Molang"]
    Value = args["Value"]
    CompFactory.CreateQueryVariable(entityId).Set(Molang, Value)
    
@AllowCall
def SetEntityBlockMolang(args={}):
    pos = args["blockPos"]
    molang = args["molang"]
    name = args["name"]
    CompFactory.CreateBlockInfo(levelId).SetEnableBlockEntityAnimations(pos, True)
    CompFactory.CreateBlockInfo(levelId).SetBlockEntityMolangValue(pos, name, molang)

@AllowCall
def PlaySwing():
    CompFactory.CreatePlayer(playerId).Swing()   

@Listen(Events.LoadClientAddonScriptsAfter)
def LoadAddon(args={}):
    CompFactory.CreateQueryVariable(levelId).Register('query.mod.avaritia_wing', 0.0)

@Listen("AddPlayerCreatedClientEvent")
def AddBowAnimationToPlayer(args={}):
        comp = compFactory.CreateActorRender(args['playerId'])
        itemName = 'avaritia:infinity_bow'
        def GetTestMolang(itemName):
            # 当手持itemName，并且正在右键使用，该molang会通过
            return "query.is_item_name_any('slot.weapon.mainhand', '"+itemName+"') && query.item_remaining_use_duration"
        # 给自定义弓添加第三人称动画
        comp.AddPlayerAnimation(itemName, 'animation.player.bow_equipped')
        comp.AddPlayerAnimationIntoState('root', 'third_person', itemName, GetTestMolang(itemName))
        # 上面两句的作用是，当Molang通过，就播放动画animation.player.bow_equipped
        comp.RebuildPlayerRender()

# 地蕴复生之锄
@Listen("ClientItemUseOnEvent")
def OnInfinityHoeClientUse(args={}):
    entityId = args["entityId"]
    itemDict = args["itemDict"]
    isSneaking = CompFactory.CreatePlayer(entityId).isSneaking()
    if isSneaking:
        return
    itemName = itemDict.get("newItemName")
    if itemName == "avaritia:infinity_hoe":
        PlaySwing()
        Call("OnInfinityHoeServerUse", args)
        