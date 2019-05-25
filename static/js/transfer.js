// JavaScript Document

$(document).ready(function(){
	/*
	* logout
	*/
	$('#logout').click(function(){
		var urlLogout = $('#logout').val();
		$(location).attr('href',urlLogout);
	})
	
	function requestRateUpdate(){
		/*
		 get rate
		*/
		
		$.ajax({
		url:'http://localhost:5000/rate',
		type:'GET',
		dataType:'json',
		cache: false,
		success:function(data){
			$('#rateSet').val(data.rate.convertRate);
		},
		complete: function(data){
			setTimeout(requestRateUpdate, 10000);
		}
	});
	}
	
	function requestUpdate(){
		
		$.ajax({
		url:'http://localhost:5000/transfer/user',
		type:'GET',
		dataType:'json',
		cache: false,
		success:function(data){
			var tday = '';
			$.each(data.transactions, function(idex,i){
				tday += '<tr><td>'+i.usAmount+'</td><td>'+i.gdAmount+'</td><td>'+i.transferDate+'</td><td>'+"<a href='http://localhost:5000'>report</a>"+'</td></tr>';
			});
			$('#loadData').html(tday);
		},
		complete: function(data){
			setTimeout(requestUpdate, 30000);
		}
	});
	}
	
	//call function
	requestUpdate();
	requestRateUpdate();
	/*
	transaction side
	*/
	
	$('#transferAmount').submit(function(e){
		e.preventDefault();
		var received = $("input[name=amountReceived]").val();
		var rate = $("input[name=rateSet]").val();
		var given = $("input[name=amountGiven]").val();
		var url = 'http://localhost:5000/convert';
		var formData = {
			'usamount':received,
			'rateSet':rate
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
				console.log(data.message);
				$('#amountToGive').val(data.gdAmount);
				requestUpdate();
			},
			fail:function(){
				alert("failed")
			}
			
		});
		
	});
	
	/*
	* simple calculator - need to be changed because it is too messy
	*/
	$("#equal").click(function(){
		var result = $('#result').val();
		$('#result').val(eval(result));
	})
	$("#clear").click(function(){
		$('#result').val(0);
		//alert('testing');
	});
	$("#add").click(function(){
		var result = $('#result').val();
		$('#result').val(result+"+");
		//alert('testing');
	});
	$("#multiply").click(function(){
		var result = $('#result').val();
		$('#result').val(result+"*");
		//alert('testing');
	});
	$("#minus").click(function(){
		var result = $('#result').val();
		$('#result').val(result+"-");
		//alert('testing');
	});
	$("#divide").click(function(){
		var result = $('#result').val();
		$('#result').val(result+"/");
		//alert('testing');
	});
	$("#one").click(function(){
		var result = $('#result').val();
		var num = $('#one').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#two").click(function(){
		var result = $('#result').val();
		var num = $('#two').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#three").click(function(){
		var result = $('#result').val();
		var num = $('#three').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#four").click(function(){
		var result = $('#result').val();
		var num = $('#four').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#five").click(function(){
		var result = $('#result').val();
		var num = $('#five').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#six").click(function(){
		var result = $('#result').val();
		var num = $('#six').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#seven").click(function(){
		var result = $('#result').val();
		var num = $('#seven').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#eight").click(function(){
		var result = $('#result').val();
		var num = $('#eight').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#nine").click(function(){
		var result = $('#result').val();
		var num = $('#nine').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	$("#zero").click(function(){
		var result = $('#result').val();
		var num = $('#zero').val();
		$('#result').val(result+num);
		//alert('testing');
	});
	/*
	*logout if page not being used
	*/
	var idleTime = 0;
	var idleInterval = setInterval(timerIncrement, 60000);
	$(this).mousemove(function(e){
		idleTime = 0;
	});
	$(this).keypress(function(e){
		idleTime = 0;
	});
	
	function timerIncrement(){
		idleTime = idleTime+1;
		if(idleTime > 19){
			$(location).attr("href",'http://localhost:5000/logout');
		}
	}
});