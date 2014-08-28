KISSY.use("dom,event,sizzle", function (S,D,E) {
    E.on(".name-text","focusin focusout",function(e){
        if(e.type=="focusin"){
            D.val(this,"");
        }else if(e.type="focusout"){
            if(D.val(this)==""){
                D.val(this,"name");
//                D.attr(this,{type:"text"});
            }
        }
    });
    E.on(".password-text","focusin focusout",function(e){
        if(e.type=="focusin"){
            D.val(this,"");
            D.attr(this,{type:"password"});
        }else if(e.type="focusout"){
            if(D.val(this)==""){
                D.val(this,"password");
                D.attr(this,{type:"text"});
            }
        }
    });
});