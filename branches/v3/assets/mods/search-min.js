KISSY.use("dom,event,ua,sizzle",function(b,d,c,a){if(a.ie==6){c.on(".d-m-search-type","mouseenter mouseleave",function(f){d.toggleClass(this,"hover")})}c.on(".d-m-search-type li","click",function(f){d.prepend(this,".d-m-search-type-list");d.val("#type",d.attr(this,"data-type"))})});