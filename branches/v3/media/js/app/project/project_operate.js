//最新开源
KISSY.ready(function(S) {
    //搜索
    S.add(function() {
    }, {requires: ['js/mods/search']});
    S.use("dom,event,ua,sizzle", function (S,D,E,U) {
        E.on(".radio","click",function(e){
            if(D.attr(S.one(e.target),"id")=="is_public"){
                D.style(".yestag",{"display":"block"});
                D.style(".notag",{"display":"none"});
            }
            if(D.attr(S.one(e.target),"id")=="is_private"){
                D.style(".notag",{"display":"block"});
                D.style(".yestag",{"display":"none"});
            }
        });
        E.on("#J_nfpinpai_list .text-down a","click",function(e){
            D.text(".liecense-text span",D.text(this));
            D.val("#id_license",D.text(this));
        });
//        E.delegate(document,"click","#J_language_list .text-down a",function(e){
//            var select_languages=[],select_language=D.text(S.one(e.target));
//            var select_tags="";
//            if(S.trim(D.html(".select_language"))=="")
//            {
//                select_languages=[];
//            }else{
//                S.each(S.query(".select_language span"),function(item){
//                    select_languages.push(D.html(D.first(item)));
//                });
//            }
//            if(S.indexOf(select_language,select_languages)>-1){
//                return;
//            }
//            select_languages.push(select_language);
//            S.each(select_languages,function(item){
//                select_tags+='<span><b>'+item+'</b><a href="javascript:void(0);" class="p-p-project-btn close">close</a></span>';
//            });
//            D.html(".select_language",select_tags);
//            D.val("#id_language",select_languages.join(","));
//        });
        E.delegate(document,"click","#J_language_list .text-down a",function(e){
            var select_language=D.text(S.one(e.target));
            var select_tags='<span><b>'+select_language+'</b><a href="javascript:void(0);" class="p-p-project-btn close">close</a></span>';
            D.html(".select_language",select_tags);
            D.val("#id_language",select_language);
        });
        var alllanguage=[];
        S.each(S.query("#J_language_list a"),function(item){
            alllanguage.push(D.html(item).toUpperCase());
        });
        D.html("#J_language_list .text-down","");
        E.on(".language-text .text","valuechange",function(e){
            D.html("#J_language_list .text-down","");
            var nowlanguage=[],s="";
            if(e.newVal==""){
                return;
            }
            var patt=new RegExp("^"+e.newVal.toUpperCase()+"\w*");
            S.each(alllanguage,function(item,v){
                if(patt.test(item)){
                    nowlanguage.push(item);
                }
            });
            S.each(nowlanguage,function(item,v){
                s+='<a href="javascript:void(0);">'+item+'</a>';
            });
            D.html("#J_language_list .text-down",s);
        });
        E.on(".language-text .text","focusin focusout", function (e) {
            D.toggleClass("#J_language_list","hover");
        });
        E.delegate(document,"click",".select_language .close",function(e){
            var old_tages;
            old_tages=D.val("#id_language").split(/,|，/);
            var _this=S.one(e.target);
            var cl_tag=D.html(D.first(D.parent(_this))),cl_tag_index=S.indexOf(cl_tag,old_tages);
            if(cl_tag_index<0){
                return;
            }else{

                old_tages.splice(cl_tag_index,1);
            }
            D.remove(D.parent(_this,'span'));
            D.val("#id_language",old_tages.join(","));
        });
    });
});
