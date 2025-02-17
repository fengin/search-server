# Web Search API

## 一、API简介

从全网搜索任何网页信息和网页链接，结果准确、摘要完整，更适合AI使用。

可配置搜索时间范围、是否显示摘要，支持按分页获取更多结果。

## 二、搜索结果

包括网页、图片、Response格式兼容Bing Search API。

- 网页包括name、url、snippet、summary、siteName、siteIcon等信息

![](https://aq6ky2b8nql.feishu.cn/space/api/box/stream/download/asynccode/?code=YTg1YjdmNDA4OGY1MDAzNzMwMzVjYzJiNzg0NjgwMDlfdVVsbklmSDB5cFB3OHNReHQ3NjU5N044MGZ3Q0JxRHNfVG9rZW46TUNlbGJvR3Q0b2pqcUZ4dHVHRWNUZGRQbkhiXzE3Mzk3MTMwODU6MTczOTcxNjY4NV9WNA)

- 图片包括 contentUrl、hostPageUrl、width、height等信息

## 三、API接口

> 接口域名：https://api.bochaai.com
> 
> EndPoint：https://api.bochaai.com/v1/web-search

## 四、调用方式

#### 请求方式

POST

#### 请求参数

##### 请求头

|               |                  |                                                                                         |
| ------------- | ---------------- | --------------------------------------------------------------------------------------- |
| **参数**        | **取值**           | **说明**                                                                                  |
| Authorization | Bearer {API KEY} | 鉴权参数，示例：Bearer xxxxxx，API KEY请先前往博查AI开放平台（https://open.bochaai.com）> **API KEY 管理**中获取。 |
| Content-Type  | application/json | 解释请求正文的方式。                                                                              |

##### 请求体

|           |         |        |                                                                                                |
| --------- | ------- | ------ | ---------------------------------------------------------------------------------------------- |
| **参数**    | **类型**  | **必填** | **说明**                                                                                         |
| query     | String  | 是      | 用户的搜索词。                                                                                        |
| freshness | String  | 否      | 搜索指定时间范围内的网页。可填值：- oneDay，一天内  - oneWeek，一周内  - oneMonth，一个月内  - oneYear，一年内  - noLimit，不限（默认） |
| summary   | Boolean | 否      | 是否显示文本摘要。可填值：- true，显示- false，不显示（默认）                                                          |
| count     | Int     | 否      | 返回结果的条数（实际返回结果数量可能会小于count指定的数量）。- 可填范围：1-10- 默认为10                                            |
| page      | Int     | 否      | 页码，默认值为 1                                                                                      |

#### 响应内容

##### 响应定义

###### SearchData

- `_type`: "SearchResponse" 搜索的类型

- `queryContext`: WebSearchQueryContext

- `webPages`: WebSearchWebPages 搜索的网页结果

- `images`: WebSearchImages 搜索的图片结果

- `videos`: WebSearchVideos 搜索的视频结果

###### WebSearchQueryContext

- `originalQuery`: String 原始的搜索关键字

###### WebSearchWebPages

- `webSearchUrl`: String

- `totalEstimatedMatches`: int 搜索匹配的网页总数

- `value`: List<WebPageValue>

- `someResultsRemoved`: boolean 结果中是否有被安全过滤

###### WebPageValue

- `id`: String 网页的排序ID

- `name`: String 网页的标题

- `url`: String 网页的URL

- `displayUrl`: String 网页的展示URL（url decode后的格式）

- `snippet`: String 网页内容的简短描述

- `summary`: String 网页内容的文本摘要，当请求参数中 summary 为 true 时显示此属性

- `siteName`: String 网页的网站名称

- `siteIcon`: String 网页的网站图标

- `dateLastCrawled`: String 网页的`发布时间`（此处其实是发布时间，名字起为LastCrawled是兼容性适配）

- `cachedPageUrl`: String 网页的缓存页面URL

- `language`: String 网页的语言

- `isFamilyFriendly`: boolean 是否为家庭友好的页面

- `isNavigational`: boolean 是否为导航性页面

###### WebSearchImages

- `id`: String

- `readLink`: String

- `webSearchUrl`: String

- `isFamilyFriendly`: boolean

- `value`: List<ImageValue>

###### WebSearchVideos

- `id`: String

- `readLink`: String

- `webSearchUrl`: String

- `isFamilyFriendly`: boolean

- `scenario`: String

- `value`: List<VideoValue>

###### ImageValue

- `webSearchUrl`: String

- `name`: String

- `thumbnailUrl`: String

- `datePublished`: String

- `contentUrl`: String

- `hostPageUrl`: String

- `contentSize`: String

- `encodingFormat`: String

- `hostPageDisplayUrl`: String

- `width`: int

- `height`: int

- `thumbnail`: Thumbnail

###### VideoValue

- `webSearchUrl`: String

- `name`: String

- `description`: String

- `thumbnailUrl`: String

- `publisher`: List<Publisher>

- `creator`: Creator

- `contentUrl`: String

- `hostPageUrl`: String

- `encodingFormat`: String

- `hostPageDisplayUrl`: String

- `width`: int

- `height`: int

- `duration`: String

- `motionThumbnailUrl`: String

- `embedHtml`: String

- `allowHttpsEmbed`: boolean

- `viewCount`: int

- `thumbnail`: Thumbnail

- `allowMobileEmbed`: boolean

- `isSuperfresh`: boolean

- `datePublished`: String

###### Creator

- `name`: String

###### Publisher

- `name`: String

###### Thumbnail

- `height`: int

- `width`: int

###### RankingResponse

- `mainline`: Mainline

###### Mainline

- `items`: List<MainlineItem>

###### MainlineItem

- `answerType`: String

- `value`: MainlineItemValue

###### MainlineItemValue

- `id`: String

#### 调用示例

##### 请求内容

body：

```JSON
{
    "query": "阿里巴巴2024年的esg报告",
    "freshness": "noLimit",
    "summary": false, // 当设置为 true 的时候显示摘要
    "count": 10
}
```

##### 响应内容

```JSON
{
    "code": 200,
    "log_id": "d71841ad20095f61",
    "msg": null,
    "data": {
        "_type": "SearchResponse",
        "queryContext": {
            "originalQuery": "阿里巴巴2024年的esg报告"
        },
        "webPages": {
            "webSearchUrl": "",
            "totalEstimatedMatches": 8912791,
            "value": [
                {
                    "id": null,
                    "name": "阿里巴巴发布2024年ESG报告　持续推进减碳与数字化普惠",
                    "url": "https://www.alibabagroup.com/document-1752073403914780672",
                    "displayUrl": "https://www.alibabagroup.com/document-1752073403914780672",
                    "snippet": "阿里巴巴集团发布《2024财年环境、社会和治理（ESG）报告》（下称“报告”），详细分享过去一年在ESG各方面取得的进展。报告显示，阿里巴巴扎实推进减碳举措，全集团自身运营净碳排放和价值链碳...",
                    "siteName": "www.alibabagroup.com",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=https://www.alibabagroup.com/document-1752073403914780672",
                    "dateLastCrawled": "2024-07-22T00:00:00Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                },
                {
                    "id": null,
                    "name": "阿里巴巴发布2024年ESG报告: 保持前瞻、保持善意、保持务实",
                    "url": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "displayUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "snippet": "2024财年是阿里巴巴深化ESG治理的一年。在环境保护议题中，阿里巴巴以ESG治理机制的保障为基础，继续探索“在发展中减碳”，通过科技提升能源利用效率，使用可再生能源、带动生态伙伴参与等方式，推进绿色低碳高质量发展。数据显示，2024财年，阿里巴巴实现自身运营碳排放和价值链碳排放强度的“双降”目标；自身运营中的减排量达到232.0万吨，相比上一财年显著提升63.5%；清洁电力使用比例...",
                    "siteName": "大鱼号",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "dateLastCrawled": "2024-07-22T11:54:00Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                },
                {
                    "id": null,
                    "name": "186页|阿里巴巴：2024年环境、社会和治理（ESG）报告",
                    "url": "https://m.sohu.com/a/815036254_121819701/?pvid=000115_3w_a",
                    "displayUrl": "https://m.sohu.com/a/815036254_121819701/?pvid=000115_3w_a",
                    "snippet": "阿里巴巴集团的2024年环境、社会和治理（ESG）报告涵盖了公司在可持续发展方面的多项进展和成就。报告强调了公司的使命—“让天下没有难做的生意”，并通过技术创新和平台优势，支持中小微企...",
                    "siteName": "搜狐网",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=https://m.sohu.com/a/815036254_121819701/?pvid=000115_3w_a",
                    "dateLastCrawled": "2024-11-07T06:50:00Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                },
                {
                    "id": null,
                    "name": "阿里巴巴发布2024年ESG报告，阿里云数据中心清洁能源占比达56.0%",
                    "url": "http://tech.cnr.cn/techph/20240722/t20240722_526807992.shtml",
                    "displayUrl": "http://tech.cnr.cn/techph/20240722/t20240722_526807992.shtml",
                    "snippet": "阿里巴巴集团发布《环境、社会和治理报告（2024）》（以下简称“ESG报告”）提及，阿里巴巴自身运营减少碳排放量达232.0万吨，相比上一财年显著提升63.5%，其中，阿里云自建数据中心电力使用效率（PUE）从 2023财年1.215降至1.2...",
                    "siteName": "央广网",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=http://tech.cnr.cn/techph/20240722/t20240722_526807992.shtml",
                    "dateLastCrawled": "2024-07-22T17:54:38Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                },
                {
                    "id": null,
                    "name": "CSR周刊：京东物流携手野生救援共推环境保护，阿里巴巴发布2024年ESG报告引领可持续发展",
                    "url": "https://m.thepaper.cn/newsDetail_forward_28258281",
                    "displayUrl": "https://m.thepaper.cn/newsDetail_forward_28258281",
                    "snippet": "·阿里巴巴发布2024年ESG报告：保持前瞻、保持善意、保持务实·TT语音发布首份网络信息内容生态治理报告·Atlas Corp.发布《2023年可持续发展报告》·唯品会发布《环境、社会及治理报告（2023...",
                    "siteName": "澎拜",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=https://m.thepaper.cn/newsDetail_forward_28258281",
                    "dateLastCrawled": "2024-07-31T18:09:00Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                },
                {
                    "id": null,
                    "name": "阿里巴巴ESG报告：2024财年优酷无障碍剧场播放次数近百万",
                    "url": "https://t.m.youth.cn/transfer/index/url/news.youth.cn/yl/202407/t20240722_15396110.htm",
                    "displayUrl": "https://t.m.youth.cn/transfer/index/url/news.youth.cn/yl/202407/t20240722_15396110.htm",
                    "snippet": "阿里巴巴2024年ESG报告截图 无障碍电影在影片台词与声效间隙增加旁白解说，帮助视障观众了解剧情。过去一年，优酷无障碍剧场以科技推动无障碍观影建设，开发明星AI语音讲述包;在线上积极扩充片库，加快新热剧集、电影的更新速度;在线下进社区、进影院、进校园，为视障者带去不一样的观影体验。在取得诸多成绩此同时，越来越多的公益机构和爱心人士也加入其中，共同为中国无障碍事业发展贡献力量。前沿技术是优酷无障碍剧场发展的重要力量。两个月前，无障碍剧场上线演员胡歌的AI语音讲述包，这也是国内视听平台首次运...",
                    "siteName": "中国青年网",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=https://t.m.youth.cn/transfer/index/url/news.youth.cn/yl/202407/t20240722_15396110.htm",
                    "dateLastCrawled": "2024-07-22T18:48:00Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                },
                {
                    "id": null,
                    "name": "2024年阿里巴巴环境、社会和治理（ESG）报告-阿里巴巴",
                    "url": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "displayUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "snippet": "《2024年阿里巴巴环境、社会和治理（ESG）报告》由阿里巴巴集团发布，涵盖修复绿色星球、支持员工发展、服务可持续的美好生活、助力中小微企业高质量发展、助力提升社会包容和韧性、推动人人参与的公益、构建信任等方面内容。在修复绿色星球方面，阿里巴巴致力于实现碳中和，通过技术创新和管理优化降低自身运营和价值链的碳排放，同时带动和赋能平台生态减排；在支持员工发展方面，推动多元、平等和共融，吸引和保留人才，促进员工健康与活力；在...",
                    "siteName": "搜狐网",
                    "siteIcon": "https://th.bochaai.com/favicon?domain_url=https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "dateLastCrawled": "2024-07-26T12:33:00Z",
                    "cachedPageUrl": null,
                    "language": null,
                    "isFamilyFriendly": null,
                    "isNavigational": null
                }
            ],
            "someResultsRemoved": true
        },
        "images": {
            "id": null,
            "readLink": null,
            "webSearchUrl": null,
            "value": [
                {
                    "webSearchUrl": null,
                    "name": null,
                    "thumbnailUrl": "http://dayu-img.uc.cn/columbus/img/oc/1002/45628755e2db09ccf7e6ea3bf22ad2b0.jpg",
                    "datePublished": null,
                    "contentUrl": "http://dayu-img.uc.cn/columbus/img/oc/1002/45628755e2db09ccf7e6ea3bf22ad2b0.jpg",
                    "hostPageUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "contentSize": null,
                    "encodingFormat": null,
                    "hostPageDisplayUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "width": 553,
                    "height": 311,
                    "thumbnail": null
                },
                {
                    "webSearchUrl": null,
                    "name": null,
                    "thumbnailUrl": "http://image.uczzd.cn/15500294364735623464.jpg?id=0&from=export",
                    "datePublished": null,
                    "contentUrl": "http://image.uczzd.cn/15500294364735623464.jpg?id=0&from=export",
                    "hostPageUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "contentSize": null,
                    "encodingFormat": null,
                    "hostPageDisplayUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "width": 0,
                    "height": 0,
                    "thumbnail": null
                },
                {
                    "webSearchUrl": null,
                    "name": null,
                    "thumbnailUrl": "http://image.uczzd.cn/11174338884233139640.jpg?id=0&from=export",
                    "datePublished": null,
                    "contentUrl": "http://image.uczzd.cn/11174338884233139640.jpg?id=0&from=export",
                    "hostPageUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "contentSize": null,
                    "encodingFormat": null,
                    "hostPageDisplayUrl": "https://mparticle.uc.cn/article_org.html?uc_param_str=frdnsnpfvecpntnwprdssskt#!wm_cid=632457937121448960!!wm_id=b3f0578cbbd8434da8e437702e399f91",
                    "width": 0,
                    "height": 0,
                    "thumbnail": null
                },
                {
                    "webSearchUrl": null,
                    "name": null,
                    "thumbnailUrl": "http://q9.itc.cn/q_70/images01/20240726/3bbb91f089924a56b5abb95d0776fcc5.png",
                    "datePublished": null,
                    "contentUrl": "http://q9.itc.cn/q_70/images01/20240726/3bbb91f089924a56b5abb95d0776fcc5.png",
                    "hostPageUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "contentSize": null,
                    "encodingFormat": null,
                    "hostPageDisplayUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "width": 1285,
                    "height": 722,
                    "thumbnail": null
                },
                {
                    "webSearchUrl": null,
                    "name": null,
                    "thumbnailUrl": "http://q6.itc.cn/q_70/images01/20240726/490b71f2963b43588bb053f20bb4d775.png",
                    "datePublished": null,
                    "contentUrl": "http://q6.itc.cn/q_70/images01/20240726/490b71f2963b43588bb053f20bb4d775.png",
                    "hostPageUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "contentSize": null,
                    "encodingFormat": null,
                    "hostPageDisplayUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "width": 883,
                    "height": 374,
                    "thumbnail": null
                },
                {
                    "webSearchUrl": null,
                    "name": null,
                    "thumbnailUrl": "http://q7.itc.cn/q_70/images01/20240726/ee26d6fa8658472d8b4c5e7236b1640a.png",
                    "datePublished": null,
                    "contentUrl": "http://q7.itc.cn/q_70/images01/20240726/ee26d6fa8658472d8b4c5e7236b1640a.png",
                    "hostPageUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "contentSize": null,
                    "encodingFormat": null,
                    "hostPageDisplayUrl": "https://m.sohu.com/a/796245119_121713887/?pvid=000115_3w_a",
                    "width": 1285,
                    "height": 722,
                    "thumbnail": null
                }
            ],
            "isFamilyFriendly": null
        },
        "videos": null
    }
}
```

当前版本Web Search API 暂不返回 videos （返回结果为空）。如需视频搜索能力，请先使用 AI Search API中的视频结果。

# 五、Python SDK

```bash
import requests
import json

url = "https://api.bochaai.com/v1/web-search"

payload = json.dumps({
  "query": "天空为什么是蓝色的？",
  "summary": true,
  "count": 10,
  "page": 1
})

headers = {
  'Authorization': 'Bearer sk-********',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
```

# 六、OpenAPI Yaml配置文件

在各种 AI Agent 开发平台中，可以参考以下下的 yaml 文件，快速添加成自定义插件：

```yaml
openapi: 3.0.3
info:
  title: 博查AI搜索
  description: 从博查搜索网页信息和网页链接，搜索结果准确、完整，更适合AI使用。
  version: 1.0.0
servers:
  - url: https://api.bochaai.com/v1
paths:
  /web-search:
    post:
      summary: 从近百亿网页和生态内容源中搜索高质量世界知识，例如新闻、图片、百科、文库等。
      operationId: WebSearch
      requestBody:
        description: 请求参数
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: 搜索关键字或语句
                  example: "阿里巴巴2024年的ESG报告"
                summary:
                  type: boolean
                  description: 是否在搜索结果中包含摘要
                  example: true
                freshness:
                  type: string
                  description: 搜索指定时间范围内的网页（可选值 "noLimit"、"oneDay"、"oneWeek"、"oneMonth"、"oneYear"）
                  default: "noLimit"
                  enum:
                    - "noLimit"
                    - "oneDay"
                    - "oneWeek"
                    - "oneMonth"
                    - "oneYear"
                  example: "noLimit"
                count:
                  type: integer
                  description: 返回的搜索结果数量（1-8），默认为8
                  default: 10
                  minimum: 1
                  maximum: 10
                  example: 10
              required:
                - query
                - count
      responses:
        '200':
          description: 成功的搜索响应
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    description: 响应的状态码
                    example: 200
                  log_id:
                    type: string
                    description: 请求的唯一日志ID
                    example: "0d0eb34abc6eec9d"
                  msg:
                    type: string
                    nullable: true
                    description: 请求的消息提示（如果有的话）
                    example: null
                  data:
                    type: object
                    properties:
                      _type:
                        type: string
                        description: 搜索的类型
                        example: "SearchResponse"
                      queryContext:
                        type: object
                        properties:
                          originalQuery:
                            type: string
                            description: 原始的搜索关键字
                            example: "阿里巴巴2024年的ESG报告"
                      webPages:
                        type: object
                        properties:
                          webSearchUrl:
                            type: string
                            description: 网页搜索的URL
                            example: "https://bochaai.com/search?q=阿里巴巴2024年的ESG报告"
                          totalEstimatedMatches:
                            type: integer
                            description: 搜索匹配的网页总数
                            example: 1618000
                          value:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                  nullable: true
                                  description: 网页的排序ID
                                name:
                                  type: string
                                  description: 网页的标题
                                url:
                                  type: string
                                  description: 网页的URL
                                displayUrl:
                                  type: string
                                  description: 网页的展示URL
                                snippet:
                                  type: string
                                  description: 网页内容的简短描述
                                summary:
                                  type: string
                                  description: 网页内容的文本摘要
                                siteName:
                                  type: string
                                  description: 网页的网站名称
                                siteIcon:
                                  type: string
                                  description: 网页的网站图标
                                dateLastCrawled:
                                  type: string
                                  format: date-time
                                  description: 网页的收录时间或发布时间
                                cachedPageUrl:
                                  type: string
                                  nullable: true
                                  description: 网页的缓存页面URL
                                language:
                                  type: string
                                  nullable: true
                                  description: 网页的语言
                                isFamilyFriendly:
                                  type: boolean
                                  nullable: true
                                  description: 是否为家庭友好的页面
                                isNavigational:
                                  type: boolean
                                  nullable: true
                                  description: 是否为导航性页面
                      images:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                            description: 图片搜索结果的ID
                          webSearchUrl:
                            type: string
                            nullable: true
                            description: 图片搜索的URL
                          value:
                            type: array
                            items:
                              type: object
                              properties:
                                webSearchUrl:
                                  type: string
                                  nullable: true
                                  description: 图片搜索结果的URL
                                name:
                                  type: string
                                  nullable: true
                                  description: 图片的名称
                                thumbnailUrl:
                                  type: string
                                  description: 图像缩略图的URL
                                  example: "http://dayu-img.uc.cn/columbus/img/oc/1002/45628755e2db09ccf7e6ea3bf22ad2b0.jpg"
                                datePublished:
                                  type: string
                                  nullable: true
                                  description: 图像的发布日期
                                contentUrl:
                                  type: string
                                  description: 访问全尺寸图像的URL
                                  example: "http://dayu-img.uc.cn/columbus/img/oc/1002/45628755e2db09ccf7e6ea3bf22ad2b0.jpg"
                                hostPageUrl:
                                  type: string
                                  description: 图片所在网页的URL
                                  example: "http://dayu-img.uc.cn/columbus/img/oc/1002/45628755e2db09ccf7e6ea3bf22ad2b0.jpg"
                                contentSize:
                                  type: string
                                  nullable: true
                                  description: 图片内容的大小
                                encodingFormat:
                                  type: string
                                  nullable: true
                                  description: 图片的编码格式
                                hostPageDisplayUrl:
                                  type: string
                                  nullable: true
                                  description: 图片所在网页的显示URL
                                width:
                                  type: integer
                                  description: 图片的宽度
                                  example: 553
                                height:
                                  type: integer
                                  description: 图片的高度
                                  example: 311
                                thumbnail:
                                  type: string
                                  nullable: true
                                  description: 图片缩略图（如果有的话）
                      videos:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                            description: 视频搜索结果的ID
                          readLink:
                            type: string
                            nullable: true
                            description: 视频的读取链接
                          webSearchUrl:
                            type: string
                            nullable: true
                            description: 视频搜索的URL
                          isFamilyFriendly:
                            type: boolean
                            description: 是否为家庭友好的视频
                          scenario:
                            type: string
                            description: 视频的场景
                          value:
                            type: array
                            items:
                              type: object
                              properties:
                                webSearchUrl:
                                  type: string
                                  description: 视频搜索结果的URL
                                name:
                                  type: string
                                  description: 视频的名称
                                description:
                                  type: string
                                  description: 视频的描述
                                thumbnailUrl:
                                  type: string
                                  description: 视频的缩略图URL
                                publisher:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      name:
                                        type: string
                                        description: 发布者名称
                                creator:
                                  type: object
                                  properties:
                                    name:
                                      type: string
                                      description: 创作者名称
                                contentUrl:
                                  type: string
                                  description: 视频内容的URL
                                hostPageUrl:
                                  type: string
                                  description: 视频所在网页的URL
                                encodingFormat:
                                  type: string
                                  description: 视频编码格式
                                hostPageDisplayUrl:
                                  type: string
                                  description: 视频所在网页的显示URL
                                width:
                                  type: integer
                                  description: 视频的宽度
                                height:
                                  type: integer
                                  description: 视频的高度
                                duration:
                                  type: string
                                  description: 视频的长度
                                motionThumbnailUrl:
                                  type: string
                                  description: 动态缩略图的URL
                                embedHtml:
                                  type: string
                                  description: 用于嵌入视频的HTML代码
                                allowHttpsEmbed:
                                  type: boolean
                                  description: 是否允许HTTPS嵌入
                                viewCount:
                                  type: integer
                                  description: 视频的观看次数
                                thumbnail:
                                  type: object
                                  properties:
                                    height:
                                      type: integer
                                      description: 视频缩略图的高度
                                    width:
                                      type: integer
                                      description: 视频缩略图的宽度
                                allowMobileEmbed:
                                  type: boolean
                                  description: 是否允许移动端嵌入
                                isSuperfresh:
                                  type: boolean
                                  description: 是否为最新视频
                                datePublished:
                                  type: string
                                  description: 视频的发布日期
        '400':
          description: 请求参数错误
        '401':
          description: 未授权 - API 密钥无效或缺失
        '500':
          description: 搜索服务内部错误
      security:
        - apiKeyAuth: []
components:
  securitySchemes:
    apiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
```

# 七、异常码

|         |                                                                                              |                                |                                                                                            |
| ------- | -------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------ |
| http异常码 | 消息体                                                                                          | 异常原因                           | 处理方式                                                                                       |
| 403     | {"code": "403",  "message": "You do not have enough money",  "log_id": "c66aac17eab1bb7e"}   | 余额不足                           | 请前往 https://open.bochaai.com 进行充值                                                          |
| 400     | {"code": "400","message": "Missing parameter query","log_id": "c66aac17eab1bb7e"}            | 请求参数缺失                         |                                                                                            |
| 400     | {"code": "400","message": "The API KEY is missing","log_id": "c66aac17eab1bb7e"}             | 权限校验失败，Header 缺少 Authorization |                                                                                            |
| 401     | {"code": "401","message": "Invalid API KEY","log_id": "c66aac17eab1bb7e"}                    | API KEY无效                      | 权限校验失败                                                                                     |
| 429     | {"code": "429","message": "You have reached the request limit","log_id": "c66aac17eab1bb7e"} | 请求频达到率限制                       | 频率限制与总充值金额有关，具体详见：[API 定价](https://aq6ky2b8nql.feishu.cn/wiki/JYSbwzdPIiFnz4kDYPXcHSDrnZb) |
| 500     | {"code": "500","message": "xxxx","log_id": "c66aac17eab1bb7e"}                               | 各种异常                           |                                                                                            |
