// JavaScript Document
$(document).ready(function(){
	$('#login-validation').on('submit', function(e){
		e.preventDefault();
		var url = 'http://localhost:5000/login';
		var email = $('#email').val();
		var password = $('#password').val();
		//e.preventDefault();
		var formData = {
			'email':email,
			'password':password
		};
		$.ajax({
			type: "POST",
			headers:{
				"accept":"application/json",
				"content-type":"application/json"
			},
			data: JSON.stringify(formData),
			dataType:'json',
			xhrFields:{
				withCredentials: true
			},
			cache:false,
			crossDomain: true,
			url: url,
			timeout:2000,
			success: function(data, status, xhr){
				console.log(data.message+" "+status+" "+xhr);
				if(xhr.status == '201'){
					$(location).attr("href",data.location);
				}
				else{
					$(location).attr("href",data.location);
				}
			},
			fail:function(){
				alert("failed")
			}
		});
	});
});