import easygui

import boolRetrieval

bool = boolRetrieval.BoolRetrieval()
easygui.msgbox(msg="请点击输入按钮，输入您要检索的内容!", title="基于倒排索引和布尔检索的信息检索系统",
               ok_button="输入")
flag = easygui.choicebox(msg="是否需要进行拼写纠正?", title="基于倒排索引和布尔检索的信息检索系统",
                         choices=['需要', '不需要'])
query = easygui.enterbox(msg="请输入您需要检索的内容（布尔检索表达式）!", title="基于倒排索引和布尔检索的信息检索系统",
                         default="例如：american AND china", strip=False)
answer = easygui.textbox(msg="输出对应文档如下：", text=bool.answer(query.split(), flag),
                         title="基于倒排索引和布尔检索的信息检索系统", codebox=0)
