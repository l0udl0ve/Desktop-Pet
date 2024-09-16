<div align="center" style="text-align:center">
   <h1> Desktop Pet </h1>
   <p>
    Desktop Pet | Windows桌宠 <br>
      <code><b> ver 1.0.0 </b></code>
   </p>
   <p>
      <img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/l0udl0ve/Desktop-Pet?label=Python">
      <img alt="GitHub License" src="https://img.shields.io/github/license/l0udl0ve/Desktop-Pet?label=License"/>
   </p>
</div>


## **概述**
本项目是一个基于python标准库<font color="#00b0f0">tkinter</font>为<font color="#ff0000">Windows操作系统</font>开发的一个罗小黑桌宠，旨在更为便捷地对用户编写的python脚本进行管理。支持自编写插件。

## **功能**
### 1、桌宠自由拖动，眼动跟随光标
![](https://raw.githubusercontent.com/l0udl0ve/imageWare/master/1.gif)

### 2、拖拽事件捕捉，趣味文件回收
![](https://raw.githubusercontent.com/l0udl0ve/imageWare/master/2.gif)

### 3、窗口标题隐藏，最小化到托盘
![](https://raw.githubusercontent.com/l0udl0ve/imageWare/master/3.gif)

### 4、双击菜单打开，插件动态加载
![](https://raw.githubusercontent.com/l0udl0ve/imageWare/master/4.gif)

### 5、开机自动启动，一键应用安装

## **使用**
直接下载对应的[**release版本**](https://github.com/l0udl0ve/Desktop-Pet/releases)的Installer.exe即可安装，或者使用pyinstaller等工具进行源码编译。安装完毕之后即可使用。

## **插件**
本项目支持运行python编写的脚本文件，仅当本机拥有python环境才能使用import调用库。插件应放置于plugin文件下，可包含icon.png(图标文件)和多个依赖python脚本文件，必须包含主逻辑文件main.py。
一个合法的插件文件夹结构如下：
```
./Plugin
	├─插件名称1 
	|  ├─main.py
	|  ├─（依赖.py）     
	|  └─（icon.png）
	├─插件名称2
	...
```
其中，主逻辑文件必须包含具有run方法的Plugin类，便于项目可执行文件调用。详情参照插件Template。
```python
class Plugin:  
    def __init__(self):  
        pass  
  
    def run(self):  
        print('This is a plugin template!')  
  
  
if __name__ == '__main__':  
    plugin = Plugin()  
    plugin.run()
```

## **其他**
本项目遵循MIT License 3.0许可证，欢迎大家进行二次开发、制作插件和提交Issure。本人水平有限，希望大家批评指正不足。
