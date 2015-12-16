//最新开源
KISSY.ready(function(S) {
    //搜索
    S.add(function() {
    }, {requires: ['js/mods/search']});
    S.use("dom,event,ua,sizzle", function (S,D,E,U) {
        D.val("#select_versions","");
        E.on('.d-p-project-files tr','mouseenter mouseleave', function(e) {
            if(D.attr(D.first(this),"width")){
                return;
            }
           D.toggleClass(this,"hover");
        });
        E.on('.d-p-project-files tr','click', function(e) {
            if(D.attr(D.first(this),"width")){
                return;
            }
            var select_versions=[];
            if( D.val("#select_versions")==""){
                select_versions=[];
            }else{
                select_versions= D.val("#select_versions").split(",");
            }
            var select=D.attr(S.one(this),"id");//选中版本号
            if(D.attr(this,"class").indexOf("selected")!=-1){
                select_versions.splice(S.indexOf(select,select_versions),1);
            }else{
                if(D.val("#select_versions").split(",").length==2){
                    return;
                }
                select_versions.push(select);

            }
            D.toggleClass(this,"selected");
            D.val("#select_versions",select_versions.join(","));
        });
    });
});
