## 项目结构描述

- 依赖第三方库```pyjce2```
  ```pytea2```
  
- ```pymirai.binary```:存放协议所需的jce结构体和tlv读写相关模块

- ```pymirai.client```:bot自身相关,提供相对低级的api

- ```pymirai.net```:网络相关 **未来可能重构掉这个**

- ```pymirai.protocol```:存希强协议需要的pb文件和tlv文件

- ```pymirai.util```:项目相关的工具,比如解析和打包字节流,模拟QQ客户端进行http通信的工具