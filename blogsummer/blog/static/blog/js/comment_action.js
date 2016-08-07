$(document).ready(function(){
        $("#submit_btn").click(function(){
              
              	if ($("#name").val().length==0) {
                        alert("Error:请输入您的用户名");
                        $("#id_name").focus();
                        return false;
                };
                if ($("#email").val().length==0) {
                        alert("Error:请输入您的邮箱地址");
                        $("#id_email").focus();
                        return false;
                };

                if(!$("#email").val().match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)){
        	        alert("Error:邮箱不正确！请重新输入");
        	        $("#email").focus();
        	        return false;
                }

                if ($("#content").val().length==0){
                    	alert("Error:请输入您的评论");
                    	$("#content").focus();
                   	 return false;
                };

                $.post(
                     "comment/",
                     {
                         name:$("#name").val(),
                         email:$("#email").val(), 
                         content:$("#content").val()
                     },
                     function(data)
                     {   	
                 	$("#name").attr("value",'');
                 	$("#email").attr("value",'');
                 	$("#content").attr("value",'');
                         $("span.locate_comment").after("<p class=‘comment_list_item’> "+ data['name']+  " says：" + data['content'] +"</p> ");

                    }
                );
        });



 //回复_鼠标经过
        $(".comment_list_item,.comment_reply li").each(function(){
                $(this).hover(function(){
                    $(this).append("<span class='reply_button'> <a href='javascript:void(0);' onclick='reply_click(this);'>回复</a></span>");
                },function(){
                    $(this).children(".reply_button").remove();
                });
        });	
         //回复按钮点击事件
        function reply_click(obj){
            var comment=obj.parentElement.parentElement;
            var $c=$(comment);
            var root=$c.attr("root");
            var role=$c.attr("role");
            var base=$c.attr("base");

            $("#reply_form").hide();
            $c.after($("#reply_form"));
            $("#reply_form").slideDown(200);

            $("#reply_to").val(role);
            $("#root_id").val(root);
            $("#reply_name").val(base);
            return false;
        }
});