### 2018.11.13
- 编写部分Adb shell模块函数
- 完成获取安卓设备模块(/public/common/get_devices.py)

```text
递归遍历device.yaml文件, 封装appium_server模块,自动开启
多个appium服务,封装driver,多线程运行,为后期多设备平行测试
做铺垫.明日编写用例运行相关模块,并且能在单台设备上运行.Json
文件用例。
```

### 2018.11.12
- 完成移动端页面操作基类(/public/base/keywords.py)
- 开始编写Adb shell封装成模块

```text
先前说过项目将使用JSON格式进行用例管理,但今天下班路上。
突然想到万一有人不喜欢用JSON或编写不规范怎么办？(就算
我将用例编写规则在说明文档进行详细叙述,但总有万一)。因此
在Web框架的启发下,是否可以在一个指定的模块中例如：
JsonCaseModules.py中进行编写相关用例模型。
构思中的示例（真正实现未必如此）：
    class Login(object):
        test_name = 'login'
        test_id = 'login001'
        action = 'click'
        location = 'kw'
        assert = 'hello world!'
写完用例模型，在命令行执行例如：
python manage.py createJsonCase
在指定用例目录下根据类名生成对应Json文件, 并根据属性生成
对应的事件。由于业务繁忙先记录下这个idea.后续实现。
```


### 2018.11.11
- 构思项目结构 & 创建项目
- 使用Json格式管理测试用例
