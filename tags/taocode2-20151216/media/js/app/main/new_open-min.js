KISSY.ready(function(a){a.add(function(){},{requires:["js/mods/search"]});a.use("dom,event,sizzle",function(c,f,e){e.on(".d-p-newopen tr","mouseenter mouseleave",function(h){f.toggleClass(this,"hover")});e.on(".d-p-update tr","mouseenter mouseleave",function(h){f.toggleClass(this,"hover")});var g=c.trim(f.val(".d-p-languagesearch .search-text"));e.on(".d-p-languagesearch .search-text","focusin focusout",function(h){if(h.type=="focusin"){f.val(this,"")}else{if(c.trim(f.val(this))==""){f.val(this,g)}}});e.on(".d-p-languagesearch .search-btn","click",function(h){if(c.trim(f.val(".d-p-languagesearch .search-text"))==g){return}window.location.href="/project/lang/list/"+c.trim(f.val(".d-p-languagesearch .search-text"))+"/1/"});var d=[],b=[];c.each(c.query(".d-p-languagelist a"),function(h){d.push(f.html(h).toUpperCase());b.push(f.attr(h,"href"))});e.on(".d-p-languagesearch .search-text","valuechange",function(l){var i="";if(l.newVal==""){c.each(d,function(o,n){i+="<li><a href="+d[n]+">"+o+"</a></li>"});f.html(".d-p-languagelist",i);return}else{var m=[],j=[];if(l.newVal==""){return}var h=l.newVal.replace(/([\+\*\?\.\[\]])/g,"\\$1");var k=new RegExp("^"+h.toUpperCase()+".*");c.each(d,function(o,n){if(k.test(o)){m.push(o);j.push(b[n])}});c.each(m,function(o,n){i+="<li><a href="+j[n]+">"+o+"</a></li>"});f.html(".d-p-languagelist",i)}})})});
