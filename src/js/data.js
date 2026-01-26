function getNavTitleLise(title,id) {
    let text = `<li class="nav-list-li"><a href='#${id}'>${title}</a>`;
    return text;
}
function loadJson(){
    var jsonUrl = 'webindexdb.json?timestamp' + new Date().getTime();
    var request = new XMLHttpRequest();
    request.open("get",jsonUrl);
    request.send(null);
    request.onload = function (){
        if(request.status == 200){
            var json = JSON.parse(request.responseText);

            var title_list = {};
            var div_title = "";

            for(let title_i = 0;title_i < json["TitleList"].length;title_i++){
                title_list[title_i] = json["TitleList"][title_i];

                div_title += getNavTitleLise(json["TitleList"][title_i],title_i);
            }
            // div_title += "<hr />";
            div_title += getNavTitleLise("关于","about");
            document.getElementById("nav-list").innerHTML = div_title;


            var list_html = ""

            for(let title_i = 0;title_i < json["TitleList"].length;title_i++){
                title = json['TitleList'][title_i];

                let div_html = "";
                let header_html = `<h2><a name="${title_i}"></a> ${title}</h2>`;
                var url_list = '';
                for (let url_i = 0;url_i < json[title]["list"].length;url_i++){
                    urlobj = json[title]['list'][url_i];

                    switch (urlobj["y"]){
                        case 0:
                            l =  `<hr /><abbr title='${urlobj["t"]}'>${urlobj["n"]}</abbr>`;
                            break;
                        case 1:
                            l = `<li><a href="${urlobj['l']}"><abbr title="${urlobj['t']}">${urlobj['n']}</abbr></a> </li>`;
                            break;
                    }
                    url_list += l;
                }
                div_html = `${header_html}<ul>${url_list}</ul><br /><br /><hr />`;

                list_html += div_html;
            }

            document.getElementById("list").innerHTML = list_html;
            document.getElementById("lastChangedTime").innerText = `数据更新时间：${json["lastChangedTime"]}`;
        }
    }
}