KISSY.ready(function(S) {
    S.add(function() {
    }, {requires: ['js/mods/search']});
    S.use("dom,event,js/mods/overlayer,sizzle", function (S,D,E,O) {
        E.delegate(document,'click','.close',function(e){
            var old_tages;
            old_tages=D.val("#tages").split(/,|，/);
            var _this=S.one(e.target);
            var cl_tag=D.html(D.first(D.parent(_this))),cl_tag_index=S.indexOf(cl_tag,old_tages);
            if(cl_tag_index<0){
                return;
            }else{

                old_tages.splice(cl_tag_index,1);
            }
            D.remove(D.parent(_this,'.tag'));
            D.val("#tages",old_tages.join(","));
        });
        E.on(".addtag","click",function(){
             O.show("添加标签",D.html("#addtag-html"),"");
        });
//        E.on(".project-delete","click",function(){
//            O.show("删除项目",'<p>你是否要删除该项目？</p><a href="javascript:void(0);" class="p-p-project-btn del-project">确认删除</a>',"");
//        });
//        E.on(".question-info #btn_close","click",function(){
//            O.show("关闭问题",D.html("#addtag-html"),"");
//        });
//        E.on(".question-info #btn_del","click",function(){
//            O.show("删除问题",D.html("#addtag-html"),"");
//        });
    });
});