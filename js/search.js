sEngine = "bing";

// 选中默认搜索引擎图标
function chooseDefaultEngineRadio()
{
    // 设置默认搜索引擎单选按钮选中
    var rRadio = document.getElementsByName( "searchEngine");
    for(var i = 0;i<rRadio.length;i++){
        if(rRadio[i].id = sEngine){
            rRadio[i].checked = 'checked';
            break;
        }
    }
}

// 切换搜索引擎
function setSearchEngine(engine){
    // 更改变量
    sEngine = engine;
    // 更改图标
    var seiObj = document.getElementById("searchEngineIco");
    iconsrc = "https://cdn.jsdelivr.net/gh/ruxia-TJY/webicon@latest/png/" + engine + ".png";

    seiObj.src = iconsrc;
}

// 搜索
function startSearch()
{
    // 获取要搜索的内容
    var sWord= document.getElementById("searchInput").value;

    sEngineURL = "";
    switch(sEngine){
        case "baidu":
            sEngineURL = "https://www.baidu.com/s?word=";break;
        case "bing":
            sEngineURL = "https://cn.bing.com/search?q=";break;
        case "google":
            sEngineURL = "https://www.google.com/search?q=";break;
        case "github":
            sEngineURL = "https://github.com/search?q=";break;
        case "gitee":
            sEngineURL = "https://search.gitee.com/?q=";break;

    }
    window.event.returnValue=false;

    window.location.href = encodeURI(sEngineURL + sWord);
}

// 点击图标打开相应搜索引擎网址
function openEngineWebsite()
{
    openURL="";
    switch(sEngine){
        case "baidu":
            openURL="https://www.baidu.com";break;
        case "bing":
            openURL="https://cn.bing.com";break;
        case "google":
            openURL = "https://www.google.com";break;
        case "github":
            openURL = "https://github.com";break;
        case "gitee":
            openURL = "https://gitee.com";break;
    }
    window.location.href = openURL;
}