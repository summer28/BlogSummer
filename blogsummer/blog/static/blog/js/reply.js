$(document).ready(function() {
//绑定回复提交事件
$('#reply_submit_btn').click(function() {
 
    //if ($("#reply_id_honeypot").val().length!=0) {alert("Stop!垃圾评论");return false;};

    if ($("#reply_id_comment").val().length==0) {alert("Error:请输入您的回复内容");$("#reply_id_comment").focus();return false;};

    //$("#id_timestamp").val(event.timeStamp);

    $.ajax({
        type: "POST",
        data: $('#reply_form').serialize(),
        url: "comments/post/",
        cache: false,
        dataType: "json",
        success: function(data){
            $("#reply_id_name").val("")
            $("#reply_id_email").val("")
            $("#reply_id_comment").val("")
            if(data["result_info"]=="success"){
                // not a fixed position ,should locate the comment reply to first

                $("#reply_form").before('<li root="'+data["root_id"] +'" role="'+data["comment_id"] +'" base="'+data["user_name"]+'">'+
                                              data["user_name"] +' 回复  '+data["reply_name"]  +' ( '+data["submit_date"]+' )：'+data["comment"] +'</li>')
                $("#reply_form").hide();
                alert("reply ok");
            }else{
                alert('error:'+data["result_info"]+" .");
            }
        },
        error: function () {
            alert("回复出错");
        }
    });
    return false;
});

//绑定回复按钮的鼠标经过事件

 $(".comment_list").on("mouseover", ".comment_content,li", function(event){
    $(this).append("<span class='reply_button'> <a href='javascript:void(0);' onclick='reply_click(this);'>回复</a></span>");
});   
  $(".comment_list").on("mouseout", ".comment_content,li", function(event){
    $(this).children(".reply_button").remove();
});   
          // $(this).children(".reply_button").remove();

});

// $(".comment_content,.comment_reply li").live("mouseover",function(){
    
//         $(this).append("<span class='reply_button'> <a href='javascript:void(0);' onclick='reply_click(this);'>回复</a></span>");
//         //$(this).children(".reply_button").remove();

// });

// });
//回复按钮点击触发的方法
function reply_click(obj){
    //获取回复按钮对应的评论或回复（DOM转成jQuery对象）
    var comment=obj.parentElement.parentElement;
    var $c=$(comment);
    //获取相关信息
    var root_id=$c.attr("root");
    var role=$c.attr("role");
    var base=$c.attr("base");

    //显示回复面板
    $("#reply_form").hide();
    $c.after($("#reply_form"));
    $("#reply_form").slideDown(200);

    //设置回复表单相关值
    $("#reply_reply_to").val(role);
    $("#reply_root_id").val(root_id);
    $("#reply_reply_name").val(base);
    return false;
}
