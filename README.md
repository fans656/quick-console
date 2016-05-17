quick-console
=============
# 全局快捷控制台

![Screenshot](https://raw.githubusercontent.com/fans656/image-hosting/master/20140819201216.png)

按 Ctrl-; 呼出，键入自定义的命令，可以执行类似以下任务：
- 打开某个网页
- 启动某个程序
- 将当前日期放入剪贴板(e.g. 20140818010932 or 20140818 01:10:12)

之后想要添加的功能：
- 特殊快捷键，包括：
  - normal key modifier (e.g. aj{j}{a} -> a down j down j up a up)
  - ctrl modifier (e.g. Ctrl-;d -> Ctrl down ; down ; up d down d up)
- 命令参数 (e.g. new t.py -> 在当前 explorer 新建 t.py 文件)
- web search (包括 google, wiki, stackoverflow 等，支持 suggestion)
- intellisense (弹出选项使用快捷键选择，比如 jkl;)

# Environment
- Python >= 2.7.8
- PySide >= 1.2.2
- pyHook
