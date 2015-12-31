# coding=utf-8
__author__ = 'Anwar Pasaribu'

from textteaser import TextTeaser

if __name__ == '__main__':
	"""
	Kapolri Jenderal Badrodin Haiti tak menyoalkan tembakan yang dilepaskan anak buahnya saat kerusuhan antitambang di Kabupaten Banyuwangi, Jawa Timur.
	"Boleh-boleh saja (menembak)," kata Badrodin di Mabes Polri, Jalan Trunojoyo, Kebayoran Baru, Jakarta Selatan, Jumat (27/11/2015).
	Kapolri mengatakan, seharusnya warga tak berlaku anarkis.
	Menurut Badrodin, saat kerusuhan posisi anak buahnya melindungi dan menjaga agar tak ada perusakan.
	Kerusuhan pecah ketika warga coba menerobos masuk ke areal tambang milik PT Bumi Sukses Indo (BSI).
	"""
	texts = """
	Kapolri Jenderal Badrodin Haiti tak menyoalkan tembakan yang dilepaskan anak buahnya saat kerusuhan antitambang di Kabupaten Banyuwangi, Jawa Timur. 
	Insiden melukai tiga warga, satu di antaranya bocah. 
	"Boleh-boleh saja (menembak)," kata Badrodin di Mabes Polri, Jalan Trunojoyo, Kebayoran Baru, Jakarta Selatan. 
	Kapolri mengatakan, seharusnya warga tak berlaku anarkis. 
	Apalagi, penambangan di sana berizin resmi. 
	Menurut Badrodin, saat kerusuhan posisi anak buahnya melindungi dan menjaga agar tak ada perusakan. 
	"Siapa yang melanggar hukum harus ditindak tegas," ujar Kapolri."""



	texts2 = """SAMPAI sekarang tidak diketahui secara pasti kapan komponis legendaris Ludwig van Beethoven dibaptis dilahirkan.  Namun hari ini, Kamis (17/12), menandai 245 tahun sejak penggubah lagu Fur Elise itu dibatpis.\n\nMomen bersejarah ini tentu saja ikut dirayakan oleh situs Google.com dengan memajang doodle bertemakan karya musik Beethoven.  Logo situs pencarian itu kini dimodifikasi sehingga setiap hurufnya terbuat dari kertas musik berisi komposisi gubahan Beethoven.\n\nPengguna yang membuka halaman beranda google.com dari desktop juga berkesempatan menikmati sebuah permainan interaktif yang tentu saja masih berkaitan karya-karya maestro asal Jerman itu.  Kehidupan Beethoven yang penuh kesialan pun dikisahkan secara jenaka dalam permainan terserbut.\n\nBeethoven adalah salah satu komposer terbaik sepanjang masa.  Gubahannya seperti Fifth Symphony, Fur Elise, Moonlight Sonata dan Ode to Joy masuk jajaran komposisi klasik paling terkenal dan berpengaruh di dunia musik.\n\nSalah satu hal yang paling mengagumkan dari Beethoven adalah fakta bahwa dia tetap menelurkan maha karya bahkan setelah pendengarannya rusak di usia 30 tahun.  Ketika meninggal dunia pada tahun 1827, Beethoven sudah dalam kondisi tuli total."""
	# Texts 2 tanpa spasi setelah comma
	texts2 = "SAMPAI sekarang tidak diketahui secara pasti kapan komponis legendaris Ludwig van Beethoven dibaptis dilahirkan.Namun hari ini, Kamis (17/12), menandai 245 tahun sejak penggubah lagu Fur Elise itu dibatpis.Momen bersejarah ini tentu saja ikut dirayakan oleh situs Google.com dengan memajang doodle bertemakan karya musik Beethoven.Logo situs pencarian itu kini dimodifikasi sehingga setiap hurufnya terbuat dari kertas musik berisi komposisi gubahan Beethoven.Pengguna yang membuka halaman beranda google.com dari desktop juga berkesempatan menikmati sebuah permainan interaktif yang tentu saja masih berkaitan karya-karya maestro asal Jerman itu.Kehidupan Beethoven yang penuh kesialan pun dikisahkan secara jenaka dalam permainan terserbut.Beethoven adalah salah satu komposer terbaik sepanjang masa.Gubahannya seperti Fifth Symphony, Fur Elise, Moonlight Sonata dan Ode to Joy masuk jajaran komposisi klasik paling terkenal dan berpengaruh di dunia musik.Salah satu hal yang paling mengagumkan dari Beethoven adalah fakta bahwa dia tetap menelurkan maha karya bahkan setelah pendengarannya rusak di usia 30 tahun.Ketika meninggal dunia pada tahun 1827, Beethoven sudah dalam kondisi tuli total."

	news_title = "Kapolri Bela Anak Buah di Kerusuhan Banyuwangi"
	news_title2 = "Google Doodle Hari Ini Rayakan Hidup dan Karya Ludwig van Beethoven"
	# Masalah setelah titik harus spasi.
	text_to_summarize = texts2.replace('.', '.')

	text_teaser = TextTeaser()
	sentences = text_teaser.summarize(news_title2, text_to_summarize)

	# Kalimat hasil ringkasan dipisahkan \n
	summarized = ""
	for text in sentences:
		summarized += '{0}\n'.format(text)

	print u'{0}'.format(summarized)
