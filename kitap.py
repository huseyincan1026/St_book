import pandas as pd 
import streamlit as st

# CSV dosyasını oku
df = pd.read_csv('https://raw.githubusercontent.com/scostap/goodreads_bbe_dataset/refs/heads/main/Best_Books_Ever_dataset/books_1.Best_Books_Ever.csv')

# Gereksiz verileri veri setinden çıkar
df = df.drop(['bookId', 'characters', 'firstPublishDate', 'awards', 
               'numRatings', 'ratingsByStars', 'likedPercent', 
               'bbeScore', 'setting', 'bbeVotes', 'edition'], axis=1)

# NaN olan 'language' sütunlarını temizle
df.dropna(subset=['language'], inplace=True)

# 'Arabic' diline sahip olan satırları çıkar
df = df.drop(df[df.language == 'Arabic'].index)

# Kitap isimlerini ve kapak linklerini elde et
books = df.title.tolist()  # .tolist() ile listeye çeviriyoruz
authors = df.author.unique()  # Yazarları benzersiz olarak al

def link_bul():
    isim_gir = str.title(st.selectbox('Kitap ismi seçiniz...', books))
    
    if isim_gir:  # Kullanıcı bir kitap seçmişse
        selected_book = df[df.title == isim_gir]
        
        if not selected_book.empty:  # Seçilen kitap var mı?
            # Kitap bilgilerini göster
            st.markdown(
                f"<div style='text-align: center;'>"
                f"<img src='{selected_book.coverImg.iloc[0]}' style='width: 300px;'>"
                f"<h3 style='text-align: center;'>{selected_book.title.iloc[0]}</h3>"
                f"<h4 style='text-align: center;'>Yazarı: {selected_book.author.iloc[0]}</h4>"
                f"<p style='text-align: justify;'>{selected_book.description.iloc[0]}</p>"
                f"<h3 style='color: red; font-size: 23px;'>${selected_book.price.iloc[0]}</h3>"
                f"</div>", 
                unsafe_allow_html=True
            )
        else:
            st.write("Bu kitap bulunamadı.")
            
def yaz_kitap():
    yazar_gir = str.title(st.selectbox('Yazar İsmi Giriniz...', authors))
    
    if yazar_gir:  # Kullanıcı bir yazar seçmişse
        selected_books = df[df.author == yazar_gir]
        
        if not selected_books.empty:  # Seçilen yazarın kitapları var mı?
            for i in range(len(selected_books)):  
                # Resmi ortalamak için div kullanıyoruz
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<img src='{selected_books.coverImg.iloc[i]}' style='width: 300px;'>"
                    f"<h3 style='text-align: center;'>{selected_books.title.iloc[i]}</h3>"
                    f"<p style='text-align: justify;'>{selected_books.description.iloc[i]}</p>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
        else:
            st.write("Bu yazarın kitabı bulunamadı.")

# Uygulama fonksiyonlarını çağır
link_bul()
yaz_kitap()
