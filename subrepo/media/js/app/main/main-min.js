KISSY.ready(function(a){a.add(function(){},{requires:["js/mods/search"]});a.use("switchable,dom,event,js/mods/overlayer,sizzle",function(c,b,g,e,f){var d=new b.Slide("#J_Slide",{effect:"none",easing:"easeOutStrong",activeTriggerCls:"current"});e.on(".d-p-projectlist li","mouseenter mouseleave",function(h){g.toggleClass(this,"current")});e.on(".d-p-index-hotmember li","mouseenter mouseleave",function(h){g.addClass(".d-p-index-hotmember li","active");g.removeClass(this,"active")})})});init_send_msg("");