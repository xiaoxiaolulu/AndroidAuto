### Appium 常用Api总汇
[AppiumApi](https://blog.csdn.net/bear_w/article/details/50330565)

### Adb 常用命令
[AdbShell](https://blog.csdn.net/u010375364/article/details/52344120)

### 无线连接设备
```text
1. 指定端口         adb tcpip 5555
2. 查看设备网络ip    adb shell netcfg
3. 连接设备         adb connect 10.2.28.181:5555
4. 断开连接         adb disconnect 10.2.28.181:5555
```

### 设备集控了解
- 搭建stf+minicap实现安卓群控


### Appium环境搭建
- Jdk1.8.0
- Android-sdk
- Python3.6.3
- [Appium1.4.1](https://bitbucket.org/appium/appium.app/downloads/)
- [Node.js](https://nodejs.org/en/download/)
- Appium-Python-Client


### 禁止Unlock & Setting
```text
找到路径D:\Program Files (x86)\Appium\node_modules\appium\lib\devices\android (笔者的路径)
下面的android.js文件，并且注释调下图的几行代码
```
![Image text](https://images2017.cnblogs.com/blog/1081259/201708/1081259-20170814110652662-925097114.png)