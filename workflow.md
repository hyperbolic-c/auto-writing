基于claude code中现有的plugins开发一个自动学术写作的plugins
1. 启动 /superpowers:brainstorm 根据要求制定计划，原插件实现在 @superpowers 文件夹
2. zotero-mcp实现对应的参考文献检索查找，原mcp实现在 @zotero-mcp 文件夹。由于zotero mcp服务有两个版本，其一为@zotero-mcp 文件夹，其二为@cookjohn-zotero-mcp 文件夹，要适配两个服务。
3. MinerU将对应的参考文献解析为md文件，调用api例子位于 @MinerU.py 文件
4. 读取参考文献作为上下文信息
5. 根据要求利用 /scientific-skills 开始撰写，原插件实现位于 @claude-scientific-skills 文件夹

# v1.1.0
1. 启动setup后要运行python进行配置，能否改为利用终端命令进行配置？
2. 增加是否获取参考文献的全文的配置选项？在需求文档中填写完整题目的参考文献就获取全文，其他利用语义进行相近主题搜索的文献就仅获取摘要作为参考，或者通过算法来决定是否获取全文。