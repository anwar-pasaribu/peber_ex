$(document).ready(function(e) {	var search_bar = $('input#search_text');	var url_search_res = "/peber_web/search/";	//Pencarian pada base.html	search_bar.on('keyup keypress',function(e){		console.log('Keyword: '+ search_bar.val());		$.ajax({			type: "POST",			url: url_search_res,			data: {				'search_text' : search_bar.val(),				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()			},			success: searchSuccess,			dataType: 'html'		});			});//End of Pencarian pada base.html	//This may require the ``json2.js`` library for older browsers.	/*var data = JSON.stringify({	    "source_publisher": "The Boston Globe",	    "source_category": "Politic",	    "source_url": "www.thebostonglobe.com"	});	var data_user = JSON.stringify({	    "bio": "Akun kedua anggun. Masalah!",	    "news_choices": [	    	"http://192.168.1.100:8000/peber_web/api/v1/news_source/19/",	    	"http://192.168.1.100:8000/peber_web/api/v1/news_source/20/"]	});	console.log(JSON.stringify(data_user));	$.ajax({	  url: 'http://192.168.1.101:8000/peber_web/api/v1/user_desc/5/',	  type: 'PUT', // POST : data baru, PUT : Update	  contentType: 'application/json',	  data: data_user,	  dataType: 'json',	  processData: false,	  success: sukses, 	  error: gagal	});*/});function sukses(data, textStatus, jqXHR){	console.log("Data berhasil ditambah", JSON.stringify(data), JSON.stringify(textStatus), JSON.stringify(jqXHR));}function gagal(data, textStatus, jqXHR){	console.log("Gagal besar", JSON.stringify(data));}function searchSuccess(data, textStatus, jqXHR) {	$("ul#rearch_results").html(data);}