$(document).ready(function() {

$("#submit_btn").click(function(){
            // if ($("#id_honeypot").val().length!=0) {
            //             alert("Stop!垃圾评论");
            //             return false;
            // };
            // if ($("#id_name").val().length==0) {
            //             alert("Error:请输入您的用户名");
            //             $("#id_name").focus();
            //             return false;
            // };
            // if ($("#id_email").val().length==0) {
            //             alert("Error:请输入您的邮箱地址");
            //             $("#id_email").focus();
            //             return false;
            // };

            // var email=$("#id_email").val();
            // if(!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)){
            //     alert("Error:邮箱不正确！请重新输入");
            //     $("#id_email").focus();
            //     return false;
            // }

            // if ($("#id_comment").val().length==0){
            //     alert("Error:请输入您的评论");
            //     $("#id_comment").focus();
            //     return false;
            // };
            // $("#id_timestamp").value=event.timeStamp;
            $.ajax({
                type: "POST",
                data: $('#comment_form').serialize(),
                url: "comments/post/",
                cache: false,
                dataType: "json",
                success: function(data) {
                    //empty all the form filed 
                        $("#id_name").val("")
                        $("#id_email").val("")
                        $("#id_comment").val("")
                        if(data["result_info"]=="success"){
                                 $("#comment_start").after('<p class="comment_title">'+
                                    data["submit_date"]  +' | '+data["user_name"]  +' 评论</p>'+
                                                            '<p class="comment_content" root="{{comment.id}}"role="{{comment.id}}" base="{{comment.user_name}}">'+
                                                              data["comment"]+'</p>');
                                  // window.location.reload();
                        }else{
                           alert('error:'+data["result_info"]+" .");
                        }
                    },
                error: function () {
                    alert("评论出错");
                }
            });
});


//绑定回复提交事件
$('#submit_reply').click(function() {
    if ($("#id_honeypot_reply").val().length!=0) {alert("Stop!垃圾评论");return false;};
    if ($("#id_comment_reply").val().length==0) {alert("Error:请输入您的回复内容");$("#id_comment").focus();return false;};
    $("#id_timestamp").val(event.timeStamp);
    $.ajax({
        type: "POST",
        data: $('#reply_update_form').serialize(),
        url: "comments/post/",
        cache: false,
        dataType: "json",
       success: function(data) {

                        if(data["result_info"]=="success"){

                                  window.location.reload();
                        }else{
                           alert('error:'+data["result_info"]+" .");
                        }
                    },
                error: function () {
                    alert("评论出错");
                }
            });
});

 $(".comment_content,.comment_reply li").each(function(){
                $(this).hover(function(){
                    $(this).append("<span class='reply_button'> <a href='javascript:void(0);' onclick='reply_click(this);'>回复</a></span>");
                },function(){
                    $(this).children(".reply_button").remove();
                });
            });

            // //定位到评论位置
            // if(window.location.hash!=""){
            //     obj = document.getElementsByName(window.location.hash.split("#")[1])[0];
            //     var $obj = $(obj);
            //     $("body,html").animate({
            //       scrollTop: $obj.offset().top - 70
            //     }, 0);
            // };
        });

        //回复按钮点击事件
        function reply_click(obj){
            var comment=obj.parentElement.parentElement;
            var $c=$(comment);
            var root_id=$c.attr("root");
            var role=$c.attr("role");
            var base=$c.attr("base");
//hide the other reply_form
            $("#comment_form").hide();
            $c.after($("#comment_form"));
            $("#comment_form").slideDown(200);

            $("#reply_to").val(role);
            $("#root_id").val(root_id);
            $("#reply_name").val(base);
            return false;
        }