KISSY.ready(function(a){a.add(function(){},{requires:["js/mods/search"]});a.use("dom,event,ua,sizzle",function(c,f,e,b){e.on(".radio","click",function(g){if(f.attr(c.one(g.target),"id")=="is_public"){f.style(".yestag",{display:"block"});f.style(".notag",{display:"none"})}if(f.attr(c.one(g.target),"id")=="is_private"){f.style(".notag",{display:"block"});f.style(".yestag",{display:"none"})}});e.on("#J_nfpinpai_list .text-down a","click",function(g){f.text("#license",f.text(this))});e.delegate(document,"click","#J_language_list .text-down a",function(i){var h=f.text(c.one(i.target));var g="<span><b>"+h+'</b><a href="javascript:void(0);" class="p-p-project-btn close">close</a></span>';f.html(".select_language",g);f.val("#id_language",h)});var d=[];c.each(c.query("#J_language_list a"),function(g){d.push(f.html(g).toUpperCase())});f.html("#J_language_list .text-down","");e.on(".language-text .text","valuechange",function(i){f.html("#J_language_list .text-down","");var j=[],g="";if(i.newVal==""){return}var h=new RegExp("^"+i.newVal.toUpperCase()+"w*");c.each(d,function(l,k){if(h.test(l)){j.push(l)}});c.each(j,function(l,k){g+='<a href="javascript:void(0);">'+l+"</a>"});f.html("#J_language_list .text-down",g)});e.on(".language-text .text","focusin focusout",function(g){f.toggleClass("#J_language_list","hover")});e.delegate(document,"click",".select_language .close",function(j){var i;i=f.val("#id_language").split(/,|\uff0c/);var k=c.one(j.target);var g=f.html(f.first(f.parent(k))),h=c.indexOf(g,i);if(h<0){return}else{i.splice(h,1)}f.remove(f.parent(k,"span"));f.val("#id_language",i.join(","))})})});
