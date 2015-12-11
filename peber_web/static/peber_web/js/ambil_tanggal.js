$(function () {

	var data_waktu = {
		'ck_in': {},
		'ck_out': {}
	};

	//Tanggal Lahir
	$('div#tgl_lahir').datepicker();
	
	//Card Expiration Date
	$('div#expire').datepicker();
	
	// Punyaku disabling dates
	var nowTemp = new Date();
	var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);

	var checkin = $('#arrival').datepicker({
		onRender: function (date) {
			return date.valueOf() < now.valueOf() ? 'disabled' : '';
		}
	}).on('changeDate', function (ev) {
		if (ev.date.valueOf() > checkout.date.valueOf()) {
			var newDate = new Date(ev.date)
			newDate.setDate(newDate.getDate() + 1);
			checkout.setValue(newDate);
		}
		
		data_waktu.ck_in = ev.date;
		checkin.hide();

	}).data('datepicker');

	var checkout = $('#ck_out').datepicker({
		onRender: function (date) {
			return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
		}
	}).on('changeDate', function (ev) {
		data_waktu.ck_out = ev.date;
		checkout.hide();

		var a = new Date(data_waktu.ck_out),
			b = new Date(data_waktu.ck_in),
			c = 24 * 60 * 60 * 1000,
			diffDays = Math.round(Math.abs((a - b) / (c)));
		
		$kamar_pilihan.total_hari = diffDays;
		updateJumlahHari(data_waktu.ck_in, data_waktu.ck_out, $kamar_pilihan.total_hari);

	}).data('datepicker');

});

		//Fungsi update total hari 
		function updateJumlahHari(ck_in, ck_out, total_hari) {
			var teks_total_hari = $('span#for_days');
			var ket_nominal = $('span#ket_nominal');
			var nominal_harga = $('span#nominal');
			
			var harga_multi_hari = parseInt($kamar_pilihan.total_harga) * parseInt($kamar_pilihan.total_hari);
			
			$kamar_pilihan.harga_multi_hari = harga_multi_hari;
			
			teks_total_hari.html(' for ' + total_hari + ' day(s)');
			nominal_harga.html(' '+ numberWithCommas(harga_multi_hari) );
			ket_nominal.html(' ');
			
			
		}

	//Fungsi pemecah int menjadi berkoma''
	//src : http://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
	function numberWithCommas(x) {
		var parts = x.toString().split(".");
		parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		return parts.join(".");
	}
