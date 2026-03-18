# -*- coding: utf-8 -*-
import client.extraClientApi as clientApi
CustomUIScreenProxy = clientApi.GetUIScreenProxyCls()
ViewBinder = clientApi.GetViewBinderCls()
playerId = clientApi.GetLocalPlayerId()
CompFactory = clientApi.GetEngineCompFactory()

class AvaritiaNeutronCollector(CustomUIScreenProxy):
    def __init__(self, screenName, screenNode):
        CustomUIScreenProxy.__init__(self, screenName, screenNode)
        self.progress = None # 初始化中子尘埃收集进度

    @ViewBinder.binding(ViewBinder.BF_BindString, "#progress")
    def OnNeutronCollectorProgress(self):
        Pos = CompFactory.CreateModAttr(playerId).GetAttr("avaritiaOpenUIPos")
        if not Pos:
            return
        BlockEntityData = CompFactory.CreateBlockInfo(playerId).GetBlockEntityData(Pos)
        if BlockEntityData:
            progress = BlockEntityData["exData"].get("progress",{}).get("__value__")
            if progress:
                progress_ratio = "%.2f" % (progress * 100.0 / 7111.0)
                self.progress = "§8" + progress_ratio +"％"
        return self.progress