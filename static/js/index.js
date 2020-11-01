$(document).ready(function (){
    //初始化动态加载控件
    ajax();
	
    //注册菜单展开收缩事件

    $(".parentnode_title_symbol").click(function () {

        shrinkage($(this));

    })

    //当没有子节点的div去除样式

    upclass();
	
	$("#parentnode li:first .parentnode_title:first").addClass("active");

	$(".parentnode_title a").click(function () {
	$(".parentnode_title").each(function () {
	var each = $(this);
	each.removeClass("active");
	});

       $(this).parent().parent().addClass("active");

    })
	$(".parentnode_title_symbol").css('background-image', 'url("static/icon/minus.png")');
});
function ajax() {
    //直接使用ajax访问
    data = $("#jsonContent").val();

    var hehe = { "tbFuncDic": JSON.parse(data) }
    // alert(hehe);
    databinding(hehe);//绑定数据


}


//菜单子节点展开关闭
function shrinkage(dom) {
    //改变图片背景
    if (!dom.hasClass('parentnode_title_nochildnode_symbol')) {
        switch (parseInt($(dom).children("b").html())) {
            case 1://关闭
                $(dom).css('background-image', 'url("static/icon/plus.png")');
                $(dom).children("b").html("2");
                $(dom).parent().siblings().hide();
                break;
            case 2://展开
                $(dom).css('background-image', 'url("static/icon/minus.png")');
                $(dom).children("b").html("1");
                $(dom).parent().siblings().show();
                break;
            default: break;
        }
    }

}

//循环绑定数据

function databinding(data) {
    //动态创建树形菜单
    var parentnodediv = $("#parentnode");
    for (var i = 0; i < data.tbFuncDic.length; i++) {
        //最上层父节点
        if (data.tbFuncDic[i].parentID == 0) {
            Cycledata(parentnodediv, data.tbFuncDic[i]);
        }
    }
    //创建子节点
    if (data.tbFuncDic.length > 0) {
        childnodes(data);
    }
	
	
}

//创建子节点

function childnodes(data) {
    for (var j = 0; j < $("#parentnode").find(".parentnode_title_name").length; j++) {
        for (var i = 0; i < data.tbFuncDic.length; i++) {
            if (data.tbFuncDic[i].parentID == $("#parentnode").find(".parentnode_title_name")[j].id) {
                var parentnodediv = $($("#parentnode").find(".parentnode_title_name")[j]).parent().parent();
                Cycledata(parentnodediv, data.tbFuncDic[i]);
            }
        }
    }
}

//绑定数据方法
function Cycledata(parentnodediv, data) {
    var parentnode_noe = document.createElement("li");//创建一个div
    parentnode_noe.className = " parentnode_noe";//为div添加class
    parentnodediv.append(parentnode_noe);//将其添加到div末尾

    var parentnode_title = document.createElement("div");//创建一个div
    parentnode_title.className = " parentnode_title ";//为div添加class
    parentnode_noe.appendChild(parentnode_title);//将其添加到div末尾

    var parentnode_title_symbol = document.createElement("div");//创建一个div
    parentnode_title_symbol.className = "parentnode_title_symbol parentnode_title_fix ";//为div添加class
    parentnode_title.appendChild(parentnode_title_symbol);//将其添加到div末尾
    var b = document.createElement("b");//创建一个b标签
    b.innerHTML = 1;//为b添加内容
    parentnode_title_symbol.appendChild(b);//将其添加到div末尾
    var parentnode_title_name = document.createElement("div");//创建一个div
    parentnode_title_name.className = "parentnode_title_name";//为div添加class

    if ( data.titleName.length > 30) {
        parentnode_title_name.innerHTML = "<a href='#a_" + data.titleID + "' title='" + data.titleName + "'>" + data.titleName.substr(0,30) + '...'  + "</a>";//为div添加class
    } else {
        parentnode_title_name.innerHTML = "<a href='#a_" + data.titleID + "' title='" + data.titleName + "'>" + data.titleName + "</a>";//为div添加class
    }
    parentnode_title_name.id = data.titleID;//为div添加ID
    parentnode_title_name.setAttribute("name", data.parentID);

    parentnode_title.appendChild(parentnode_title_name);//将其添加到div末尾

}



//当没有子节点的div去除样式

function upclass() {
    $(".parentnode_title").each(function () {
        var me = $(this);
        if (me.siblings().length == 0) {
            me.find(".parentnode_title_symbol b").css("display", "none");
            me.find(".parentnode_title_symbol").addClass("parentnode_title_nochildnode_symbol").removeClass("parentnode_title_symbol");
        }
    })
}