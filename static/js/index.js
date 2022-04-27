// 全球页面js

// 中间累计数据
(function () {
    $.ajax({
        url: 'http://127.0.0.1:5001/film/statistics',
        type: 'get',
        // data: {},
        dataType: 'json',
    }).then((data) => {
        $(".no-hd li:first").text(data.film_total)
        $(".no-hd li:nth-child(2)").text(data.film_type_total)
        $(".no-hd li:nth-child(3)").text(data.director_total)
        $(".no-hd li:nth-child(4)").text(data.performer_total)
        $(".no-hd li:last").text(data.country_total)
    })
})();


// 1、语言占比 -饼图
(function () {
    //初识化ECharts
    var myChart = echarts.init(document.querySelector(".bar .chart"));
    //指定配置项和数据
    var option = {
        title: {
            show: false,
            text: '饼图',
            x: 'center'
        },
        color: ['#37a2da', '#9fe6b8', '#ffdb5c', '#ff9f7f', '#fb7293', '#8378ea', '#00d887'],
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        calculable: true,
        series: [{
            name: '电影语言Top10',
            type: 'pie',
            radius: [50, 100],
            center: ['50%', '50%'],
            roseType: 'radius',
            // data:
        }]
    };
    //配置项设置给ECarts实例对象
    myChart.setOption(option);
    var count = [];
    $.ajax({
        url: 'http://127.0.0.1:5001/film/language/top',
        type: 'get',
        // data: {},
        dataType: 'json',
        success: function (data) {
            data.forEach(x => count.push({
                name: x['name'],
                value: x['total']
            }))

            //必须在这里在设置一遍，这里涉及到的问题不太懂，只知道如不再设置，而在ajax外赋值是没有作用的
            myChart.setOption({ //加载数据图表
                series: [{
                    data: count
                }]
            })
        }
    })

    //图表跟随屏幕自适应
    window.addEventListener('resize', function () {
        myChart.resize();
    })
})();


// 3、评分-片长关系 - 散点图
(function () {
    var myChart = echarts.init(document.querySelector('.line .chart'))

    var option = {
        // title: {
        //     left: 'center',
        //     text: '评分-片长关系',
        //     textStyle: {
        //         color: '#6d6'
        //     }
        // },
        tooltip: {},
        // legend: {
        //     left: 'right'
        // },
        // dataset: {
        //     source: [
        //         ['length', '123', '22', '222', '2333'],
        //         ['score', 1, 3.5, 4.5,9.8]
        //     ]
        // },
        xAxis: {
            name: '分钟',
            type: 'category'
        },
        axisLabel: {
            color: '#FFFFFF'
        },
        yAxis: {
            name: '评分'
        },
        series: [
            {
                name: '片长-评分',
                type: 'scatter',
                seriesLayoutBy: 'row',
                symbolSize: 4,
                itemStyle: {
                    color: '#e48'
                }
            }
        ]
    };

    myChart.setOption(option);

    $.ajax({
        url: 'http://127.0.0.1:5001/film/score/length/relation',
        type: 'get',
        // data: {},
        dataType: 'json',
        success: function (data) {
            var x = ['length']
            var y = ['score']
            data.forEach(item => {
                x.push(item["length"])
                y.push(item["score"])
            })
            //必须在这里在设置一遍，这里涉及到的问题不太懂，只知道如不再设置，而在ajax外赋值是没有作用的
            myChart.setOption({ //加载数据图表
                dataset: {
                    source: [
                        x,
                        y
                    ]
                },
            })
        }
    })

    window.addEventListener('resize', function () {
        myChart.resize()
    })
})();

function randomColor() {
    return 'rgb(' + [
        Math.round(Math.random() * 160),
        Math.round(Math.random() * 160),
        Math.round(Math.random() * 160)
    ].join(',') + ')';
}

