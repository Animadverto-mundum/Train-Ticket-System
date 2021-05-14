# 数据分析模块前后端对接说明



前端只需要看`Analysis.py`中的代码，设计是只有`manger_predict.html`这一个html界面。request请求中按以下两种情况分类：

1. 请求预测数据
   - 请求应该包含的字段
     - 请求类型`type`：应该是    'predict'
     - 预测周期`periods`    应该是个整数
     - 预测频率 `freq`   应该是个复选框    可选值：`1D`   `1Y`   `1M`  `1W`       数字1可以修改成任何值  看你前端展现形式   也可以输入两个字段（数字和单位）给我，交给我来拼接。
   - 我返回的字段
     - 字典组成的列表，名称`predict_list`。字段键名分别为`'ds', 'yhat', 'yhat_lower', 'yhat_upper'`  代表时间、预测值、预测值上限、预测值下限。在html中读取列表中每一个item，再用item.键名的方式显示成一个表格。
     - 图片，名称`pic`，调用方式我已经写在`manger_predict.html`
2. 请求分析趋势
   - 请求应该包含的字段
     - 请求类型`type`：应该是    'trend'
     - 车次号`train_number_ID`:一个字符串
     - 开始时间`begin_time`:一个字符串  格式如`20210514`
     - 结束时间`end_time`
   - 我返回的字段
     - 图片，名称`pic`，调用方式我已经写在`manger_predict.html`

同时提供了多个错误检查，利用flash返回了错误，记得在前端显示就行。



