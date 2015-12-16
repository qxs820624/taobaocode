//最新开源
KISSY.use("dom,event,ua,sizzle", function (S,D,E,U) {
    if(U.ie==6){
        E.on(".d-m-search-type","mouseenter mouseleave",function(e){
            D.toggleClass(this,"hover");
        });    }
    E.on(".d-m-search-type li","click",function(e){
        D.prepend(this,".d-m-search-type-list");
        D.val("#type", D.attr(this,"data-type"));
    });
});