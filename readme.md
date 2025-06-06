# 算法设计与分析

## 实验一：算法效率分析—排序与TopK问题

### 一、实验目的：
1.	掌握选择排序、冒泡排序、插入排序、合并排序、快速排序算法原理
2.	掌握不同排序算法时间效率的经验分析方法，验证理论分析与经验分析的一致性。
3.	求解TOP K问题，并分析比较不同算法效率。

### 二、实验内容：
1. 实现选择排序、冒泡排序、插入排序、合并排序、快速排序算法；
2. 以待排序数组的大小n为输入规模，固定n，随机产生20组测试样本，统计不同排序算法在20个样本上的平均运行时间；
3. 分别以n=10万, n=20万, n=30万, n=40万, n=50万等等（建议输入规模n可以直至极限），重复2的实验，画出不同排序算法在20个随机样本的平均运行时间与输入规模n的关系，如下图1所示，注意横坐标要均匀。
 
<center>
<img src=".\img\lab1.png" alt="图1. 时间效率与输入规模n的关系图" style="zoom:100%;" />

图1. 时间效率与输入规模n的关系图

</center>


1. 画出理论效率分析的曲线和实测的效率曲线，注意：由于实测效率是运行时间，而理论效率是基本操作的执行次数，两者需要进行对应关系调整。调整思路举例：以输入规模为10万的数据运行时间为基准点，计算输入规模为其他值的理论运行时间，画出不同规模数据的理论运行时间曲线，并与实测的效率曲线进行比较。经验分析与理论分析是否一致？如果不一致，请解释存在的原因。
2. 现在有10亿的数据（每个数据四个字节），请快速挑选出最大的十个数，并在小规模数据上验证算法的正确性。


## 实验二：分治法——最近点对问题 

### 一、实验目的：
1. 掌握分治法思想。
2. 学会最近点对问题求解方法。

### 二、实验内容及环境：
实验内容：
1. 对于平面上给定的N个点，给出所有点对的最短距离，即，输入是平面上的N个点，输出是N点中具有最短距离的两点。
2. 要求随机生成N个点的平面坐标，应用蛮力法编程计算出所有点对的最短距离。
3. 要求随机生成N个点的平面坐标，应用分治法编程计算出所有点对的最短距离。
4. 分别对N=100000—1000000，统计算法运行时间，比较理论效率与实测效率的差异，同时对蛮力法和分治法的算法效率进行分析和比较。
5. 如果能将算法执行过程利用图形界面输出，可获加分。

## 实验三 回溯法——地图填色问题

### 一、实验目的：

1. 掌握回溯法算法设计思想。
2. 掌握地图填色问题的回溯法解法。

### 二、内容：

#### 背景知识：  
为地图或其他由不同区域组成的图形着色时，相邻国家/地区不能使用相同的颜色。 我们可能还想使用尽可能少的不同颜色进行填涂。一些简单的“地图”（例如棋盘）仅需要两种颜色（黑白），但是大多数复杂的地图需要更多颜色。   

每张地图包含四个相互连接的国家时，它们至少需要四种颜色。1852年，植物学专业的学生弗朗西斯·古思里（Francis Guthrie）于1852年首次提出“四色问题”。他观察到四种颜色似乎足以满足他尝试的任何地图填色问题，但他无法找到适用于所有地图的证明。这个问题被称为四色问题。长期以来，数学家无法证明四种颜色就够了，或者无法找到需要四种以上颜色的地图。直到1976年德国数学家沃尔夫冈·哈肯（Wolfgang Haken）（生于1928年）和肯尼斯·阿佩尔（Kenneth Appel，1932年-2013年）使用计算机证明了四色定理，他们将无数种可能的地图缩减为1936种特殊情况，每种情况都由一台计算机进行了总计超过1000个小时的检查。  

他们因此工作获得了美国数学学会富尔克森奖。在1990年，哈肯（Haken）成为伊利诺伊大学（University of Illinois）高级研究中心的成员，他现在是该大学的名誉教授。  

四色定理是第一个使用计算机证明的著名数学定理，此后变得越来越普遍，争议也越来越小 更快的计算机和更高效的算法意味着今天您可以在几个小时内在笔记本电脑上证明四种颜色定理。  

#### 问题描述：  
我们可以将地图转换为平面图，每个地区变成一个节点，相邻地区用边连接，我们要为这个图形的顶点着色，并且两个顶点通过边连接时必须具有不同的颜色。附件是给出的地图数据，请针对三个地图数据尝试分别使用5个（le450_5a），15个（le450_15b），25个（le450_25a）颜色为地图着色。

### 三、实验要求

1. 对下面这个小规模数据，利用四色填色测试算法的正确性；

<div align="center">
<img src=".\img\lab3.png" alt="图2. 小规模数据" style="zoom:100%;" />
<br>图2. 小规模数据
</div>

2. 对附件中给定的地图数据填涂；
3. 随机产生不同规模的图，分析算法效率与图规模的关系（四色）。
