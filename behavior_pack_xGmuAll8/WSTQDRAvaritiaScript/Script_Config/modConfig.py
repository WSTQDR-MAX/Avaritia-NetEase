# -*- coding: utf-8 -*-

#中子态素压缩机配方
NeutroniumCompressorRecipe = {
    "minecraft:redstone_block":{"output":{"newItemName":"avaritia:redstone_singularity", "count": 1}, "required_count":200},
    "minecraft:iron_block":{"output":{"newItemName":"avaritia:iron_singularity", "count": 1}, "required_count":400},
    "minecraft:gold_block":{"output":{"newItemName":"avaritia:gold_singularity", "count": 1}, "required_count":200},
    "minecraft:lapis_block":{"output":{"newItemName":"avaritia:lapis_singularity", "count": 1}, "required_count":200},
    "minecraft:emerald_block":{"output":{"newItemName":"avaritia:emerald_singularity", "count": 1}, "required_count":200},
    "minecraft:quartz_block":{"output":{"newItemName":"avaritia:quartz_singularity", "count": 1}, "required_count":200},
    "minecraft:netherite_block":{"output":{"newItemName":"avaritia:netherite_singularity", "count": 1}, "required_count":200},
    "minecraft:diamond_block":{"output":{"newItemName":"avaritia:diamond_singularity", "count": 1}, "required_count":300},
    "minecraft:copper_block":{"output":{"newItemName":"avaritia:copper_singularity", "count": 1}, "required_count":400},
    "minecraft:amethyst_block":{"output":{"newItemName":"avaritia:amethyst_singularity", "count": 1}, "required_count":200},
}

