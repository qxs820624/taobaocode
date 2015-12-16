/*
combined files : 

page/language-pic

*/
$(function () {
    var chart,_data=[];
    $(document).ready(function() {
        $.ajax({
            url: '/ajax/prj/lang/',
            type: 'GET',
            dataType: 'json',
            success: function (json) {
                for(var i=0;i<json.length;i++){
                    if(i==1){
                        _data[i]= {
                            name: json[1][0],
                            y:parseFloat(json[1][1]),
                            sliced: true,
                            selected: true
                        }
                    }else{
                        _data[i]=[json[i][0],parseFloat(json[i][1])];
                    }
                }
                chart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'container',
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false
                    },
                    title: {
                        text: 'Top 10语言分类'
                    },
                    tooltip: {
                        formatter: function() {
                            return'<b>'+this.point.name+'</b>: '+Highcharts.numberFormat(this.percentage, 1)+' %';
                        }
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true
                            },
                            showInLegend: false
                        }
                    },
                    series: [{
                        type: 'pie',
                        name: 'Browser share',
                        data:_data
                    }]
                });
            },
            error:function(){}
        });
    });

});
