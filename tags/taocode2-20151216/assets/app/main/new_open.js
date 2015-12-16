//最新开源
KISSY.ready(function(S) {
    S.add(function() {
    }, {requires: ['assets/mods/search']});
    S.use("dom,event,sizzle", function (S,D,E) {
        E.on(".d-p-newopen tr","mouseenter mouseleave",function(e){
            D.toggleClass(this,"hover");
        });
    });
});
