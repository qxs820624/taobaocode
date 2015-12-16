//∏≈¿¿
KISSY.use("switchable,dom,event,sizzle", function (S, Switchable,D,E) {
    var s = new Switchable.Slide('#J_Slide', {
        effect : 'none',
        easing : 'easeOutStrong',
        activeTriggerCls:'current'
    });
    E.on(".d-p-projectlist li","mouseenter mouseleave",function(e){
        D.toggleClass(this,"current");

    });
    E.on(".d-p-index-hotmember li","mouseenter mouseleave",function(e){
        D.addClass(".d-p-index-hotmember li","active");
        D.removeClass(this,"active");
    });
    E.on(".d-m-main-nav li","mouseenter mouseleave",function(e,v){
        console.log(v);
    });

});