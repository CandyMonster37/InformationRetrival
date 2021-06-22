# InformationRetrival
Course final project for Information Retrival (IR).  信息检索的期末课程作业。

做任何想做的工作，与信息检索相关即可。

## 英文文本信息检索系统

​        一款针对英文文本的信息检索系统。

## 目前实现的功能：

1. 自动获取某英文小说网站的文本作为数据源；

2. 建立查询表；

3. 计算指定词的TF-IDF值；

4. 进行布尔查询；

5. 进行通配符查询；

6. 进行短语查询。

所有功能都可以通过--hit参数限制输出的结果数量。

## 可使用的命令

### ？ / help

输出提示信息。

### help [command]

获取指定命令的详细介绍。如，`help get_data`可以获得关于`get_data`命令的详细介绍。

### get_data [dir] --wait --numbers

自动获取文本。

输入命令`get_data ./data –numbers=17 –wait=0.5`可以从内置的某英文小说网站获取17篇短篇小说并保存到./data目录下。每获取一个链接，爬虫都会等待0.5s，以防止被服务器封停。

### build_table [dir] --language

建立查询表。

输入命令`build_table ./data`可以从./data目录下读取文件并建立查询表。

### show_index [word]

查询指定词的VB码。

输入命令`show_index we`可以查看单词we的VB压缩码。

### boolean_query [options] --hit

布尔查询。

输入命令`boolean_query (we OR you) AND (he OR she) AND NOT( kill OR dead)`可以查看包含we或者you、且包含he或者she、且不包含kill或者dead的文档。

输入命令`boolean_query (we OR you) AND (he OR she) AND NOT( kill OR dead) –hits=5`限制结果的展示数量为最多5篇。

### wildcard_query [target] --hit

通配符查询。

输入命令`wildcard_query a*e`可以查看包含以a开头以e结尾的单词的文档。

输入命令`wildcard_query a*ose --hits=20`就可以显示包含a*ose单词的前20份结果。

### phrase_query [phrase] --hit

短语查询。

输入`phrase_query New York`可以查看包含New York的文档及摘要信息。

输入命令`phrase_query I loved her --hits=3`可以显示最多3篇包含短语I loved her的文档。

## 目前存在的问题

1. 不支持对单个词的查询。这个是我忘了做了，其实很简单，只需要对倒排索引表查询指定词，该次在倒排索引表中的值就是包含该词的文档ID。
2. 对于不存在的词或者短语，没有相应的处理方式。理论上来讲应该根据编辑距离推荐近似词作为结果，最次也要提示用户没有找到结果，时间不够了，我就没做。
3. 只针对英文文本。其实我一开始想做对中文文本的支持来着，jieba库都导入了，但是时间真的不够用了，考虑到中文文本对词的处理稍微麻烦一点，就将其搁置了。

## 配置环境

见`requirement.txt`。

## 其他的话

点个fork或者star呗。
