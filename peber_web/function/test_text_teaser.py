# coding=utf-8
__author__ = 'Anwar Pasaribu'

from peber_web.algorithms.textteaser import TextTeaser

def test():
	texts = """Kapolri Jenderal Badrodin Haiti tak menyoalkan tembakan yang dilepaskan anak buahnya saat kerusuhan antitambang di Kabupaten Banyuwangi, Jawa Timur. Insiden melukai tiga warga, satu di antaranya bocah. "Boleh-boleh saja (menembak)," kata Badrodin di Mabes Polri, Jalan Trunojoyo, Kebayoran Baru, Jakar ta Selatan, Jumat (27/11/2015). Kapolri mengatakan, seharusnya warga tak berlaku anarkis. Apalagi, pe nambangan di sana berizin. Resmi. Menurut Badrodin, saat kerusuhan posisi anak buahnya melindungi dan menjaga agar tak ada perusakan. "Siapa yang melanggar hukum harus ditindak tegas," ujar Kapolri.Dua hari lalu, ratusan warga Gunung Tumpang Pitu, Kecamatan Banyuwangi, bentrok lawan polisi. Kerusuhan pecah ketika warga coba menerobos masuk ke areal tambang milik PT Bumi Sukses Indo (BSI). Warga suda h lama memendam amarah kepada PT BSI. Mereka menuding aktivitas penambangan merusak ekosistem. Suara bising alat pengeboran pun mengganggu ketenangan warga. Belum lagi debu dari penambangan yang membu at banyak warga terserang penyakit. Komisi untuk Orang Hilang dan Korban Kekerasan (KontraS) merilis, bentrok warga dengan polisi menyebabkan tiga warga menderita luka tembak. Satu korban di antaranya anak-anak. ICH"""

	news_title = "Kapolri Bela Anak Buah di Kerusuhan Banyuwangi"
	# Masalah setelah titik harus spasi.
	text_to_summarize = texts.replace('.', '. ')

	text_teaser = TextTeaser()
	sentences = text_teaser.summarize(news_title, text_to_summarize)

	# Kalimat hasil ringkasan dipisahkan \n
	summarized = ""
	for text in sentences:
		summarized += '{0}\n'.format(text)

	print u'{0}'.format(summarized)


if __name__ == '__main__':
	"""
	Kapolri Jenderal Badrodin Haiti tak menyoalkan tembakan yang dilepaskan anak buahnya saat kerusuhan antitambang di Kabupaten Banyuwangi, Jawa Timur.
	"Boleh-boleh saja (menembak)," kata Badrodin di Mabes Polri, Jalan Trunojoyo, Kebayoran Baru, Jakarta Selatan, Jumat (27/11/2015).
	Kapolri mengatakan, seharusnya warga tak berlaku anarkis.
	Menurut Badrodin, saat kerusuhan posisi anak buahnya melindungi dan menjaga agar tak ada perusakan.
	Kerusuhan pecah ketika warga coba menerobos masuk ke areal tambang milik PT Bumi Sukses Indo (BSI).
	"""
	test()