// 导演数量top n -柱状图
(function () {
    // 初始化绘制图表的echarts实例
    var myChart = echarts.init(document.querySelector('.bar1 .chart'))

    // 指定图表的配置
    var option = {
        tooltip: {//提示框组件
            trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
            axisPointer: {
                // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: '{b} <br/>电影计数 : {c}' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
        },
        xAxis: {
            name: '姓名',
            axisLabel: {
                //x轴文字的配置
                show: true,
                interval: 0,//使x轴文字显示全
                rotate: -35
            },
            data: []    //x轴
        },
        grid: {
            left: '5%',
            top: '15%',
            containLabel: true
        },
        axisLabel: {
            color: '#FFFFFF',
        },
        yAxis: {
            name: '数量'
        },    //不写的话，y轴默认就标出数字
        //=====图标的数据
        series: [
            {
                name: "电影数量",    //鼠标放上去浮现的内容，跟data一样
                type: "bar",     //指定条形图类型
                data: []      //分别对应vue、react那几个x轴的数值
            }
        ]
    }
    // 对实例对象设置配置
    myChart.setOption(option)

    $.ajax({
        url: 'http://127.0.0.1:5001/film/director/films',
        type: 'get',
        // data: {},
        dataType: 'json',
        success: function (data) {
            var x = []
            var y = []
            data.forEach(item => {
                x.push(item["name"])
                y.push(item["total"])
            })

            //必须在这里在设置一遍，这里涉及到的问题不太懂，只知道如不再设置，而在ajax外赋值是没有作用的
            myChart.setOption({ //加载数据图表
                xAxis: {
                    data: x    //x轴
                },
                series: [
                    {
                        name: "电影数量",    //鼠标放上去浮现的内容，跟data一样
                        type: "bar",     //指定条形图类型
                        data: y      //分别对应vue、react那几个x轴的数值
                    }
                ]
            })
        }
    })

    window.addEventListener("resize", function () {
        myChart.resize();
    });
})();


// 电影类型-词云
(function () {
    // 初始化绘制图表的echarts实例
    var myChart = echarts.init(document.querySelector('.line1 .chart'))

    $.ajax({
        url: 'http://127.0.0.1:5001/film/type',
        type: 'get',
        // data: {},
        dataType: 'json',
        success: function (data) {
            var res = data.map(val => ({
                ...val,
                textStyle: {
                    normal: {
                        color: randomColor()
                    }
                }
            }));

            //必须在这里在设置一遍，这里涉及到的问题不太懂，只知道如不再设置，而在ajax外赋值是没有作用的
            myChart.setOption({
                series: [{
                    type: 'wordCloud',
                    shape: 'circle',
                    left: 'center',
                    top: 'center',
                    right: null,
                    bottom: null,
                    width: '100%',
                    height: '95%',
                    sizeRange: [12, 70],
                    rotationRange: [-25, 25],
                    rotationStep: 8,
                    gridSize: 14,
                    drawOutOfBound: false,
                    textStyle: {
                        normal: {
                            fontFamily: 'sans-serif',
                            fontWeight: 'normal'
                        },
                        emphasis: {
                            shadowBlur: 10,
                            shadowColor: 'yellow'
                        }
                    },
                    data: res
                }],
                tooltip: {//提示框组件
                    trigger: 'item', //item数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
                    axisPointer: {
                        // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                    },
                    formatter: '{b} <br/>电影计数 : {c}' //{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
                },
            })
        }
    })

    window.addEventListener("resize", function () {
        myChart.resize();
    });
})();


// 4、全球电影地图 -地图
(function () {
    var myChart = echarts.init(document.querySelector('.map .chart'))
    var nameMap = {
        "Canada": "加拿大",
        "Turkmenistan": "土库曼斯坦",
        "Saint Helena": "圣赫勒拿",
        "Lao PDR": "老挝",
        "Lithuania": "立陶宛",
        "Cambodia": "柬埔寨",
        "Ethiopia": "埃塞俄比亚",
        "Faeroe Is.": "法罗群岛",
        "Swaziland": "斯威士兰",
        "Palestine": "巴勒斯坦",
        "Belize": "伯利兹",
        "Argentina": "阿根廷",
        "Bolivia": "玻利维亚",
        "Cameroon": "喀麦隆",
        "Burkina Faso": "布基纳法索",
        "Aland": "奥兰群岛",
        "Bahrain": "巴林",
        "Saudi Arabia": "沙特阿拉伯",
        "Fr. Polynesia": "法属波利尼西亚",
        "Cape Verde": "佛得角",
        "W. Sahara": "西撒哈拉",
        "Slovenia": "斯洛文尼亚",
        "Guatemala": "危地马拉",
        "Guinea": "几内亚",
        "Dem. Rep. Congo": "刚果（金）",
        "Germany": "德国",
        "Spain": "西班牙",
        "Liberia": "利比里亚",
        "Netherlands": "荷兰",
        "Jamaica": "牙买加",
        "Solomon Is.": "所罗门群岛",
        "Oman": "阿曼",
        "Tanzania": "坦桑尼亚",
        "Costa Rica": "哥斯达黎加",
        "Isle of Man": "曼岛",
        "Gabon": "加蓬",
        "Niue": "纽埃",
        "Bahamas": "巴哈马",
        "New Zealand": "新西兰",
        "Yemen": "也门",
        "Jersey": "泽西岛",
        "Pakistan": "巴基斯坦",
        "Albania": "阿尔巴尼亚",
        "Samoa": "萨摩亚",
        "Czech Rep.": "捷克",
        "United Arab Emirates": "阿拉伯联合酋长国",
        "Guam": "关岛",
        "India": "印度",
        "Azerbaijan": "阿塞拜疆",
        "N. Mariana Is.": "北马里亚纳群岛",
        "Lesotho": "莱索托",
        "Kenya": "肯尼亚",
        "Belarus": "白俄罗斯",
        "Tajikistan": "塔吉克斯坦",
        "Turkey": "土耳其",
        "Afghanistan": "阿富汗",
        "Bangladesh": "孟加拉国",
        "Mauritania": "毛里塔尼亚",
        "Dem. Rep. Korea": "朝鲜",
        "Saint Lucia": "圣卢西亚",
        "Br. Indian Ocean Ter.": "英属印度洋领地",
        "Mongolia": "蒙古",
        "France": "法国",
        "Cura?ao": "库拉索岛",
        "S. Sudan": "南苏丹",
        "Rwanda": "卢旺达",
        "Slovakia": "斯洛伐克",
        "Somalia": "索马里",
        "Peru": "秘鲁",
        "Vanuatu": "瓦努阿图",
        "Norway": "挪威",
        "Malawi": "马拉维",
        "Benin": "贝宁",
        "St. Vin. and Gren.": "圣文森特和格林纳丁斯",
        "Korea": "韩国",
        "Singapore": "新加坡",
        "Montenegro": "黑山共和国",
        "Cayman Is.": "开曼群岛",
        "Togo": "多哥",
        "China": "中国",
        "Heard I. and McDonald Is.": "赫德岛和麦克唐纳群岛",
        "Armenia": "亚美尼亚",
        "Falkland Is.": "马尔维纳斯群岛（福克兰）",
        "Ukraine": "乌克兰",
        "Ghana": "加纳",
        "Tonga": "汤加",
        "Finland": "芬兰",
        "Libya": "利比亚",
        "Dominican Rep.": "多米尼加",
        "Indonesia": "印度尼西亚",
        "Mauritius": "毛里求斯",
        "Eq. Guinea": "赤道几内亚",
        "Sweden": "瑞典",
        "Vietnam": "越南",
        "Mali": "马里",
        "Russia": "俄罗斯",
        "Bulgaria": "保加利亚",
        "United States": "美国",
        "Romania": "罗马尼亚",
        "Angola": "安哥拉",
        "Chad": "乍得",
        "South Africa": "南非",
        "Fiji": "斐济",
        "Liechtenstein": "列支敦士登",
        "Malaysia": "马来西亚",
        "Austria": "奥地利",
        "Mozambique": "莫桑比克",
        "Uganda": "乌干达",
        "Japan": "日本",
        "Niger": "尼日尔",
        "Brazil": "巴西",
        "Kuwait": "科威特",
        "Panama": "巴拿马",
        "Guyana": "圭亚那",
        "Madagascar": "马达加斯加",
        "Luxembourg": "卢森堡",
        "American Samoa": "美属萨摩亚",
        "Andorra": "安道尔",
        "Ireland": "爱尔兰",
        "Italy": "意大利",
        "Nigeria": "尼日利亚",
        "Turks and Caicos Is.": "特克斯和凯科斯群岛",
        "Ecuador": "厄瓜多尔",
        "U.S. Virgin Is.": "美属维尔京群岛",
        "Brunei": "文莱",
        "Australia": "澳大利亚",
        "Iran": "伊朗",
        "Algeria": "阿尔及利亚",
        "El Salvador": "萨尔瓦多",
        "C?te d'Ivoire": "科特迪瓦",
        "Chile": "智利",
        "Puerto Rico": "波多黎各",
        "Belgium": "比利时",
        "Thailand": "泰国",
        "Haiti": "海地",
        "Iraq": "伊拉克",
        "Sao Tome and Principe": "圣多美和普林西比",
        "Sierra Leone": "塞拉利昂",
        "Georgia": "格鲁吉亚",
        "Denmark": "丹麦",
        "Philippines": "菲律宾",
        "S. Geo. and S. Sandw. Is.": "南乔治亚岛和南桑威奇群岛",
        "Moldova": "摩尔多瓦",
        "Morocco": "摩洛哥",
        "Namibia": "纳米比亚",
        "Malta": "马耳他",
        "Guinea-Bissau": "几内亚比绍",
        "Kiribati": "基里巴斯",
        "Switzerland": "瑞士",
        "Grenada": "格林纳达",
        "Seychelles": "塞舌尔",
        "Portugal": "葡萄牙",
        "Estonia": "爱沙尼亚",
        "Uruguay": "乌拉圭",
        "Antigua and Barb.": "安提瓜和巴布达",
        "Lebanon": "黎巴嫩",
        "Uzbekistan": "乌兹别克斯坦",
        "Tunisia": "突尼斯",
        "Djibouti": "吉布提",
        "Greenland": "丹麦",
        "Timor-Leste": "东帝汶",
        "Dominica": "多米尼克",
        "Colombia": "哥伦比亚",
        "Burundi": "布隆迪",
        "Bosnia and Herz.": "波斯尼亚和黑塞哥维那",
        "Cyprus": "塞浦路斯",
        "Barbados": "巴巴多斯",
        "Qatar": "卡塔尔",
        "Palau": "帕劳",
        "Bhutan": "不丹",
        "Sudan": "苏丹",
        "Nepal": "尼泊尔",
        "Micronesia": "密克罗尼西亚",
        "Bermuda": "百慕大",
        "Suriname": "苏里南",
        "Venezuela": "委内瑞拉",
        "Israel": "以色列",
        "St. Pierre and Miquelon": "圣皮埃尔和密克隆群岛",
        "Central African Rep.": "中非",
        "Iceland": "冰岛",
        "Zambia": "赞比亚",
        "Senegal": "塞内加尔",
        "Papua New Guinea": "巴布亚新几内亚",
        "Trinidad and Tobago": "特立尼达和多巴哥",
        "Zimbabwe": "津巴布韦",
        "Jordan": "约旦",
        "Gambia": "冈比亚",
        "Kazakhstan": "哈萨克斯坦",
        "Poland": "波兰",
        "Eritrea": "厄立特里亚",
        "Kyrgyzstan": "吉尔吉斯斯坦",
        "Montserrat": "蒙特塞拉特",
        "New Caledonia": "新喀里多尼亚",
        "Macedonia": "马其顿",
        "Paraguay": "巴拉圭",
        "Latvia": "拉脱维亚",
        "Hungary": "匈牙利",
        "Syria": "叙利亚",
        "Honduras": "洪都拉斯",
        "Myanmar": "缅甸",
        "Mexico": "墨西哥",
        "Egypt": "埃及",
        "Nicaragua": "尼加拉瓜",
        "Cuba": "古巴",
        "Serbia": "塞尔维亚",
        "Comoros": "科摩罗",
        "United Kingdom": "英国",
        "Fr. S. Antarctic Lands": "南极洲",
        "Congo": "刚果（布）",
        "Greece": "希腊",
        "Sri Lanka": "斯里兰卡",
        "Croatia": "克罗地亚",
        "Botswana": "博茨瓦纳",
        "Siachen Glacier": "锡亚琴冰川地区"
    }
    var option = {
        title: {
            text: '各国电影数量',
            left: 'center',
            textStyle: {
                color: 'white'
            },
            top: 'top'
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                // var value = params.value + '';
                // return params.seriesName + '<br/>' + params.name + ' : ' + params.data[2] + '人';
                return "国家: " + params.data.name + "</br>" +
                    "电影计数: " + params.data.value;
            }
        },
        visualMap: {
            min: 0,
            max: 400,
            text: ['High', 'Low'],
            realtime: false,
            calculable: false,
            textStyle: {
                color: 'white'
            },
            color: ['#481380', '#7f78d2', '#efb1ff', '#ffe2ff']
        },
        series: [{
            name: '电影计数',
            type: 'map',
            mapType: 'world',
            roam: true,
            itemStyle: {
                normal: {
                    areaColor: '#fce8d5',
                    borderColor: 'rgb(0,108,255)',
                },
                emphasis: {
                    label: {
                        show: true,
                        color: 'black'
                    },
                    areaColor: '#fce8d5'
                }
            },
            nameMap: nameMap,
            // data:
        }]
    };
// 把配置和数据给实例对象
    myChart.setOption(option);
    var virus = []
    $.ajax({
        url: 'http://127.0.0.1:5001/film/country/count',
        type: 'get',
        // data: {},
        dataType: 'json',
        success: function (data) {
            data.forEach(item => {
                virus.push({
                    // 用于visualMap与地图区域对应
                    'name': item.name,
                    // 用于visualMap筛选, 颜色显示
                    'value': item.total
                })
            })

            myChart.setOption({ //加载数据图表
                series: [{
                    // 根据名字对应到相应的系列
                    data: virus
                }]
            })
        }
    });

    window.addEventListener('resize', function () {
        myChart.resize()
    })
})();