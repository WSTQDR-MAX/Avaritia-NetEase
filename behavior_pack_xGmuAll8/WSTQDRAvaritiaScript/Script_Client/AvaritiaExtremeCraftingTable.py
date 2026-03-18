# -*- coding: utf-8 -*-
import client.extraClientApi as clientApi
from WSTQDRAvaritiaScript.QuModLibs.Client import Call
CustomUIScreenProxy = clientApi.GetUIScreenProxyCls()
ViewBinder = clientApi.GetViewBinderCls()
playerId = clientApi.GetLocalPlayerId()
CompFactory = clientApi.GetEngineCompFactory()

MAIN_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/common_panel/bg_image/container_panel/extreme_crafting_table_panel_top_half/main_panel"
BUTTON_PATH = MAIN_PATH + "/button"
ITEM_RENDER_PATH = MAIN_PATH + "/item_render"

class AvaritiaExtremeCraftingTable(CustomUIScreenProxy):
    def __init__(self, screenName, screenNode):
        CustomUIScreenProxy.__init__(self, screenName, screenNode)
        self.screenNode = screenNode # 拿到起，获取控件
        self.button = None # 初始化按钮组件
        self.item_render = None

    def OnCreate(self):
        self.item_render = self.screenNode.GetBaseUIControl(ITEM_RENDER_PATH)
        self.button = self.screenNode.GetBaseUIControl(BUTTON_PATH)
        buttonControl = self.button.asButton()
        buttonControl.AddTouchEventParams()
        buttonControl.SetButtonTouchUpCallback(self.OnGetResult)

    def OnGetResult(self, args):
        Pos = CompFactory.CreateModAttr(playerId).GetAttr("avaritiaOpenUIPos")
        if not Pos:
            return
        data = {"playerId":playerId, "blockPos":Pos}
        Call("OnExtremeCraftingTableResult", data)

    def OnTick(self):
        Pos = CompFactory.CreateModAttr(playerId).GetAttr("avaritiaOpenUIPos")
        if not Pos:
            return
        data = {"playerId":playerId}
        Call("OnExtremeCraftingTableTick", data)
        OutputItem = CompFactory.CreateModAttr(playerId).GetAttr("AvaritiaExtremeCraftingTableResult")
        #渲染物品
        if OutputItem:
            self.screenNode.GetBaseUIControl(MAIN_PATH).SetVisible(True)
            OutputItemName = OutputItem["newItemName"]
            self.item_render.asItemRenderer().SetUiItem(OutputItemName, 0, False)
        else:
            self.screenNode.GetBaseUIControl(MAIN_PATH).SetVisible(False)