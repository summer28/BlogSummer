$(document).ready(function() {

$("#submit_btn").click(function(){
            if ($("#id_honeypot").val().length!=0) {
                        alert("Stop!垃圾评论");
                        return false;
            };
            if ($("#id_name").val().length==0) {
                        alert("Error:请输入您的用户名");
                        $("#id_name").focus();
                        return false;
            };
            if ($("#id_email").val().length==0) {
                        alert("Error:请输入您的邮箱地址");
                        $("#id_email").focus();
                        return false;
            };

            var email=$("#id_email").val();
            if(!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)){
                alert("Error:邮箱不正确！请重新输入");
                $("#id_email").focus();
                return false;
            }

            if ($("#id_comment").val().length==0){
                alert("Error:请输入您的评论");
                $("#id_comment").focus();
                return false;
            };
     
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


});

      
