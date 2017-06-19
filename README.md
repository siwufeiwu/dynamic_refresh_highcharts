# dynamic_refresh_highcharts

Highcharts之动态刷新——结合后台数据，flask实现，以内存监控为例

http://ju.outofmemory.cn/entry/126800


功能：
---
1.完成监控页面的展示。<br>
2.monitor.py在被监控主机上运行，time.sleep(1)设置每1秒就会取一次数据写入数据库，监控程序monitor.py通过post提交数据到web后台存入数据库。（可以直接存入数据库，不通过flask后台post接口）<br>
3.图表使用的JS为highcharts、highstock 。<br>
3.前台highcharts通过json接口不断到后台get一条最新的数据库加入图表显示，动态刷新。<br>
4.highcharts动态刷新，重点是chart里面的event属性，series属性。此时：series属性是模板渲染是提供的一组数据，而event属性是一个js函数（实现周期性ajax请求数据），highstock代码如下：<br>
```
<script type="text/javascript">
  var data={{data}}; 
  //创建图表
  var chart;
  $(document).ready(function() {
   Highcharts.setOptions({
    global:{
        useUTC:false
    }
   })
   chart = new Highcharts.StockChart( {
    chart : {
     renderTo : 'container',
     events : {
      load : st// 定时器（函数）
     }
    },
    rangeSelector: {
      inputEnabled: $('#container').width() > 480,
        selected: 1
    },
    exporting:{
     enabled:true
    },
    title : {
     text : '内存使用情况'
    },
    series : [ {
     name: '内存使用情况',
     data : data,
     type: 'spline',
     }]
   });
   
  });
  //2秒钟刷新一次数据
  function st() {
   setInterval("getData()", 1000);
  }
  //动态更新图表数据
  function getData() {
   $.ajax({
      type: "get",
      url: "/new",
      dataType: "json",
      success : function(data){
      chart.series[0].addPoint(data,true,true);

      }
    });
  }
  </script>
```

运行
---
@ubuntu:~$python flask_web.py 监听在8888端口上。<br>
@ubuntu:~$python monitor.py 采集数据
<br>
访问 http://localhost:8888 就可以看到的监控数据了<br>
效果图如下
---
![demo1](http://img.blog.csdn.net/20160317215157193?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
![demo2](http://img.blog.csdn.net/20160317215249348?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
