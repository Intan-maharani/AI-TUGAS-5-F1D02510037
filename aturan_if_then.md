# Ringkasan Aturan

1. R1: IF radiasi matahari tinggi THEN potensi surya. (S1)
2. R2: IF potensi surya AND lahan terbuka THEN rekomendasi surya. (S2)
3. R3: IF angin kencang THEN potensi angin. (S1)
4. R4: IF potensi angin AND area terbuka THEN rekomendasi angin. (S3)
5. R5: IF aliran air stabil THEN potensi hidro. (S1)
6. R6: IF potensi hidro AND beda ketinggian/kondisi aliran sesuai THEN rekomendasi hidro. (S3)
7. R7: IF limbah organik tersedia THEN potensi biomassa. (S1)
8. R8: IF potensi biomassa AND pengumpulan limbah teratur THEN rekomendasi biomassa. (S3)
9. R9: IF indikasi panas bumi THEN potensi geotermal. (S1)
10. R10: IF potensi geotermal AND akses jaringan listrik memungkinkan THEN rekomendasi geotermal. (S4)

Semua aturan memakai mode DAN. Rantai aturan terjadi karena hasil R1/R3/R5/R7/R9 menjadi premis bagi aturan berikutnya.
