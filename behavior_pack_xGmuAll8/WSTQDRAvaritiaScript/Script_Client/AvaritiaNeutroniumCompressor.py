# -*- coding: utf-8 -*-
import client.extraClientApi as clientApi
from WSTQDRAvaritiaScript.QuModLibs.Client import Call
NeutroniumCompressorUIScreenProxy = clientApi.GetUIScreenProxyCls()
ViewBinder = clientApi.GetViewBinderCls()
playerId = clientApi.GetLocalPlayerId()
CompFactory = clientApi.GetEngineCompFactory()

RENDER_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/common_panel/bg_image/container_panel/neutronium_compressor_panel_top_half/item_render"

class AvaritiaNeutroniumCompressor(NeutroniumCompressorUIScreenProxy):
    def __init__(self, screenName, screenNode):
        NeutroniumCompressorUIScreenProxy.__init__(self, screenName, screenNode)
        self.screenNode = screenNode # 拿到起，获取控件
        self.progress = None # 初始化奇点收集进度
        self.render_panel = None # 初始化渲染面板

    def OnCreate(self):
        self.render_panel = self.screenNode.GetBaseUIControl(RENDER_PANEL_PATH)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#progress")
    def OnNeutronCollectorProgress(self):
        Pos = CompFactory.CreateModAttr(playerId).GetAttr("avaritiaOpenUIPos")
        if not Pos:
            return
        data = {"playerId":playerId, "blockPos":Pos}
        Call("OnNeutroniumCompressorTick", data)
        BlockEntityData = CompFactory.CreateBlockInfo(playerId).GetBlockEntityData(Pos)
        if BlockEntityData:
            #渲染物品
            InputItemName = BlockEntityData["exData"].get("input",{}).get("newItemName",{}).get("__value__")
            OutputItemName = BlockEntityData["exData"].get("output",{}).get("newItemName",{}).get("__value__")
            if InputItemName and OutputItemName:
                self.screenNode.GetBaseUIControl(RENDER_PANEL_PATH).SetVisible(True)
                item_input = self.render_panel.GetChildByName("item_input")
                item_input.asItemRenderer().SetUiItem(InputItemName, 0, False)
                item_output = self.render_panel.GetChildByName("item_output")
                item_output.asItemRenderer().SetUiItem(OutputItemName, 0, False)
            else:
                self.screenNode.GetBaseUIControl(RENDER_PANEL_PATH).SetVisible(False)
            progress = BlockEntityData["exData"].get("input",{}).get("count",{}).get("__value__")
            required_count = BlockEntityData["exData"].get("required_count",{}).get("__value__")
            if progress and required_count:
                progress_ratio = str(progress) + "/" + str(required_count)
                self.progress = "§8" + progress_ratio
            else:
                if self.progress:
                    self.progress = None
        return self.progress