//概览
KISSY.ready(function(S) {
    S.add(function() {
    }, {requires: ['js/mods/search']});
    S.use("switchable,dom,event,js/mods/overlayer,sizzle", function (S, Switchable,D,E,O) {
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
//        var content= function(name){
//            return '<div class="layout content">'+
//                '<p>send to '+name+'</p>' +
//                '<textarea class="text" style="width:296px;height:47px;" id="messagecontent"></textarea>'+
//                '<a href="javascript:void(0);" class="p-p-project-btn sendmail">确认添加</a>'+
//                '</div>';
//        }
//        E.on(".email","click",function(e){
//            var questioner=D.attr(S.one(e.target),"data-name");
//            O.show("发站内信",content(questioner),questioner );
//        });


    });
});
init_send_msg("");