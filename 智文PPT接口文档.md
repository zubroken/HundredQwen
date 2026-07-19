\# 讯飞星火 智能 PPT 生成（新版）接口文档 

## 一、新版核心说明 

新版优势：200+ 免费主题模板，支持联网搜索、AI 配图，不额外扣量 接口限制：新版与旧版接口不可混用，推荐使用新版 页数控制：无法精确指定页数，通过大纲章节数量调整 

## 二、接口鉴权

 接口域名：`zwapi.xfyun.cn`

请求头必填参数： - appId：应用 ID - timestamp：时间戳（秒），与服务端相差≤5 分钟 - signature：签名（MD5+HmacSHA1+Base64） 

鉴权逻辑： signature = hmacSHA1( md5(appId+timestamp), secret ) 

## 三、错误码 

| 错误码 | 说明         | 处理方式                                                     |
| ------ | ------------ | ------------------------------------------------------------ |
| 20002  | 参数错误     | 确认接口参入                                                 |
| 20005  | 大纲生成失败 | 查看是否存在敏感词汇，尝试重新生成                           |
| 20006  | PPT生成失败  | PPT导出错误，请重新生成或联系技术人员                        |
| 20007  | 鉴权错误     | 检查鉴权信息                                                 |
| 9999   | 系统异常     | 确认鉴权信息、请求方式、请求参数是否有误，或联系技术人员排查相关日志 |



## 四、核心接口列表

 ### 1. PPT 主题列表查询

接口地址： https://zwapi.xfyun.cn/api/ppt/v2/template/list

请求类型：application/json

筛选参数：style风格、color颜色、industry行业、pageNum页数、pageSize每页数量 

返回：templateIndexId（模板 ID）、预览图、页数等 

### 2. 直接生成 PPT 

接口地址： https://zwapi.xfyun.cn/api/ppt/v2/create 

请求类型：multipart/form-data 

必选三选一：query/file/fileUrl 

支持文件：pdf/doc/docx/txt/md（txt≤100 万字，其他≤10M） 

可选：templateId、isCardNote演讲备注、search联网、isFigureAI 配图、language语种 

返回：sid（唯一 ID）、封面图、标题 

### 3. 生成大纲 

接口地址：POST https://zwapi.xfyun.cn/api/ppt/v2/createOutline 

请求类型：multipart/form-data 

必填：query  用户生成PPT要求（最多12000字）注意：query不能为空字符串、仅包含空格的字符串

返回：sid、完整大纲结构（标题 / 章节） 

### 4. 文档生成大纲 

- 地址：POST https://zwapi.xfyun.cn/api/ppt/v2/createOutlineByDoc 
- 请求类型：multipart/form-data 
- 必填：fileName + file/fileUrl 

同生成大纲返回 

### 5. 按大纲生成 PPT 

- 地址：POST https://zwapi.xfyun.cn/api/ppt/v2/createPptByOutline 
- 请求类型：application/json 
- 必填：query、outline（大纲结构体） 
- 可选：outlineSid、templateId、配图、备注、联网等 
- 返回同「直接生成 PPT」 

### 6. PPT 进度查询 

地址：GET https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={sid} 

限流：3 秒 / 次 

返回状态：

- pptStatus：building/done/build_failed 
- pptUrl：PPT 下载链接（保存 30 天） 
- 总页数 / 已完成页数 

## 五、扣量规则（基础 + 附加） 

### 基础扣量 

- 直接生成 PPT：10 点，1 并发 
- 生成大纲：2 点，1 并发 
- 按大纲生成 PPT：8 点 

### 附加扣量

- AI 配图：普通 4 点 / 高级 8 点 
-  演讲备注：5 点 
-  多语种：大纲 1 点 / PPT 2 点 
-  联网搜索：2 点 

## 六、调用流程

1. 查模板 → 获取templateIndexId 
2.  生成大纲 / 直接生成 PPT → 获取sid  
3. 轮询进度 → 完成后获取pptUrl 
4. 下载 PPT ## 其他 官方 Demo：Java / Python / SDK-DEMO 
