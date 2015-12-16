function init_send_msg(uname){
    $('#send-msg').click(function(e) {
	show_send_box(e.pageX, e.pageY, uname);
    });
	$('.email').click(function(e) {
	show_send_box(e.pageX, e.pageY, $(e.target).attr("data-name"));
    });

}

function show_send_box(x, y, target) {

    if ($('body').find('#send-msg-form').length > 0) {
	return;
    } 


    var t = $("<div id='send-msg-form'style='position:absolute;'><div id='send-msg-box' class='confirm-box'>"+

   
	      "<h1>发送给<span class='username'>"+target+"</span></h1>"+

	      "<textarea id='content'class='text' style='height:50px;margin-bottom: 10px;'></textarea>"+

	      "<p><a id='send' class='button green' href='javascript:;'>发送</a>" +
	      "<a id='cancel' class='button orange' href='javascript:;'>取消</a>" +	  
	      "</p></div></div>");
    
    t.css({"top":y, "left":x});
    t.find('#cancel').click(function () {
	t.remove();
    });

    t.find('#send').click(function () {
	var c = t.find('#content').val();
	if (c.length <= 0) {
	    alert("站内信内容不能为空");
	    return;
	}

	q_get('msg/send', {'u':target, 'c':c}, function(result) {	 
	}, function() { // onfail
	    alert("发送失败");
	});
	
	t.remove();
    });
    
    $('body').append(t);
}