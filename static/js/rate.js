// JavaScript Document
//change rate
$(document).ready(function(){
	/*
	* logout
	*/
	$('#logout').click(function(){
		var urlLogout = $('#logout').val();
		$(location).attr('href',urlLogout);
	})
	
	
	$('#changeRate').submit(function(e){
		e.preventDefault();
		var rate = $("input[name=rateChange]").val();
		var url = 'http://localhost:5000/rate';
		var formData = {
			'rate':rate
		};
		$.ajax({
			type:"POST",
			headers:{
				"accept":"application/json",
				"content-type":"application/json"
			},
			data: JSON.stringify(formData),
			dataType:'json',
			cache:false,
			url:url,
			success:function(data){
				$(location).attr('href','http://localhost:5000/')
			},
			fail:function(){
				alert("failed")
			}
			
		});
		
	});
})