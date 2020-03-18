# Property Graphs Lab Assignment

## A.1 Modeling
![ModelDesign](PartA.1_LiJin.png)
The base of the graph is followed by the default setting from `dblp`. Based on the query in Part B, general `Conference` nodes are derived from `Proceedings` where the edge `contains` has property of each `volume` and `year`. `confarticle` is derived from `inproceedings` with the same properties, but only cited works are extracted. Also, `citing` is created from `cite` to outperform the 'number of citation' aggregation.

## A.2 Instantiating/Loading
The original database is parsed through the     `dblp-to-csv` tool available in [GitHub](https://github.com/ThomHurks/dblp-to-csv). When passing the `--neo4j` option, the type annotations will be Neo4j compatible, and the tool generates a shell script called `neo4j_import.sh` that can be run to import the generated CSV files into a Neo4j graph database using the `neo4j-admin import` bulk importer tool.
Further changes are performed in Cypher and saved as `PartA.2_LiJin`.

## A.3 Evolving the graph
![ModelDesign](PartA.3.jpeg)
We create the `reviewers` property for each article/inproceeding based on the community of the corresponding journal/conference (derived from PartB.3). Random 3 reviewers are assigned to each paper.

For the `affiliation`, given the missing raw data, it is randomly assigned for each author a specific university. 

## B Querying
### 1. H-index

```
MATCH ()-[c:citing]->(p:article)-[:authored_by]->(a:author)
WITH a, p, count(c) as numCit
ORDER BY numCit
WITH a, collect(numCit) AS NumCit
WITH a, NumCit, range(0, size(NumCit)) AS is
UNWIND is AS i
WITH a, NumCit[i] as numCit, i
WHERE (i+1) < numCit
RETURN distinct a.author as authorName, max(i) as hIndex
ORDER BY hIndex DESC
```
Testing result:

![Query1](TestingResult/Query_1.png)

### 2. Top 3 for each conference
```
MATCH ()-[c:citing]->(p:confarticle)-[con:published_in]->(conf:conference)
with distinct p, count(c) as citnum, conf ORDER BY citnum DESC
with conf, collect(p.title) as array_1, collect(citnum) as array_2
return distinct conf.booktitle, array_1[..3], array_2[..3]
```
Testing result:

![Query1](TestingResult/Query_2.png)

### 3. Community for each Conference

```
MATCH(conf:proceedings)
WITH distinct conf.booktitle as confTitle #LIMIT 25
MATCH (inp:inproceedings{booktitle:confTitle})-[:authored_by]->(a:author)
WITH distinct a, collect(distinct inp.key) as inps, confTitle
WHERE size(inps)>=4
RETURN confTitle, collect(a.author)
```

Testing result:

![Query1](TestingResult/Query_3.png)

### 4. Impact factor of journals

```
MATCH ()-[c:citing]->(a:article)
with a, count(c) as citnum
MATCH (j:journal)<-[pi:published_in]-(a:article)
with j, a.year as year, count(pi) as pnum, sum(citnum) as cnum
with j, collect(year) as Year, collect(pnum) as Pnum, collect(cnum) as Cnum
with j, Year, Pnum, Cnum, range(0, size(Year)-1) AS is
UNWIND is AS i
return j.journal, Year[i] as year, Cnum[i]/Pnum[i] as impact
order by impact desc, j.journal, year
```

Testing result:

![Query1](TestingResult/Query_4.png)

## C Graph algorithms

## D Recommender
### 1 Define research community
The `keywords` are derived from the paper title (tokenize & remove stop words). 