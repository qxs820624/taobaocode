KISSY.ready(function(S) {
    S.add(function() {
    }, {requires: ['js/mods/search']});
    S.use("dom,event,js/mods/overlayer,sizzle", function (S,D,E,O) {
        E.delegate(document,'click','.close',function(e){
            var old_tages;
            old_tages=D.val("#tages").split(/,|��/);
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
             O.show("��ӱ�ǩ",D.html("#addtag-html"),"");
        });
//        E.on(".project-delete","click",function(){
//            O.show("ɾ����Ŀ",'<p>���Ƿ�Ҫɾ������Ŀ��</p><a href="javascript:void(0);" class="p-p-project-btn del-project">ȷ��ɾ��</a>',"");
//        });
//        E.on(".question-info #btn_close","click",function(){
//            O.show("�ر�����",D.html("#addtag-html"),"");
//        });
//        E.on(".question-info #btn_del","click",function(){
//            O.show("ɾ������",D.html("#addtag-html"),"");
//        });
    });
});