# 9x9终极工作台配方
ExtremeCraftingTableRecipe = [
    # 中子态素收集器
    {
        "pattern": [
            "IIQQQQQII",
            "I QQQQQ I",
            "I  RRR  I",
            "X RRRRR X",
            "I RRXRR I",
            "X RRRRR X",
            "I  RRR  I",
            "I       I",
            "IIIXIXIII"
        ],
        "key": {
            "X": {"newItemName": "avaritia:crystal_matrix_ingot"},
            "I": {"newItemName": "minecraft:iron_block"},
            "Q": {"newItemName": "minecraft:quartz_block"},
            "R": {"newItemName": "minecraft:redstone_block"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:neutron_collector"
        }
    },
    # 中子态素压缩机
    {
        "pattern": [
            "IIIHHHIII",
            "X N   N X",
            "I N   N I",
            "X N   N X",
            "RNN O NNR",
            "X N   N X",
            "I N   N I",
            "X N   N X",
            "IIIXIXIII"
        ],
        "key": {
            "X": {"newItemName": "avaritia:crystal_matrix_ingot"},
            "N": {"newItemName": "avaritia:neutronium_ingot"},
            "I": {"newItemName": "minecraft:iron_block"},
            "H": {"newItemName": "minecraft:hopper"},
            "R": {"newItemName": "minecraft:redstone_block"},
            "O": {"newItemName": "avaritia:neutronium_block"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:neutronium_compressor"
        }
    },
    # 世界崩解之镐
    {
        "pattern": [
            " IIIIIII ",
            "IIIICIIII",
            "II  N  II",
            "    N    ",
            "    N    ",
            "    N    ",
            "    N    ",
            "    N    ",
            "    N    "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "C": {"newItemName": "avaritia:crystal_matrix"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_pickaxe"
        }
    },
    # 无尽锭
    {
        "pattern": [
            "NNNNNNNNN",
            "NCXXCXXCN",
            "NXCCXCCXN",
            "NCXXCXXCN",
            "NNNNNNNNN"
        ],
        "key": {
            "C": {"newItemName": "avaritia:crystal_matrix_ingot"},
            "N": {"newItemName": "avaritia:neutronium_ingot"},
            "X": {"newItemName": "avaritia:infinity_catalyst"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_ingot"
        }
    },
    # 无尽之剑
    {
        "pattern": [
            "       II",
            "      III",
            "     III ",
            "    III  ",
            " C III   ",
            "  CII    ",
            "  NC     ",
            " N  C    ",
            "X        "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "X": {"newItemName": "avaritia:infinity_catalyst"},
            "C": {"newItemName": "avaritia:crystal_matrix_ingot"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_sword"
        }
    },
    # 无尽之铲
    {
        "pattern": [
            "      III",
            "     IIXI",
            "      III",
            "     N I ",
            "    N    ",
            "   N     ",
            "  N      ",
            " N       ",
            "N        "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "X": {"newItemName": "avaritia:infinity_block"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_shovel"
        }
    },
    # 无尽锄头
    {
        "pattern": [
            "     N ",
            " IIIIII",
            "IIIIIII",
            "I    II",
            "     N ",
            "     N ",
            "     N ",
            "     N ",
            "     N "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_hoe"
        }
    },
    # 无尽之斧
    {
        "pattern": [
            " I   ",
            "IIIII",
            "IIII ",
            " IN  ",
            "  N  ",
            "  N  ",
            "  N  ",
            "  N  ",
            "  N  "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_axe"
        }
    },
    # 无尽之弓
    {
        "pattern": [
            "   II",
            "  I S",
            " I  S",
            "I   S",
            "X   S",
            "I   S",
            " I  S",
            "  I S",
            "   II"
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "X": {"newItemName": "avaritia:crystal_matrix"},
            "S": {"newItemName": "minecraft:string"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_bow"
        }
    },
    # 无尽胸甲
    {
        "pattern": [
            " NN   NN ",
            "NNN   NNN",
            "NNN   NNN",
            " NIIIIIN ",
            " NIIXIIN ",
            " NIIIIIN ",
            " NIIIIIN ",
            " NIIIIIN ",
            "  NNNNN  "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "X": {"newItemName": "avaritia:crystal_matrix"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_chestplate"
        }
    },
    # 无尽头盔
    {
        "pattern": [
            "  NNNNN  ",
            " NIIIIIN ",
            " N XIX N ",
            " NIIIIIN ",
            " NIIIIIN ",
            " NI I IN "
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "X": {"newItemName": "avaritia:infinity_catalyst"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_helmet"
        }
    },
    # 无尽护腿
    {
        "pattern": [
            "NNNNNNNNN",
            "NIIIXIIIN",
            "NINNXNNIN",
            "NIN   NIN",
            "NCN   NCN",
            "NIN   NIN",
            "NIN   NIN",
            "NIN   NIN",
            "NNN   NNN"
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "X": {"newItemName": "avaritia:infinity_catalyst"},
            "C": {"newItemName": "avaritia:crystal_matrix"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_leggings"
        }
    },
    # 无尽靴子
    {
        "pattern": [
            " NNN NNN ",
            " NIN NIN ",
            " NIN NIN ",
            "NNIN NINN",
            "NIIN NIIN",
            "NNNN NNNN"
        ],
        "key": {
            "I": {"newItemName": "avaritia:infinity_ingot"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_boots"
        }
    },
    # 炽焰之啄颅剑
    {
        "pattern": [
            "       IX",
            "      IXI",
            "     IXI ",
            "    IXI  ",
            " B IXI   ",
            "  BXI    ",
            "  WB     ",
            " W  B    ",
            "D        "
        ],
        "key": {
            "I": {"newItemName": "avaritia:crystal_matrix_ingot"},
            "X": {"newItemName": "minecraft:blaze_powder"},
            "B": {"newItemName": "minecraft:bone"},
            "D": {"newItemName": "minecraft:nether_star"},
            "W": {"tags": {"wood"}}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:fiery_sword"
        }
    },
    # 终望珍珠
    {
        "pattern": [
            "   EEE   ",
            " EEPPPEE ",
            " EPPPPPE ",
            "EPPPNPPPE",
            "EPPNSNPPE",
            "EPPPNPPPE",
            " EPPPPPE ",
            " EEPPPEE ",
            "   EEE   "
        ],
        "key": {
            "E": {"newItemName": "minecraft:end_stone"},
            "P": {"newItemName": "minecraft:ender_pearl"},
            "S": {"newItemName": "minecraft:nether_star"},
            "N": {"newItemName": "avaritia:neutronium_ingot"}
        },
        "result": {
            "count": 1,
            "newItemName": "avaritia:endest_pearl"
        }
    },
    # 无尽奇点 (无序)
    {
        "ingredients":[
            {
                "count": 1,
                "newItemName": "avaritia:amethyst_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:copper_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:diamond_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:emerald_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:gold_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:iron_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:lapis_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:netherite_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:quartz_singularity"
            },
            {
                "count": 1,
                "newItemName": "avaritia:redstone_singularity"
            }
        ],
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_singularity"
        }
    },
    # 无尽催化剂 (无序)
    {
        "ingredients":[
            {
                "count": 1,
                "newItemName": "avaritia:diamond_lattice"
            },
            {
                "count": 1,
                "newItemName": "avaritia:crystal_matrix_ingot"
            },
            {
                "count": 1,
                "newItemName": "avaritia:neutron_pile"
            },
            {
                "count": 1,
                "newItemName": "avaritia:neutron_nugget"
            },
            {
                "count": 1,
                "newItemName": "avaritia:neutronium_ingot"
            },
            {
                "count": 1,
                "newItemName": "avaritia:record_fragment"
            },
            {
                "count": 1,
                "newItemName": "avaritia:ultimate_stew"
            },
            {
                "count": 1,
                "newItemName": "avaritia:cosmic_meatballs"
            },
            {
                "count": 1,
                "newItemName": "avaritia:endest_pearl"
            },
            {
                "count": 1,
                "newItemName": "avaritia:infinity_singularity"
            }
        ],
        "result": {
            "count": 1,
            "newItemName": "avaritia:infinity_catalyst"
        }
    },
    # 终极炖菜 (无序)
    {
        "ingredients": [
            {
                "count": 2,
                "newItemName": "minecraft:wheat"
            },
            {
                "count": 2,
                "newItemName": "minecraft:carrot"
            },
            {
                "count": 2,
                "newItemName": "minecraft:potato"
            },
            {
                "count": 2,
                "newItemName": "minecraft:beetroot"
            },
            {
                "count": 2,
                "newItemName": "minecraft:apple"
            },
            {
                "count": 2,
                "newItemName": "minecraft:melon_block"
            },
            {
                "count": 2,
                "newItemName": "minecraft:pumpkin"
            },
            {
                "count": 2,
                "newItemName": "minecraft:cactus"
            },
            {
                "count": 2,
                "newItemName": "minecraft:red_mushroom"
            },
             {
                "count": 2,
                "newItemName": "minecraft:brown_mushroom"
            },
            {
                "count": 1,
                "newItemName": "avaritia:neutron_pile"
            }
        ],
        "result": {
            "count": 1,
            "newItemName": "avaritia:ultimate_stew"
        }
    },
    # 宇宙肉丸 (无序)
    {
        "ingredients":[
            {
                "count": 2,
                "newItemName": "minecraft:cod"
            },
            {
                "count": 2,
                "newItemName": "minecraft:salmon"
            },
            {
                "count": 2,
                "newItemName": "minecraft:porkchop"
            },
            {
                "count": 2,
                "newItemName": "minecraft:rabbit"
            },
            {
                "count": 2,
                "newItemName": "minecraft:chicken"
            },
            {
                "count": 2,
                "newItemName": "minecraft:beef"
            },
            {
                "count": 2,
                "newItemName": "minecraft:mutton"
            },
            {
                "count": 1,
                "newItemName": "avaritia:neutron_pile"
            }
        ],
        "result": {
            "count": 1,
            "newItemName": "avaritia:cosmic_meatballs"
        }
    },
]