/**
 * 通用弹出浮层
 * @Author: gaozhan
 * @Time: 12-7-24 11:38
 * @Return:
 *
 */
KISSY.add(function(S, D, E, UA, O,IO){
    function Overlayer(){};
    var content=function(title,cnt){
        return '<div class="layout tender" id="J_tender">' +
        '<div class="title">' +
        '<b>'+ title +'</b>' +
        '<a class="close" href="javascript:void(0)">关闭</a>' +
        '</div>' + cnt +
        '</div>'};
    Overlayer.show=function(title,cnt,target){
        var dialog = new O.Dialog({
            width:352,
            elStyle:{
                position: UA.ie == 6 ? "absolute" : "fixed"
            },
            bodyContent: content(title,cnt),
            mask: true,
            zIndex: 10010,
            align: {
                points: ['cc', 'cc']
            },
            closable:false,
            closeAction:"destroy"
        });
        dialog.show();
        function overlayClose(){
            S.later(function(){
                dialog.destroy();
            },50);
        }
        E.delegate('#J_tender','click','a.close',overlayClose);
        E.delegate('#J_tender','click','.affirm_add',function(){
            var oldtages,addtags=D.val("#new_tag").split(/,|，/),legal_tages=[],tagdom="";
            if(D.val("#tages")==""){
                oldtages=a=[];
            }else{
                oldtages=a=D.val("#tages").split(/,|，/);
            }
            //过滤空的
            S.each(addtags, function(item,v) {
                if(S.trim(item).length==0){
                    return;
                }else{
                    legal_tages.push(S.trim(item));
                }
            });
            oldtages=oldtages.concat(legal_tages);
            //过滤重复的
            function unique(data){
                data = data || [];
                var a = {};
                for (var i=0; i<data.length; i++) {
                    var v = data[i];
                    if (typeof(a[v]) == 'undefined'){
                        a[v] = 1;
                    }
                };
                data.length=0;
                for (var i in a){
                    data[data.length] = i;
                }
                return data;
            }
            unique(oldtages);
            D.remove(".tag");
            S.each(oldtages,function(item){
                tagdom+='<span class="p-p-project-btn tag"><span>'+item+'</span><a href="javascript:void(0);" class="close">close</a></span>';
            });
            D.insertBefore(D.create(tagdom),".addtag");
            D.val("#tages",oldtages.join(","));
            S.later(function(){
                dialog.destroy();
            },50);
        });
        E.delegate('#J_tender','click','.sendmail',function(e){
            var c= D.val("#messagecontent");
            if(c==""){
                return;
            }
            IO.post('../../ajax/msg/send/', {'u':target, 'c':c}, function(result) {
                if(result=="true"){
                    alert("发送成功！");
                }else{
                    alert("发送失败！");
                }
                S.later(function(){
                    dialog.destroy();
                },50);
            },function(){});

        });
    }
    return Overlayer;

},{requires:['dom','event','ua','overlay','ajax']});