
$(document).ready(function() {
	$("#submit_btn").click(function(){
		
		$.post(
			"add_comment/",
			{
				"name":$("#name").val(),
				"email":$("#email").val(), 
				"content":$("#comment_txt").val(),
			},
			function(data)
			{	
				alert("success")
				$("p.comment_item:first").before("<p class=‘comment_item’> "+ data['name']+  "说：" + data['content'] +"</p> ")
			},
			"json"
		)
	})
})

