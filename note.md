#随手记录工作中的心得,小技巧
---
###如何在控制台，用up按钮检索相近命令

编辑(没有则新建) ~/.inputrc ，写入如下内容，然后重新启动控制台。
```
"\e[A": history-search-backward
"\e[B": history-search-forward
set show-all-if-ambiguous on
set completion-ignore-case on
```
---

###为adb添加设备权限
编辑(没有则新建) /etc/udev/rules.d/51-android.rules ，写入如下内容，然后重新插拔usb接口。
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0e8d", ATTRS{idProduct}=="201c",MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="05c6", ATTRS{idProduct}=="90b8",MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="18d1", ATTRS{idProduct}=="4ee7",MODE="0666"
```
idVendor和idProduct的值可通过lsusb命令获取
如果设备在adb root后在lsusb列表中消失,关闭再打开手机上的usb调试开关

---

###解析elf文件进行debug
程序有时会启动时直接崩溃,不输出任何log
可能的原因是有未定义的函数声明运行时在动态库中未找到它的实现
通过解析程序编译时的中间产物elf文件
```
readelf -d test_sample.elf
```
可以得到程序所引用的动态库名称
```
nm test_sample.elf | grep "U "
```
可以得到所有未定义的函数列表
```
nm -D lib_test.so
```
可以得到动态库中的所有函数的列表
如果有未定义的函数在动态库中没有实现,则程序启动时会崩溃

---
