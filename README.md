# DNASpider

项目说明：
1. 爬虫结构，一共六个文件
queryFile.py 批量查询基因变异，调用了query.py
-- query.py 单个基因变异查询,调用了以下四个文件，分别实现4个网站的查询
---- gnomad.py 查询https://gnomad-sg.org
---- hotspot.py 查询https://www.cancerhotspots.org
---- tp53.py 查询TP53数据库 https://tp53.isb-cgc.org/search_somatic_mut
---- oncokb.py  查询OncoKB，https://www.oncokb.org/

2. gnomad.py 说明
gnomad-sg.org，采用了react技术，graphSQL
def queryGnomad (qStr, refeGenome, dataset)， 依次调用了下面3个方法，进行了三次查询。
-- def getEn () # 获取ensemble ID，以调用variant页面接口
-- def getV () # 获取variant_id
-- def getAf (variantId) # 获取东亚变异频率

3. hotspot.py 说明
cancerhotspots.org，其数据在自于  https://www.cancerhotspots.org/api/hotspots/single 接口，直接复制到了文件中，本地查询
def getSpot (qStr, refeGenome, dataset)， 依次调用了下面3个方法。

4. tp53.py 说明
TP53数据库 https://tp53.isb-cgc.org/search_somatic_mut
def getTAFunc (v) 取TA Class列的前十行数据去重。

5. oncokb.py  
查询OncoKB，https://www.oncokb.org/, 其接口查询时用了token令牌，所以需要先获取令牌。
def getOncokb (gene, variant)， 依次调用了以下4个方法
-- def getToken () 获取token令牌
-- def getGene (gene) 获取基因相关的信息
-- def getTheraps (gene) 获取治疗方法相关的信息
-- def getVariant (gene, variant) 获取变异相关的信息


输入数据：将查询的数据一行一个复制到input.txt
输出结果：result文件夹下的以时间命名的txt文件
运行：windows下：在双击运行play.bat， 或者在cmd 命令行界面下，在当前目录下执行 cmd.exe 命令： python queryFile.py
	Linux下：python3 queryFile.py

