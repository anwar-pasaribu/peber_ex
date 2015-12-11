		
		var data = { }; //Object for store all data

		$(document).ready(function(e){
			
			var urlBooking = "php-engine/proses_booking_multi.php";
			
			var id_cust = $('input#id_cust');
			var no_kamar = $('input#no_kamar');
			var arrival = $('input#arrival');
			var checkout = $('input#checkout');
			var tipe_booking = $('input#tipe_booking');
						
			var tBooking = tipe_booking.val();
				
				if(tBooking == "") {
					tBooking = "Normal";	
				} else {
					tBooking = "Discount";
				}
			
			var nama = $('input#nama');
			var tgl_lahir = $('input#tgl_lahir');
			var telepon = $('input#telepon');
			var email = $('input#email');
			var negara = $('input#negara');
			var kota = $('input#kota');
			var alamat = $('input#alamat');
			
			var card_number = $('input#card_number');
			var name_on_card = $('input#name_on_card');
			var expire = $('input#expire');
			var security_code = $('input#security_code');
			
			var step1 = $('div#reservasi_step1');
			var step2 = $('div#reservasi_step2');
			var step3 = $('div#reservasi_step3');
			
			var btn_edit1 = $('a#edit_step1');
			var btn_edit2 = $('a#edit_step2');
			var btn_edit3 = $('a#edit_step3');
			
			var kirimData = $('button#kirimData');
			
		
				
			$('button#simpan_data_kamar').click(function(e){
				e.preventDefault(e);				
				
				data.id_cust = id_cust.val();
				data.no_kamar = no_kamar.val();
				data.arrival = arrival.val();
				data.checkout = checkout.val();
				data.tipe_booking = tBooking;
				
				console.log(JSON.stringify(data));
				
				step1.slideToggle(500);
				btn_edit1.removeClass('hidden');
				
			});
			
			$('button#simpan_data_personal').click(function(e){
				e.preventDefault(e);
				
				data.nama = nama.val();
				data.tgl_lahir = tgl_lahir.val();
				data.telepon = telepon.val();
				data.email = email.val();
				data.negara = negara.val();
				data.kota = kota.val();
				data.alamat = alamat.val();
				
				console.log(JSON.stringify(data));
				
				step2.slideToggle(500);
				btn_edit2.removeClass('hidden');
				
			});
			
			$('button#simpan_data_pembayaran').click(function(e){
				e.preventDefault(e);
				
				data.card_number = card_number.val();
				data.name_on_card = name_on_card.val();
				data.expire = expire.val();
				data.security_code = security_code.val();
				
				console.log(JSON.stringify(data));
				
				step3.slideToggle(500);
				btn_edit3.removeClass('hidden');
				
			});
			
			btn_edit1.click(function(e) {
				step1.slideToggle(200);
				btn_edit1.addClass('hidden');
			});
			btn_edit2.click(function(e) {
				step2.slideToggle(200);
				btn_edit2.addClass('hidden');
			});
			btn_edit3.click(function(e) {
				step3.slideToggle(200);
				btn_edit3.addClass('hidden');
			});
			
			kirimData.click(function(e) {
				
				data.id_cust = id_cust.val();
				data.no_kamar = no_kamar.val();
				data.arrival = arrival.val();
				data.checkout = checkout.val();
				data.tipe_booking = tBooking;
				
				data.nama = nama.val();
				data.tgl_lahir = tgl_lahir.val();
				data.telepon = telepon.val();
				data.email = email.val();
				data.negara = negara.val();
				data.kota = kota.val();
				data.alamat = alamat.val();
				
				data.card_number = card_number.val();
				data.name_on_card = name_on_card.val();
				data.expire = expire.val();
				data.security_code = security_code.val();
				
				var $data_total = jQuery.extend($kamar_pilihan,  data);
				
//				console.log("Final Data : " + JSON.stringify($kamar_pilihan));
//				console.log("Final Data : " + JSON.stringify(data));
//				console.log("Final Data : " + JSON.stringify($data_total));
				
				$.getJSON(urlBooking, $data_total, function(data_respon) {				
					
					console.log(JSON.stringify(data_respon));
					var respon = data_respon.response_word;
					
					if(respon == "Gagal") {
							$('p#pesanKiriman').removeClass('hidden');
							
					} else {
						alert('Berhasil');
							console.log("Data Dikirim");
							//$('p#pesanKiriman').removeClass('hidden').html("Reservasi Berhasil Dilakukan");						
							document.location.href="hasil_reservasi.php?id_cust=" + id_cust.val();
					}			
					
						
				});
				
			});
			
				
		//End of Ready function	
		})