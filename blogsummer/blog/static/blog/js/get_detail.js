$(document).ready(function(){
$("#submit_btn").click(function(){
      
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
                 $("p.comment_item:first").before("<p class=‘comment_item’> "+ data['name']+  "says：" + data['content'] +"</p> ");
            }
        );
});	
});