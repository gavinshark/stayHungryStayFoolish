## application Binary interface 二进制兼容性

### 何为二进制兼容性

大型项目通常由多人开发不同的项目，被集成模块以dll发布。

发布新被集成模块dll后，原有集成该dll的exe或者dll，在不重新编译的情况下，直接更新dll文件，仍能正常工作，即二进制兼容。

**这里只讨论非loadlibrary方式下的dll函数的ABI**

### dll加载时如何判定地址

To be continued.

### 如何保证C++的二进制兼容性

#### 不会影响二进制兼容性的

1. 增加extern C函数，无论是在原有函数前还是函数后
2. 增加Class 中普通函数，无论是在原有函数前还是函数后

#### 会影响二进制兼容性的

普通的：
1. 修改参数传递方式，如stdcal 和 cdecl。
2. 修改了struct和class的内存布局，通过偏移量访问数据成员
3. name mangling，如修改了传参列表

和C++相关的：
1. 使用指针+虚函数方式，序函数按照虚表序号找的，如果原有虚函数前加新的虚函数。集成方可能会尝试调用新的虚函数
2. 函数的访问属性发生变化，原有public改成private，其实通过name mangling实现，原有
3. RTTI和异常处理（未研究）

参考[陈硕的Blog C++ 工程实践(4)：二进制兼容性](http://www.cppblog.com/Solstice/archive/2011/03/09/141401.aspx)

### 查看工具

#### 1. dependencywalker(depends.exe)

主要对比为解析前的Function Name和旧版本dll是否一致。

当然也可以通过该工具查看解析后用户友好的Function name。

[dependencywalker官网](http://www.dependencywalker.com/)

#### 2. dumpbin

命令行方式简单查看exe导入和dll导出的符号