//最新开源
KISSY.ready(function(S) {
    //搜索
    S.add(function() {
    }, {requires: ['js/mods/search']});
    S.use("dom,event,sizzle", function (S,D,E) {
        E.on(".d-p-newopen tr","mouseenter mouseleave",function(e){
            D.toggleClass(this,"hover");
        });
        E.on(".d-p-update tr","mouseenter mouseleave",function(e){
            D.toggleClass(this,"hover");
        });
        //language_arts
        var langvdefault= S.trim(D.val(".d-p-languagesearch .search-text"));
        E.on(".d-p-languagesearch .search-text","focusin focusout",function(e){
            if(e.type=="focusin"){
                D.val(this, "");
            }else{
                if(S.trim(D.val(this))==""){
                    D.val(this, langvdefault);
                }
            }
        });
        E.on(".d-p-languagesearch .search-btn","click",function(e){
            if(S.trim(D.val(".d-p-languagesearch .search-text"))==langvdefault)
            return;
            window.location.href='/project/lang/list/'+S.trim(D.val(".d-p-languagesearch .search-text"))+'/1/';

        });
        var alllanguage=[],alllanguagehref=[];
        S.each(S.query(".d-p-languagelist a"),function(item){
            alllanguage.push(D.html(item).toUpperCase());
            alllanguagehref.push(D.attr(item,"href"));
        });
        E.on(".d-p-languagesearch .search-text","valuechange",function(e){
            var s="";
            if(e.newVal==""){
                S.each(alllanguage,function(item,v){
                    s+='<li><a href='+alllanguage[v]+'>'+item+'</a></li>';
                });
                D.html(".d-p-languagelist",s);
                return;
            }else{
                var nowlanguage=[],nowlanguagehref=[];
                if(e.newVal==""){
                    return;
                }
                var newVal = e.newVal.replace(/([\+\*\?\.\[\]])/g,'\\$1');
                var patt=new RegExp("^"+newVal.toUpperCase()+".*");
                S.each(alllanguage,function(item,v){
                    if(patt.test(item)){
                        nowlanguage.push(item);
                        nowlanguagehref.push(alllanguagehref[v]);
                    }
                });
                S.each(nowlanguage,function(item,v){
                    s+='<li><a href='+nowlanguagehref[v]+'>'+item+'</a></li>';
                });
                D.html(".d-p-languagelist",s);
            }
        });
    });
});
