//最新开源
KISSY.use("dom,event,ua,sizzle", function (S,D,E,U) {
    if(U.ie==6){
        E.on(".d-m-search-type","mouseenter mouseleave",function(e){
            D.toggleClass(this,"hover");
        });
    }
    E.on(".d-m-search-type li","click",function(e){
        D.prepend(this,".d-m-search-type-list");
        D.val("#type", D.attr(this,"data-type"));
    });
    var searchvdefault= S.trim(D.val(".d-m-search .search-text"));
    E.on(".d-m-search .search-text","focusin focusout",function(e){
        if(e.type=="focusin"){
            D.val(this, "");
        }else{
            if(S.trim(D.val(this))==""){
                D.val(this, searchvdefault);
            }
        }
    });
});