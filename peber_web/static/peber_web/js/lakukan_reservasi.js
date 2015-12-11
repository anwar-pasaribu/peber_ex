	


$(document).ready(function () {

	$('a#continue').click(function (e) {
		e.preventDefault();
		var teks_awal = "Continue Reservation";
		var teks_summary = "Show Summary";
		var tombol = $(this);
		var teks_judul = $('h1#judul_halaman');
		var judul_reservasi = "Reservation Form";
		var judul_awal = "Available Rooms";
		var pesan_no_kamar = $('p#pesan_no_kamar');
		
		//Menuju Form Reservasi : Kondisi Awal Tombol Jadi Biru
		if(tombol.text() == teks_awal) {				
			
			//Jika  ada kamar terpilih, tampilkan form
			if($kamar_pilihan.total_harga != 0) {
				
				$(this).text(teks_summary)
				.removeClass('btn-success')
				.addClass('btn-info');
				
				$('div#list_kamar').fadeToggle(300);
				$('div#reservation_container').fadeToggle(300);
				
				teks_judul.text(judul_reservasi);
				pesan_no_kamar.slideUp(200);
			
				//Jika tidak ada kamar terpilih tampilkan pesan p#pesan_no_kamar
			} else {
				
				pesan_no_kamar.slideDown(200);
				
			}
			
		//Kondisi Dua Tombol Jadi Hijau	
		} else if (tombol.text() == teks_summary) {
				$(this).text(teks_awal)
				.removeClass('btn-info')
				.addClass('btn-success');
			
				$('div#list_kamar').fadeToggle(300);
				$('div#reservation_container').fadeToggle(300);
			
				teks_judul.text(judul_awal);
			
		}

		
	//End a.click function for beralih ke form reservation
	});
	
	//PROMOTION CODE
	//Tombol Utk Aktivasi Kode Jika Ada
	$('button#cek_promo').click(function() {
		
		var url_promo = "php-engine/cek_promo.php";
		var kode = $('input#tipe_booking').val();;
		var ck_in = $('input#arrival').val();
		
		if(ck_in == "") {
			alert('Uncknow Check in date ...');
			return true;
			
		}
		
		var kode_promo = {
			kode_promo : kode
		};
		
		$.getJSON(
			url_promo,
			kode_promo,
			function(data_json) {
				console.log(JSON.stringify(data_json));
				if(data_json.length == 1) {
					
					//Penghitungan diskon
						$.each(data_json, function(idx, data_promo){
							
							var nilai = data_promo.nilai/100; // Jika Kode Menghasilkan Diskon
							var keterangan = data_promo.keterangan;
							
							console.log('Nilai : ' + nilai + '\nKet : ' + keterangan);
											
							if (keterangan == "Discount") {
								
								var harga_multi_hari = parseInt($kamar_pilihan.total_hari) * parseInt($kamar_pilihan.total_harga);
								var potongan_harga = harga_multi_hari * nilai;
								var harga_diskon = harga_multi_hari - potongan_harga;
								
								console.log('\nHarga Multi Hari : ' + harga_multi_hari + '\nPotongan : ' + potongan_harga + '\nHarga Diskon : ' + harga_diskon);
								
								//Tambah Dat $kamar_pilihan
								$kamar_pilihan.harga_diskon = harga_diskon;
								
								$('div#total_harga span h3 span#nominal')
								.append('<br><small style="color : #56CD65;">Discount : '+ numberWithCommas($kamar_pilihan.harga_diskon) + '</span>');
								
								console.log($kamar_pilihan.total_harga);
								
								$('input#tipe_booking').attr('disabled','disabled');
								$('button#cek_promo').attr('disabled','disabled');
								
								$('span#konfirmasi_promo')
								.show()
								.text(data_promo.nilai + '% ' +data_promo.keterangan+ ' , Successfully added.')
								.css('color','#56CD65');						
							//Jika Tidak Ada Promo yang didapatkan
							} else {
								$('span#konfirmasi_promo')
								.show()
								.text('Promo code not available')
								.css('color','#923D2D');
							}
							
						});		
					} else {
						$('span#konfirmasi_promo')
								.show()
								.text('No promo with ' + kode + ' code')
								.css('color','#923D2D');
					}
				
				
				
			}); 
		//End of getJSON
		
		console.log('Looking for ' + kode_promo + ' code ... ');
		
	});


//End of ready function
});