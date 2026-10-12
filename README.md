# Kadın ve Çocuklara Yönelik Cinsel Saldırı Haberleri — Türkiye çapında otomatik haber haritası

**Durum:** Çalıştırılabilir başlangıç paketi. Henüz hiçbir otomatik iş kurulmadı ve hiçbir yeni haber canlı olarak taranıp doğrulanmadı. 10 eski kayıt `legacy_import_unverified` etiketiyle taşınmıştır; bunlar ayrı olarak editoryal doğrulanmalıdır.

## Mimari

`Google News RSS → bağlantıdaki tam haber metni → OpenAI yapılandırılmış çıkarım → olay eşleştirme / iki bağımsız yayıncı → sıkı doğrulama → MapTiler mahalle geocoding → data/reports.json → MapLibre heatmap (GitHub Pages)`

- Her gün 08:18 Türkiye saati (GitHub Actions zamanlayıcıları gecikebilir).
- RSS bulma: Türkiye çapında 6 sorgu. Kaynak siteler RSS yönlendirmesine, kullanım koşullarına ve paywall'a bağlıdır; Google News bağlantıları bazen asıl haberin metnine götürmez.
- `OPENAI_API_KEY` olmadan tarama **başlamaz**. API ücreti tüketebilir; `MAX_RSS_ITEMS` sınırı vardır.
- Model veri çıkarır, haberlerin gerçekliğini kesin olarak doğrulayamaz. Otomatik yayın için **iki bağımsız yayıncı**, iki makale metni, tutarlı olay anahtarı, yer ve tarih kanıtı, resmî teyit raporu, en az 0.95 model güveni, isim/kimlik riski olmaması, yetişkin mağdur ve mahalle düzeyinde eşleşen koordinat gerekir. Yüksek güven puanı tek başına yeterli değildir.
- Şüpheli olmayan veya teyitsiz kayıtlar `data/review_queue.json` içine alınır. Çocuk istismarı haberleri **otomatik yayımlanmaz**, her zaman manuel kontrolden geçmelidir.
- **Hassas konum:** yalnızca mahalle merkezi; sokak, bina, ev konumu kaydedilmez.
- **Asla suç oranı değildir:** heatmap, basında yer alan yayınlanmış haber kayıtlarının yoğunluğunu gösterir.
- Mevcut seed haberler ayrı doğrulama gerektirdiğinden `legacy_import_unverified` işaretlidir.

## Kurulum

1. Bu klasörü yeni bir **özel** GitHub deposuna yükleyin; ana dala `main` deyin. GitHub Pages ücretsiz sunumu için deponun görünürlük/plan seçeneklerini kontrol edin.
2. Repository → Settings → Secrets and variables → Actions → New repository secret:
   - `OPENAI_API_KEY` (OpenAI API, ChatGPT aboneliğinden ayrı ücretlenebilir)
   - `MAPTILER_KEY` (MapTiler public/browser key; alan adı kısıtını site açıldıktan sonra tanımlayın; GitHub Pages `*.github.io`/özel domaini ekleyin.)
3. Settings → Actions → General → Workflow permissions → **Read and write permissions** seçin (daily workflow JSON dosyalarına commit atar).
4. Settings → Pages → Source → **GitHub Actions** seçin.
5. Actions sekmesinden önce `Publish GitHub Pages`, sonra `Daily national news verification` işlerini `Run workflow` ile test edin.
6. Deponun `main` dalındaki `data/reports.json` güncellenir, Pages aynı veriyi otomatik yayımlar. İsterseniz yerelde `cp config.example.js config.js` ve API key'i ayarlayın; `python -m http.server 8000` ile `http://localhost:8000` açın (file:// üzerinden fetch çalışmaz).

## Başlangıç için güvenlik adımları

- Otomatik yayını açmadan önce içerik denetim paneli ve **editoryal onay süreci** eklemek güçlü biçimde önerilir. İki bağımsız kaynak ve model güven puanı hatayı sıfırlamaz. Şu anki prototip bu eşiği geçerse otomatik yayın yapacak şekilde yapılandırılmıştır.
- Yayın öncesi GDPR/KVKK, telif hakları, kaynak kullanım koşulları ve hukuki sorumluluk için inceleme yaptırın.
- API anahtarını HTML içine sabit yazmayın; Pages derleme aşamasında `config.js` oluşturulur. Harita tarayıcı anahtarları kullanıcı tarafından görülebilir; bu normaldir, **domain/usage restrictions** kullanın. OpenAI key asla tarayıcıya gönderilmez.
- Otomatik çıkarım hassas ayrıntıları yanlış yorumlayabilir. Yayına çıktığında geri bildirim/itiraz, kayıt kaldırma ve düzeltme süreci kurun.
- Konum doğrulama, bölge/ilçe/mahalle adları aynı olan yerler için ayrıca güçlendirilmelidir.
- Haber kaynağı bağlantısı bozularak paywall ya da robots engeliyle karşılaşılırsa haber otomatik yayımlanmamalıdır.
- GitHub Pages ve GitHub Actions, kotalara ve hesap politikasına tabidir; zamanlayıcı garantili değildir.

## Dosyalar

- `index.html`: interaktif MapLibre/MapTiler, TR/EN, Mor Çatı bağış bağlantıları
- `data/reports.json`: yayımlanan haberler; başlangıçtaki 10 kayıt
- `data/review_queue.json`: eşik altında veya hassas aday haberler; **kişisel bilgiler otomatik kaydedilmez**
- `data/seen_urls.json`: taranan haber adreslerinin tekrar işlenmesini önler
- `scripts/collect.py`: günlük RSS haber taraması, OpenAI çıkarımı, teyit kapısı, konum kontrolü
- `.github/workflows/daily.yml`: günlük güncelleme
- `.github/workflows/pages.yml`: otomatik site yayınlama
- `tests/test_gate.py`: yayınlama eşiği temel testleri
- `config.example.js`: yerel geliştirme için yapılandırma şablonu

## Sınırlamalar

Bu sistem haber arşivini kapsamlı olarak temsil etmez. RSS arama verileri eksiktir. Farklı ajans adları aynı haberin sendikasyon kopyalarını gösterebilir ve basında iki haberin varlığı gerçeği hukuken kanıtlamaz. Kısıtlayıcı eşikler nedeniyle yeni haberlerin büyük bölümü inceleme kuyruğuna düşebilir; bu istenen güvenli varsayılandır. İlk sürümde uzman/insan editör tarafından örneklem denetimi ve hata değerlendirmesi yapılmadan tamamen gözetimsiz kullanım önerilmez.
