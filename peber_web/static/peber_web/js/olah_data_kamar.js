		var $kamar_pilihan = {
			'superior': 0,
			'deluxe': 0,
			'bussiness': 0,
			'executive': 0,
			'suite': 0,
			'jlh_sup': 0,
			'jlh_del': 0,
			'jlh_bis': 0,
			'jlh_exe': 0,
			'jlh_suite': 0,
			'total_harga':0
		}; 

		$(document).ready(function(){												
			
			//Update isi $kamar_pilihan
			$('div#kontrol div').on('change', 'label input',  function(e) {
				
				var harga_kamar = $(this).val(),
						tipe_kamar = $(this).attr('tipe'),
						no_kamar = $(this).attr('id'),
						select_jlh = $('div#kontrol div#'+no_kamar+' select'),
						selected_num = select_jlh.val();
				
				console.log(tipe_kamar);
				
				select_jlh.on('change', function(e){
					var jlh_kamar = $(this).val();					
					updateDataKamar((jlh_kamar*harga_kamar), tipe_kamar, jlh_kamar);
					console.log(jlh_kamar);
				});
				
				if($(this).is(':checked')) {		
						select_jlh.val(1);
						updateDataKamar(harga_kamar, tipe_kamar, 1);
				} else {					
						updateDataKamar(0, tipe_kamar, 0);					
				}
				
								
				
			});
			
			//End of ready
		});
		  
/*
	TODO
	Untuk Mengolah Data kamar yang akan di kirim pada halaman reservation.php
*/
		function updateDataKamar(harga, tipe_kamar, jlh_kamar){	
			harga = parseInt(harga);
			
			var badge_tipe_kamar = $('div#tipe_terpilih div');
			
			if(tipe_kamar == 'Superior') {				
				$kamar_pilihan.superior = harga;
				$kamar_pilihan.jlh_sup = jlh_kamar;
				
				if(jlh_kamar > 0){
					if(jlh_kamar == 1) {
						badge_tipe_kamar.append('<span id="superior" class="badge">Superior <span>('+jlh_kamar+')</span></span>');
					} else {
						$('div#tipe_terpilih span#superior').addClass('badge').html('Superior <span>('+jlh_kamar+')</span>');
					}					
				} else {
					$('div#tipe_terpilih span#superior').remove();
				}
					
			} else if(tipe_kamar == 'Deluxe') {
				$kamar_pilihan.deluxe = harga;
				$kamar_pilihan.jlh_del = parseInt(jlh_kamar);
				if(jlh_kamar > 0){
					if(jlh_kamar == 1) {
						badge_tipe_kamar.append('<span id="deluxe" class="badge">Deluxe <span>('+jlh_kamar+')</span></span>');
					} else {
						$('div#tipe_terpilih span#deluxe').addClass('badge').html('Deluxe <span>('+jlh_kamar+')</span>');
					}					
				} else {
					$('div#tipe_terpilih span#deluxe').remove();
				}
			}  else if(tipe_kamar == 'Bussiness') {
					$kamar_pilihan.bussiness = harga;
					$kamar_pilihan.jlh_bis = jlh_kamar;
					if(jlh_kamar > 0){
					if(jlh_kamar == 1) {
						badge_tipe_kamar.append('<span id="bussiness" class="badge">Bussiness <span>('+jlh_kamar+')</span></span>');
					} else {
						$('div#tipe_terpilih span#bussiness').addClass('badge').html('Bussiness <span>('+jlh_kamar+')</span>');
					}					
				} else {
					$('div#tipe_terpilih span#bussiness').remove();
				}
				
			} else if(tipe_kamar == 'Executive') {
					$kamar_pilihan.executive = harga;
					$kamar_pilihan.jlh_exe = jlh_kamar;
				if(jlh_kamar > 0){
					if(jlh_kamar == 1) {
						badge_tipe_kamar.append('<span id="executive" class="badge">Executive <span>('+jlh_kamar+')</span></span>');
					} else {
						$('div#tipe_terpilih span#executive').addClass('badge').html('Executive <span>('+jlh_kamar+')</span>');
					}					
				} else {
					$('div#tipe_terpilih span#executive').remove();
				}
				
			}  else if(tipe_kamar == 'Suite') {
					$kamar_pilihan.suite = harga;
					$kamar_pilihan.jlh_suite = jlh_kamar;
				if(jlh_kamar > 0){
					if(jlh_kamar == 1) {
						badge_tipe_kamar.append('<span id="suite" class="badge">Suite <span>('+jlh_kamar+')</span></span>');
					} else {
						$('div#tipe_terpilih span#suite').addClass('badge').html('Suite <span>('+jlh_kamar+')</span>');
					}					
				} else {
					$('div#tipe_terpilih span#suite').remove();
				}
				
			} 
			//End of parkaro if if
			
			var total_harga = 0;
			var i = 0;		
			$.each($kamar_pilihan, function(idx, nilai){
				
				//Hanya tambah total_harga hingga index 4 (0-4), selanjutnya adalah data per kamar
				if(i<5){
					total_harga+=nilai;					
				} else {
					return true;
				}
				
				i++;
				
			});
			
			$kamar_pilihan.total_harga = total_harga;
			
			$('div#total_harga span h3 span#nominal').html(''+ numberWithCommas(total_harga));
			
			console.log('Data Kamar Pilihan : ' + JSON.stringify($kamar_pilihan));
			
		}  