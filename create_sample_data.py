#!/usr/bin/env python3
"""
Sample data creation script for IstanbulCareAPI
Creates sample header columns and combobox items
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.header import HeaderColumn, ComboboxItem
from app.models.user import User
from app.models.blog import BlogPost
from app.models.service import Service
from app.core.security import get_password_hash
from datetime import datetime
from app.db.session import Base

def create_sample_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create admin user if not exists
        admin_user = db.query(User).filter(User.email == "admin@istanbulcare.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@istanbulcare.com",
                password_hash=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created: admin@istanbulcare.com / admin123")
        
        # Create sample header columns
        sample_columns = [
            {
                "name_tr": "Hakkımızda",
                "name_en": "About us",
                "slug": "about-us",
                "order": 1,
                "type": "link",
                "url": "/about-us",
                "has_combobox": False
            },
            {
                "name_tr": "Saç Ekimi",
                "name_en": "Hair Transplant",
                "slug": "hair-transplant",
                "order": 2,
                "type": "dropdown",
                "url": None,
                "has_combobox": True
            },
            {
                "name_tr": "Hizmetler",
                "name_en": "Services",
                "slug": "services",
                "order": 3,
                "type": "dropdown",
                "url": None,
                "has_combobox": True
            },
            {
                "name_tr": "Fiyatlandırma",
                "name_en": "Pricing",
                "slug": "pricing",
                "order": 4,
                "type": "link",
                "url": "/pricing",
                "has_combobox": False
            },
            {
                "name_tr": "Makaleler",
                "name_en": "Article",
                "slug": "articles",
                "order": 5,
                "type": "link",
                "url": "/articles",
                "has_combobox": False
            },
            {
                "name_tr": "SSS",
                "name_en": "FAQ",
                "slug": "faq",
                "order": 6,
                "type": "link",
                "url": "/faq",
                "has_combobox": False
            },
            {
                "name_tr": "İletişim",
                "name_en": "Contact us",
                "slug": "contact",
                "order": 7,
                "type": "link",
                "url": "/contact",
                "has_combobox": False
            }
        ]
        
        # Create header columns
        for col_data in sample_columns:
            existing = db.query(HeaderColumn).filter(HeaderColumn.slug == col_data["slug"]).first()
            if not existing:
                column = HeaderColumn(**col_data)
                db.add(column)
                db.commit()
                print(f"Header column created: {col_data['name_en']}")
        
        # Get header columns for combobox items
        hair_transplant_col = db.query(HeaderColumn).filter(HeaderColumn.slug == "hair-transplant").first()
        services_col = db.query(HeaderColumn).filter(HeaderColumn.slug == "services").first()
        
        # Create combobox items for Hair Transplant
        if hair_transplant_col:
            hair_transplant_items = [
                {
                    "header_column_id": hair_transplant_col.id,
                    "name_tr": "DHI Saç Ekimi",
                    "name_en": "DHI Hair Transplant",
                    "slug": "dhi-hair-transplant",
                    "url": "/hair-transplant/dhi",
                    "order": 1
                },
                {
                    "header_column_id": hair_transplant_col.id,
                    "name_tr": "FUE Saç Ekimi",
                    "name_en": "FUE Hair Transplant",
                    "slug": "fue-hair-transplant",
                    "url": "/hair-transplant/fue",
                    "order": 2
                },
                {
                    "header_column_id": hair_transplant_col.id,
                    "name_tr": "Sapphire FUE",
                    "name_en": "Sapphire FUE",
                    "slug": "sapphire-fue",
                    "url": "/hair-transplant/sapphire-fue",
                    "order": 3
                },
                {
                    "header_column_id": hair_transplant_col.id,
                    "name_tr": "Saç Ekimi Fiyatları",
                    "name_en": "Hair Transplant Prices",
                    "slug": "hair-transplant-prices",
                    "url": "/hair-transplant/prices",
                    "order": 4
                }
            ]
            
            for item_data in hair_transplant_items:
                existing = db.query(ComboboxItem).filter(
                    ComboboxItem.slug == item_data["slug"],
                    ComboboxItem.header_column_id == item_data["header_column_id"]
                ).first()
                if not existing:
                    item = ComboboxItem(**item_data)
                    db.add(item)
                    db.commit()
                    print(f"Combobox item created: {item_data['name_en']}")
        
        # Create combobox items for Services
        if services_col:
            services_items = [
                {
                    "header_column_id": services_col.id,
                    "name_tr": "Saç Ekimi",
                    "name_en": "Hair Transplant",
                    "slug": "hair-transplant-service",
                    "url": "/services/hair-transplant",
                    "order": 1
                },
                {
                    "header_column_id": services_col.id,
                    "name_tr": "Estetik Cerrahi",
                    "name_en": "Aesthetic Surgery",
                    "slug": "aesthetic-surgery",
                    "url": "/services/aesthetic-surgery",
                    "order": 2
                },
                {
                    "header_column_id": services_col.id,
                    "name_tr": "Diş Tedavisi",
                    "name_en": "Dental Treatment",
                    "slug": "dental-treatment",
                    "url": "/services/dental-treatment",
                    "order": 3
                },
                {
                    "header_column_id": services_col.id,
                    "name_tr": "Göz Cerrahisi",
                    "name_en": "Eye Surgery",
                    "slug": "eye-surgery",
                    "url": "/services/eye-surgery",
                    "order": 4
                },
                {
                    "header_column_id": services_col.id,
                    "name_tr": "Ortopedi",
                    "name_en": "Orthopedics",
                    "slug": "orthopedics",
                    "url": "/services/orthopedics",
                    "order": 5
                }
            ]
            
            for item_data in services_items:
                existing = db.query(ComboboxItem).filter(
                    ComboboxItem.slug == item_data["slug"],
                    ComboboxItem.header_column_id == item_data["header_column_id"]
                ).first()
                if not existing:
                    item = ComboboxItem(**item_data)
                    db.add(item)
                    db.commit()
                    print(f"Combobox item created: {item_data['name_en']}")
        
        # Create sample blog posts
        blog_posts = [
            {
                "slug": "dhi-hair-transplant-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de DHI Saç Ekimi",
                "title_en": "DHI Hair Transplant in Turkey", 
                "title_fr": "Greffe de Cheveux DHI en Turquie",
                "description_tr": "Türkiye, gelişmiş tıbbi tesisleri, yetenekli cerrahları ve uygun fiyatları nedeniyle DHI Saç Ekimi için en iyi destinasyon haline gelmiştir.",
                "description_en": "Turkey has become a top destination for DHI Hair Transplant due to its advanced medical facilities, skilled surgeons, and affordable pricing.",
                "description_fr": "La Turquie est devenue une destination de choix pour la greffe de cheveux DHI grâce à ses installations médicales avancées, ses chirurgiens qualifiés et ses prix abordables.",
                "content_tr": "Türkiye, gelişmiş tıbbi tesisleri, yetenekli cerrahları ve uygun fiyatları nedeniyle DHI Saç Ekimi için en iyi destinasyon haline gelmiştir. Türkiye'de DHI Saç Ekimi Maliyeti, greft sayısı, klinik itibarı ve dahil edilen hizmetler gibi faktörlere bağlı olarak değişmektedir. Geleneksel yöntemlere kıyasla DHI, daha hassas ve doğal görünümlü bir sonuç sunar, bu da onu premium bir seçim haline getirir.",
                "content_en": "Turkey has become a top destination for DHI Hair Transplant due to its advanced medical facilities, skilled surgeons, and affordable pricing. The cost of a DHI Hair Transplant Cost in Turkey varies based on factors like the number of grafts, clinic reputation, and included services. Compared to traditional methods, DHI offers a more precise and natural-looking result, making it a premium choice.",
                "content_fr": "La Turquie est devenue une destination de choix pour la greffe de cheveux DHI grâce à ses installations médicales avancées, ses chirurgiens qualifiés et ses prix abordables. Le coût d'une greffe de cheveux DHI en Turquie varie en fonction de facteurs tels que le nombre de greffons, la réputation de la clinique et les services inclus. Par rapport aux méthodes traditionnelles, la DHI offre un résultat plus précis et d'apparence naturelle.",
                "featured_image_url": "https://example.com/images/dhi-hair-transplant.jpg",
                "gallery_urls": ["https://example.com/images/dhi-1.jpg", "https://example.com/images/dhi-2.jpg"]
            },
            {
                "slug": "fue-hair-transplant-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de FUE Saç Ekimi",
                "title_en": "FUE Hair Transplant in Turkey",
                "title_fr": "Greffe de Cheveux FUE en Turquie", 
                "description_tr": "FUE saç ekimi, minimal invaziv bir teknik olup, doğal görünümlü sonuçlar sağlar.",
                "description_en": "FUE hair transplant is a minimally invasive technique that provides natural-looking results.",
                "description_fr": "La greffe de cheveux FUE est une technique minimalement invasive qui offre des résultats d'apparence naturelle.",
                "content_tr": "FUE (Follicular Unit Extraction) saç ekimi, günümüzde en popüler saç ekimi yöntemlerinden biridir. Bu teknik, saç foliküllerinin tek tek çıkarılması ve hedef bölgeye nakledilmesi prensibine dayanır. Türkiye'de FUE saç ekimi, yüksek kaliteli hizmet ve uygun fiyatlarla sunulmaktadır.",
                "content_en": "FUE (Follicular Unit Extraction) hair transplant is one of the most popular hair transplant methods today. This technique is based on the principle of individually extracting hair follicles and transplanting them to the target area. FUE hair transplant in Turkey is offered with high-quality service and affordable prices.",
                "content_fr": "La greffe de cheveux FUE (Follicular Unit Extraction) est l'une des méthodes de greffe de cheveux les plus populaires aujourd'hui. Cette technique est basée sur le principe d'extraire individuellement les follicules pileux et de les transplanter dans la zone cible. La greffe de cheveux FUE en Turquie est proposée avec un service de haute qualité et des prix abordables.",
                "featured_image_url": "https://example.com/images/fue-hair-transplant.jpg",
                "gallery_urls": ["https://example.com/images/fue-1.jpg", "https://example.com/images/fue-2.jpg"]
            },
            {
                "slug": "sapphire-fue-hair-transplant",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Sapphire FUE Saç Ekimi",
                "title_en": "Sapphire FUE Hair Transplant",
                "title_fr": "Greffe de Cheveux Sapphire FUE",
                "description_tr": "Sapphire FUE, safir bıçaklar kullanılarak yapılan gelişmiş bir saç ekimi tekniğidir.",
                "description_en": "Sapphire FUE is an advanced hair transplant technique performed using sapphire blades.",
                "description_fr": "La FUE Sapphire est une technique avancée de greffe de cheveux réalisée avec des lames en saphir.",
                "content_tr": "Sapphire FUE saç ekimi, geleneksel FUE tekniğinin geliştirilmiş versiyonudur. Bu yöntemde, kanal açma işlemi için safir bıçaklar kullanılır. Safir bıçakların keskin ve pürüzsüz yüzeyi sayesinde, daha hassas kanallar açılabilir ve iyileşme süreci hızlanır.",
                "content_en": "Sapphire FUE hair transplant is an improved version of the traditional FUE technique. In this method, sapphire blades are used for channel opening. Thanks to the sharp and smooth surface of sapphire blades, more precise channels can be opened and the healing process is accelerated.",
                "content_fr": "La greffe de cheveux Sapphire FUE est une version améliorée de la technique FUE traditionnelle. Dans cette méthode, des lames en saphir sont utilisées pour l'ouverture des canaux. Grâce à la surface tranchante et lisse des lames en saphir, des canaux plus précis peuvent être ouverts et le processus de guérison est accéléré.",
                "featured_image_url": "https://example.com/images/sapphire-fue.jpg",
                "gallery_urls": ["https://example.com/images/sapphire-1.jpg", "https://example.com/images/sapphire-2.jpg"]
            },
            {
                "slug": "hollywood-smile-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Hollywood Gülüş",
                "title_en": "Hollywood Smile in Turkey",
                "title_fr": "Sourire Hollywood en Turquie",
                "description_tr": "Hollywood gülüş, mükemmel beyaz ve düzgün dişlerle ünlü olan estetik diş tedavisidir.",
                "description_en": "Hollywood smile is an aesthetic dental treatment famous for perfect white and straight teeth.",
                "description_fr": "Le sourire Hollywood est un traitement dentaire esthétique célèbre pour des dents parfaitement blanches et droites.",
                "content_tr": "Hollywood gülüş, ünlülerin sahip olduğu mükemmel gülümsemeyi elde etmek için uygulanan kapsamlı bir estetik diş tedavisidir. Bu tedavi, diş beyazlatma, porselen veneer, diş eti estetiği ve gerektiğinde ortodontik tedavileri içerir. Türkiye'de Hollywood gülüş tedavisi, dünya standartlarında kaliteli hizmet ve uygun fiyatlarla sunulmaktadır. Deneyimli diş hekimleri ve modern teknoloji ile mükemmel sonuçlar elde edilmektedir.",
                "content_en": "Hollywood smile is a comprehensive aesthetic dental treatment applied to achieve the perfect smile that celebrities have. This treatment includes teeth whitening, porcelain veneers, gum aesthetics, and orthodontic treatments when necessary. Hollywood smile treatment in Turkey is offered with world-standard quality service and affordable prices. Perfect results are achieved with experienced dentists and modern technology.",
                "content_fr": "Le sourire Hollywood est un traitement dentaire esthétique complet appliqué pour obtenir le sourire parfait que possèdent les célébrités. Ce traitement comprend le blanchiment des dents, les facettes en porcelaine, l'esthétique des gencives et les traitements orthodontiques si nécessaire. Le traitement du sourire Hollywood en Turquie est proposé avec un service de qualité aux normes mondiales et des prix abordables.",
                "featured_image_url": "https://example.com/images/hollywood-smile.jpg",
                "gallery_urls": ["https://example.com/images/hollywood-1.jpg", "https://example.com/images/hollywood-2.jpg"]
            },
            {
                "slug": "emax-veneers-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de E-max Veneer",
                "title_en": "E-max Veneers in Turkey",
                "title_fr": "Facettes E-max en Turquie",
                "description_tr": "E-max veneer, üstün estetik ve dayanıklılık sunan modern porselen kaplama sistemidir.",
                "description_en": "E-max veneers are modern porcelain coating systems that offer superior aesthetics and durability.",
                "description_fr": "Les facettes E-max sont des systèmes de revêtement en porcelaine modernes qui offrent une esthétique et une durabilité supérieures.",
                "content_tr": "E-max veneer, lityum disilikat seramikten üretilen son teknoloji porselen kaplamadır. Geleneksel porselen kaplamalara göre daha dayanıklı, şeffaf ve doğal görünümlüdür. E-max veneer tedavisi, minimum diş kesimi ile maksimum estetik sonuç elde etmeyi sağlar. Türkiye'de E-max veneer uygulamaları, uzman diş hekimleri tarafından dijital teknoloji kullanılarak yapılmaktadır. Bu sayede hastalar kısa sürede mükemmel gülümsemeye kavuşmaktadır.",
                "content_en": "E-max veneers are state-of-the-art porcelain coatings made from lithium disilicate ceramic. They are more durable, transparent, and natural-looking compared to traditional porcelain coatings. E-max veneer treatment allows achieving maximum aesthetic results with minimal tooth cutting. E-max veneer applications in Turkey are performed by specialist dentists using digital technology. This way, patients achieve perfect smiles in a short time.",
                "content_fr": "Les facettes E-max sont des revêtements en porcelaine de pointe fabriqués à partir de céramique de disilicate de lithium. Elles sont plus durables, transparentes et d'apparence naturelle par rapport aux revêtements en porcelaine traditionnels. Le traitement des facettes E-max permet d'obtenir des résultats esthétiques maximaux avec une coupe dentaire minimale.",
                "featured_image_url": "https://example.com/images/emax-veneers.jpg",
                "gallery_urls": ["https://example.com/images/emax-1.jpg", "https://example.com/images/emax-2.jpg"]
            },
            {
                "slug": "dental-implant-treatment-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de İmplant Tedavisi",
                "title_en": "Implant Treatment in Turkey",
                "title_fr": "Traitement d'Implant en Turquie",
                "description_tr": "Diş implantı, eksik dişlerin yerine yerleştirilen titanyum vidalar ile kalıcı çözüm sunar.",
                "description_en": "Dental implants provide a permanent solution with titanium screws placed in place of missing teeth.",
                "description_fr": "Les implants dentaires offrent une solution permanente avec des vis en titane placées à la place des dents manquantes.",
                "content_tr": "Diş implantı, kayıp dişlerin yerine yerleştirilen titanyum köklü yapay dişlerdir. İmplant tedavisi, çene kemiğine yerleştirilen titanyum vida üzerine porselen kronun sabitlenmesi ile tamamlanır. Bu tedavi, doğal dişlere en yakın fonksiyon ve estetiği sağlar. Türkiye'de implant tedavisi, İsviçre ve Almanya menşeli kaliteli implant sistemleri ile yapılmaktadır. Deneyimli oral cerrahlar ve modern ameliyathaneler sayesinde yüksek başarı oranları elde edilmektedir.",
                "content_en": "Dental implants are artificial teeth with titanium roots placed in place of lost teeth. Implant treatment is completed by fixing a porcelain crown on a titanium screw placed in the jawbone. This treatment provides the closest function and aesthetics to natural teeth. Implant treatment in Turkey is performed with quality implant systems from Switzerland and Germany. High success rates are achieved thanks to experienced oral surgeons and modern operating rooms.",
                "content_fr": "Les implants dentaires sont des dents artificielles avec des racines en titane placées à la place des dents perdues. Le traitement d'implant est complété en fixant une couronne en porcelaine sur une vis en titane placée dans l'os de la mâchoire. Ce traitement offre la fonction et l'esthétique les plus proches des dents naturelles.",
                "featured_image_url": "https://example.com/images/dental-implant.jpg",
                "gallery_urls": ["https://example.com/images/implant-1.jpg", "https://example.com/images/implant-2.jpg"]
            },
            {
                "slug": "brazilian-butt-lift-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Brazilian Butt Lift",
                "title_en": "Brazilian Butt Lift in Turkey",
                "title_fr": "Brazilian Butt Lift en Turquie",
                "description_tr": "Brazilian Butt Lift, kalça bölgesine doğal görünüm kazandıran popüler estetik cerrahi işlemidir.",
                "description_en": "Brazilian Butt Lift is a popular aesthetic surgery procedure that gives a natural appearance to the hip area.",
                "description_fr": "Le Brazilian Butt Lift est une procédure de chirurgie esthétique populaire qui donne un aspect naturel à la région des hanches.",
                "content_tr": "Brazilian Butt Lift (BBL), vücudun farklı bölgelerinden alınan yağların kalça bölgesine transfer edilmesi ile yapılan estetik cerrahi işlemidir. Bu işlem, kalçalarda doğal görünümlü hacim artışı sağlar. Türkiye'de BBL operasyonları, deneyimli plastik cerrahlar tarafından güvenli şekilde gerçekleştirilmektedir. İşlem, liposuction ile yağ alımı ve ardından kalça bölgesine yağ enjeksiyonu olmak üzere iki aşamadan oluşur.",
                "content_en": "Brazilian Butt Lift (BBL) is an aesthetic surgery procedure performed by transferring fat taken from different parts of the body to the hip area. This procedure provides a natural-looking volume increase in the hips. BBL operations in Turkey are performed safely by experienced plastic surgeons. The procedure consists of two stages: fat removal with liposuction and then fat injection into the hip area.",
                "content_fr": "Le Brazilian Butt Lift (BBL) est une procédure de chirurgie esthétique réalisée en transférant la graisse prélevée sur différentes parties du corps vers la région des hanches. Cette procédure offre une augmentation de volume d'apparence naturelle dans les hanches. Les opérations BBL en Turquie sont réalisées en toute sécurité par des chirurgiens plasticiens expérimentés.",
                "featured_image_url": "https://example.com/images/brazilian-butt-lift.jpg",
                "gallery_urls": ["https://example.com/images/bbl-1.jpg", "https://example.com/images/bbl-2.jpg"]
            },
            {
                "slug": "breast-augmentation-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Meme Büyütme",
                "title_en": "Breast Augmentation in Turkey",
                "title_fr": "Augmentation Mammaire en Turquie",
                "description_tr": "Meme büyütme ameliyatı, silikon implantlar ile meme hacmini artıran estetik cerrahi işlemidir.",
                "description_en": "Breast augmentation surgery is an aesthetic surgery procedure that increases breast volume with silicone implants.",
                "description_fr": "La chirurgie d'augmentation mammaire est une procédure de chirurgie esthétique qui augmente le volume des seins avec des implants en silicone.",
                "content_tr": "Meme büyütme ameliyatı, kadınların meme hacmini artırmak ve şeklini düzeltmek için tercih ettiği popüler bir estetik cerrahi işlemidir. Türkiye'de meme büyütme operasyonları, FDA onaylı kaliteli silikon implantlar kullanılarak yapılmaktadır. Deneyimli plastik cerrahlar, hastanın vücut yapısına en uygun implant boyutunu belirleyerek doğal görünümlü sonuçlar elde etmektedir. İşlem genel anestezi altında yaklaşık 1-2 saat sürmektedir.",
                "content_en": "Breast augmentation surgery is a popular aesthetic surgery procedure preferred by women to increase breast volume and correct shape. Breast augmentation operations in Turkey are performed using FDA-approved quality silicone implants. Experienced plastic surgeons achieve natural-looking results by determining the most suitable implant size for the patient's body structure. The procedure takes approximately 1-2 hours under general anesthesia.",
                "content_fr": "La chirurgie d'augmentation mammaire est une procédure de chirurgie esthétique populaire préférée par les femmes pour augmenter le volume des seins et corriger la forme. Les opérations d'augmentation mammaire en Turquie sont réalisées en utilisant des implants en silicone de qualité approuvés par la FDA.",
                "featured_image_url": "https://example.com/images/breast-augmentation.jpg",
                "gallery_urls": ["https://example.com/images/breast-aug-1.jpg", "https://example.com/images/breast-aug-2.jpg"]
            },
            {
                "slug": "breast-lift-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Meme Dikleştirme",
                "title_en": "Breast Lift in Turkey",
                "title_fr": "Lifting des Seins en Turquie",
                "description_tr": "Meme dikleştirme ameliyatı, sarkmış memeleri yeniden şekillendiren estetik cerrahi işlemidir.",
                "description_en": "Breast lift surgery is an aesthetic surgery procedure that reshapes sagging breasts.",
                "description_fr": "La chirurgie de lifting des seins est une procédure de chirurgie esthétique qui remodèle les seins affaissés.",
                "content_tr": "Meme dikleştirme (mastopexy) ameliyatı, yaşlanma, hamilelik, emzirme veya genetik faktörler nedeniyle sarkmış olan memelerin yeniden şekillendirilmesi için uygulanan estetik cerrahi işlemidir. Türkiye'de meme dikleştirme operasyonları, modern teknikler kullanılarak minimal skar ile yapılmaktadır. İşlem sırasında fazla deri çıkarılır ve meme dokusu yeniden konumlandırılır. Sonuç olarak daha genç ve dik görünümlü memeler elde edilir.",
                "content_en": "Breast lift (mastopexy) surgery is an aesthetic surgery procedure applied for reshaping breasts that have sagged due to aging, pregnancy, breastfeeding, or genetic factors. Breast lift operations in Turkey are performed with minimal scarring using modern techniques. During the procedure, excess skin is removed and breast tissue is repositioned. As a result, younger and more upright-looking breasts are achieved.",
                "content_fr": "La chirurgie de lifting des seins (mastopexie) est une procédure de chirurgie esthétique appliquée pour remodeler les seins qui se sont affaissés en raison du vieillissement, de la grossesse, de l'allaitement ou de facteurs génétiques. Les opérations de lifting des seins en Turquie sont réalisées avec des cicatrices minimales en utilisant des techniques modernes.",
                "featured_image_url": "https://example.com/images/breast-lift.jpg",
                "gallery_urls": ["https://example.com/images/breast-lift-1.jpg", "https://example.com/images/breast-lift-2.jpg"]
            },
            {
                "slug": "breast-reduction-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Meme Küçültme",
                "title_en": "Breast Reduction in Turkey",
                "title_fr": "Réduction Mammaire en Turquie",
                "description_tr": "Meme küçültme ameliyatı, büyük memelerin neden olduğu fiziksel ve estetik sorunları çözen cerrahi işlemdir.",
                "description_en": "Breast reduction surgery is a surgical procedure that solves physical and aesthetic problems caused by large breasts.",
                "description_fr": "La chirurgie de réduction mammaire est une procédure chirurgicale qui résout les problèmes physiques et esthétiques causés par de gros seins.",
                "content_tr": "Meme küçültme ameliyatı, aşırı büyük memelerin neden olduğu sırt ağrısı, boyun ağrısı, postür bozuklukları ve estetik kaygıları gidermek için yapılan cerrahi işlemdir. Türkiye'de meme küçültme operasyonları, deneyimli plastik cerrahlar tarafından güvenli şekilde gerçekleştirilmektedir. İşlem sırasında fazla meme dokusu ve deri çıkarılarak, memelere daha orantılı ve estetik bir görünüm kazandırılır. Aynı zamanda meme başı ve areola da yeniden konumlandırılır.",
                "content_en": "Breast reduction surgery is a surgical procedure performed to eliminate back pain, neck pain, posture disorders, and aesthetic concerns caused by excessively large breasts. Breast reduction operations in Turkey are performed safely by experienced plastic surgeons. During the procedure, excess breast tissue and skin are removed, giving the breasts a more proportional and aesthetic appearance. At the same time, the nipple and areola are also repositioned.",
                "content_fr": "La chirurgie de réduction mammaire est une procédure chirurgicale réalisée pour éliminer les douleurs dorsales, les douleurs cervicales, les troubles de la posture et les préoccupations esthétiques causés par des seins excessivement gros. Les opérations de réduction mammaire en Turquie sont réalisées en toute sécurité par des chirurgiens plasticiens expérimentés.",
                "featured_image_url": "https://example.com/images/breast-reduction.jpg",
                "gallery_urls": ["https://example.com/images/breast-red-1.jpg", "https://example.com/images/breast-red-2.jpg"]
            },
            {
                "slug": "ear-reshaping-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Kulak Estetiği",
                "title_en": "Ear Reshaping in Turkey",
                "title_fr": "Remodelage d'Oreille en Turquie",
                "description_tr": "Kulak estetiği, çıkık kulakları düzelten ve kulak şeklini iyileştiren cerrahi işlemdir.",
                "description_en": "Ear reshaping is a surgical procedure that corrects protruding ears and improves ear shape.",
                "description_fr": "Le remodelage d'oreille est une procédure chirurgicale qui corrige les oreilles décollées et améliore la forme de l'oreille.",
                "content_tr": "Kulak estetiği (otoplasti), çıkık kulakları düzeltmek ve kulak şeklini iyileştirmek için yapılan estetik cerrahi işlemidir. Türkiye'de kulak estetiği operasyonları, hem çocuklarda hem de yetişkinlerde başarıyla uygulanmaktadır. İşlem genellikle kulak arkasından yapılan küçük bir kesi ile gerçekleştirilir ve skar görünmez kalır. Kulak kıkırdağı yeniden şekillendirilir ve kulaklar kafaya daha yakın konumlandırılır. Operasyon yaklaşık 1-2 saat sürer ve genellikle lokal anestezi ile yapılır.",
                "content_en": "Ear reshaping (otoplasty) is an aesthetic surgery procedure performed to correct protruding ears and improve ear shape. Ear reshaping operations in Turkey are successfully applied in both children and adults. The procedure is usually performed with a small incision made behind the ear and the scar remains invisible. The ear cartilage is reshaped and the ears are positioned closer to the head. The operation takes approximately 1-2 hours and is usually performed under local anesthesia.",
                "content_fr": "Le remodelage d'oreille (otoplastie) est une procédure de chirurgie esthétique réalisée pour corriger les oreilles décollées et améliorer la forme de l'oreille. Les opérations de remodelage d'oreille en Turquie sont appliquées avec succès chez les enfants et les adultes.",
                "featured_image_url": "https://example.com/images/ear-reshaping.jpg",
                "gallery_urls": ["https://example.com/images/ear-1.jpg", "https://example.com/images/ear-2.jpg"]
            },
            {
                "slug": "facelift-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Yüz Germe",
                "title_en": "Facelift in Turkey",
                "title_fr": "Lifting du Visage en Turquie",
                "description_tr": "Yüz germe ameliyatı, yaşlanma belirtilerini gidererek yüze genç görünüm kazandıran cerrahi işlemdir.",
                "description_en": "Facelift surgery is a surgical procedure that gives the face a youthful appearance by eliminating signs of aging.",
                "description_fr": "La chirurgie de lifting du visage est une procédure chirurgicale qui donne au visage une apparence jeune en éliminant les signes du vieillissement.",
                "content_tr": "Yüz germe (facelift) ameliyatı, yaşlanmanın yüzde oluşturduğu sarkmaları, kırışıklıkları ve hacim kaybını gidermek için yapılan estetik cerrahi işlemidir. Türkiye'de yüz germe operasyonları, modern teknikler kullanılarak doğal görünümlü sonuçlar elde edilecek şekilde yapılmaktadır. İşlem sırasında yüz kasları gerilerek yeniden konumlandırılır, fazla deri çıkarılır ve yüz hatları keskinleştirilir. Mini facelift, orta yüz germe ve tam yüz germe gibi farklı teknikler hastanın ihtiyacına göre uygulanır.",
                "content_en": "Facelift surgery is an aesthetic surgery procedure performed to eliminate sagging, wrinkles, and volume loss caused by aging on the face. Facelift operations in Turkey are performed using modern techniques to achieve natural-looking results. During the procedure, facial muscles are stretched and repositioned, excess skin is removed, and facial contours are sharpened. Different techniques such as mini facelift, mid-face lift, and full facelift are applied according to the patient's needs.",
                "content_fr": "La chirurgie de lifting du visage est une procédure de chirurgie esthétique réalisée pour éliminer l'affaissement, les rides et la perte de volume causés par le vieillissement sur le visage. Les opérations de lifting du visage en Turquie sont réalisées en utilisant des techniques modernes pour obtenir des résultats d'apparence naturelle.",
                "featured_image_url": "https://example.com/images/facelift.jpg",
                "gallery_urls": ["https://example.com/images/facelift-1.jpg", "https://example.com/images/facelift-2.jpg"]
            },
            {
                "slug": "rhinoplasty-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Burun Estetiği",
                "title_en": "Rhinoplasty in Turkey",
                "title_fr": "Rhinoplastie en Turquie",
                "description_tr": "Burun estetiği, burun şeklini ve fonksiyonunu iyileştiren popüler estetik cerrahi işlemidir.",
                "description_en": "Rhinoplasty is a popular aesthetic surgery procedure that improves nose shape and function.",
                "description_fr": "La rhinoplastie est une procédure de chirurgie esthétique populaire qui améliore la forme et la fonction du nez.",
                "content_tr": "Burun estetiği (rinoplasti), burun şeklini düzeltmek ve nefes alma fonksiyonunu iyileştirmek için yapılan estetik cerrahi işlemidir. Türkiye'de burun estetiği operasyonları, dünya çapında tanınan deneyimli plastik cerrahlar tarafından gerçekleştirilmektedir. Açık ve kapalı teknik olmak üzere iki farklı yöntem kullanılır. İşlem sırasında burun kemiği ve kıkırdağı yeniden şekillendirilir. Piezo tekniği gibi modern yöntemler sayesinde daha az travma ile daha hızlı iyileşme sağlanır.",
                "content_en": "Rhinoplasty is an aesthetic surgery procedure performed to correct nose shape and improve breathing function. Rhinoplasty operations in Turkey are performed by world-renowned experienced plastic surgeons. Two different methods are used: open and closed techniques. During the procedure, the nasal bone and cartilage are reshaped. Thanks to modern methods such as Piezo technique, faster healing is achieved with less trauma.",
                "content_fr": "La rhinoplastie est une procédure de chirurgie esthétique réalisée pour corriger la forme du nez et améliorer la fonction respiratoire. Les opérations de rhinoplastie en Turquie sont réalisées par des chirurgiens plasticiens expérimentés de renommée mondiale.",
                "featured_image_url": "https://example.com/images/rhinoplasty.jpg",
                "gallery_urls": ["https://example.com/images/rhinoplasty-1.jpg", "https://example.com/images/rhinoplasty-2.jpg"]
            },
            {
                "slug": "sleeve-gastrectomy-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Sleeve Gastrektomi",
                "title_en": "Sleeve Gastrectomy in Turkey",
                "title_fr": "Gastrectomie en Manchon en Turquie",
                "description_tr": "Sleeve gastrektomi, obezite tedavisinde kullanılan etkili bariatrik cerrahi yöntemidir.",
                "description_en": "Sleeve gastrectomy is an effective bariatric surgery method used in obesity treatment.",
                "description_fr": "La gastrectomie en manchon est une méthode de chirurgie bariatrique efficace utilisée dans le traitement de l'obésité.",
                "content_tr": "Sleeve gastrektomi (tüp mide), morbid obezite tedavisinde kullanılan en popüler bariatrik cerrahi yöntemlerinden biridir. Türkiye'de sleeve gastrektomi operasyonları, deneyimli bariatrik cerrahlar tarafından laparoskopik yöntemle güvenli şekilde yapılmaktadır. İşlem sırasında midenin yaklaşık %80'i çıkarılarak mide hacmi küçültülür. Bu sayede hasta daha az yemek yiyerek kilo verir. Operasyon sonrası hastalar ortalama 2-3 yılda fazla kilolarının %60-80'ini kaybeder.",
                "content_en": "Sleeve gastrectomy (tube stomach) is one of the most popular bariatric surgery methods used in morbid obesity treatment. Sleeve gastrectomy operations in Turkey are performed safely by experienced bariatric surgeons using laparoscopic method. During the procedure, approximately 80% of the stomach is removed, reducing stomach volume. This way, the patient loses weight by eating less food. After the operation, patients lose 60-80% of their excess weight in an average of 2-3 years.",
                "content_fr": "La gastrectomie en manchon (estomac tubulaire) est l'une des méthodes de chirurgie bariatrique les plus populaires utilisées dans le traitement de l'obésité morbide. Les opérations de gastrectomie en manchon en Turquie sont réalisées en toute sécurité par des chirurgiens bariatriques expérimentés utilisant la méthode laparoscopique.",
                "featured_image_url": "https://example.com/images/sleeve-gastrectomy.jpg",
                "gallery_urls": ["https://example.com/images/sleeve-1.jpg", "https://example.com/images/sleeve-2.jpg"]
            },
            {
                "slug": "gastric-balloon-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Mide Balonu",
                "title_en": "Gastric Balloon in Turkey",
                "title_fr": "Ballon Gastrique en Turquie",
                "description_tr": "Mide balonu, ameliyatsız kilo verme yöntemi olarak uygulanan non-invaziv obezite tedavisidir.",
                "description_en": "Gastric balloon is a non-invasive obesity treatment applied as a non-surgical weight loss method.",
                "description_fr": "Le ballon gastrique est un traitement de l'obésité non invasif appliqué comme méthode de perte de poids non chirurgicale.",
                "content_tr": "Mide balonu, ameliyat gerektirmeyen obezite tedavi yöntemlerinden biridir. Türkiye'de mide balonu uygulamaları, endoskopik yöntemle güvenli şekilde yapılmaktadır. İşlem sırasında silikon bir balon mideye yerleştirilir ve serum fizyolojik ile şişirilir. Balon mide hacminin bir kısmını kaplayarak tokluk hissini artırır ve kişinin daha az yemek yemesini sağlar. Balon 6-12 ay süreyle mide içinde kalır ve sonrasında çıkarılır. Bu sürede hastalar ortalama 15-25 kg kilo verebilir.",
                "content_en": "Gastric balloon is one of the obesity treatment methods that does not require surgery. Gastric balloon applications in Turkey are performed safely with endoscopic method. During the procedure, a silicone balloon is placed in the stomach and inflated with saline solution. The balloon covers part of the stomach volume, increasing the feeling of satiety and allowing the person to eat less food. The balloon remains in the stomach for 6-12 months and is then removed. During this period, patients can lose an average of 15-25 kg.",
                "content_fr": "Le ballon gastrique est l'une des méthodes de traitement de l'obésité qui ne nécessite pas de chirurgie. Les applications de ballon gastrique en Turquie sont réalisées en toute sécurité avec la méthode endoscopique.",
                "featured_image_url": "https://example.com/images/gastric-balloon.jpg",
                "gallery_urls": ["https://example.com/images/balloon-1.jpg", "https://example.com/images/balloon-2.jpg"]
            },
            {
                "slug": "gastric-band-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Mide Bandı",
                "title_en": "Gastric Band in Turkey",
                "title_fr": "Anneau Gastrique en Turquie",
                "description_tr": "Mide bandı, ayarlanabilir silikon band ile mide hacmini küçülten bariatrik cerrahi yöntemidir.",
                "description_en": "Gastric band is a bariatric surgery method that reduces stomach volume with an adjustable silicone band.",
                "description_fr": "L'anneau gastrique est une méthode de chirurgie bariatrique qui réduit le volume de l'estomac avec un anneau en silicone ajustable.",
                "content_tr": "Mide bandı (gastrik bant), obezite tedavisinde kullanılan ayarlanabilir bariatrik cerrahi yöntemlerinden biridir. Türkiye'de mide bandı operasyonları, laparoskopik teknikle minimal invaziv şekilde yapılmaktadır. İşlem sırasında midenin üst kısmına ayarlanabilir silikon bir band yerleştirilir. Bu band mide girişini daraltarak yemek alımını kısıtlar. Bandın sıkılığı deri altına yerleştirilen port aracılığıyla ayarlanabilir. Mide bandı geri dönüşümlü bir işlemdir ve gerektiğinde çıkarılabilir.",
                "content_en": "Gastric band is one of the adjustable bariatric surgery methods used in obesity treatment. Gastric band operations in Turkey are performed minimally invasively with laparoscopic technique. During the procedure, an adjustable silicone band is placed on the upper part of the stomach. This band restricts food intake by narrowing the stomach entrance. The tightness of the band can be adjusted through a port placed under the skin. Gastric band is a reversible procedure and can be removed when necessary.",
                "content_fr": "L'anneau gastrique est l'une des méthodes de chirurgie bariatrique ajustables utilisées dans le traitement de l'obésité. Les opérations d'anneau gastrique en Turquie sont réalisées de manière minimalement invasive avec la technique laparoscopique.",
                "featured_image_url": "https://example.com/images/gastric-band.jpg",
                "gallery_urls": ["https://example.com/images/band-1.jpg", "https://example.com/images/band-2.jpg"]
            },
            {
                "slug": "gastric-bypass-turkey",
                "author_id": admin_user.id,
                "published_date": datetime.now(),
                "title_tr": "Türkiye'de Mide Bypass",
                "title_en": "Gastric Bypass in Turkey",
                "title_fr": "Bypass Gastrique en Turquie",
                "description_tr": "Mide bypass, mide ve bağırsak sistemini yeniden düzenleyen etkili bariatrik cerrahi yöntemidir.",
                "description_en": "Gastric bypass is an effective bariatric surgery method that reorganizes the stomach and intestinal system.",
                "description_fr": "Le bypass gastrique est une méthode de chirurgie bariatrique efficace qui réorganise l'estomac et le système intestinal.",
                "content_tr": "Mide bypass (gastrik bypass), morbid obezite tedavisinde kullanılan en etkili bariatrik cerrahi yöntemlerinden biridir. Türkiye'de mide bypass operasyonları, deneyimli cerrahlar tarafından laparoskopik yöntemle güvenli şekilde yapılmaktadır. İşlem sırasında mide küçültülür ve ince bağırsağın bir kısmı atlanarak yeni bir bağlantı oluşturulur. Bu sayede hem besin alımı kısıtlanır hem de emilim azaltılır. Mide bypass sonrası hastalar 2-3 yılda fazla kilolarının %70-90'ını kaybedebilir.",
                "content_en": "Gastric bypass is one of the most effective bariatric surgery methods used in morbid obesity treatment. Gastric bypass operations in Turkey are performed safely by experienced surgeons using laparoscopic method. During the procedure, the stomach is reduced and a new connection is created by bypassing part of the small intestine. This way, both food intake is restricted and absorption is reduced. After gastric bypass, patients can lose 70-90% of their excess weight in 2-3 years.",
                "content_fr": "Le bypass gastrique est l'une des méthodes de chirurgie bariatrique les plus efficaces utilisées dans le traitement de l'obésité morbide. Les opérations de bypass gastrique en Turquie sont réalisées en toute sécurité par des chirurgiens expérimentés utilisant la méthode laparoscopique.",
                "featured_image_url": "https://example.com/images/gastric-bypass.jpg",
                "gallery_urls": ["https://example.com/images/bypass-1.jpg", "https://example.com/images/bypass-2.jpg"]
            }
        ]
        
        for post_data in blog_posts:
            existing = db.query(BlogPost).filter(BlogPost.slug == post_data["slug"]).first()
            if not existing:
                post = BlogPost(**post_data)
                db.add(post)
                db.commit()
                print(f"Blog post created: {post_data['title_en']}")
        
        print("\nSample data created successfully!")
        print("\nCreated:")
        print("- Admin user: admin@istanbulcare.com / admin123")
        print("- 7 Header columns (About us, Hair Transplant, Services, etc.)")
        print("- 9 Combobox items (DHI, FUE, Services subcategories)")
        print("- 15 Multilingual blog posts:")
        print("  * Hair Transplant: DHI, FUE, Sapphire FUE")
        print("  * Dental Treatment: Hollywood Smile, E-max Veneers, Implant Treatment")
        print("  * Plastic Surgery: Brazilian Butt Lift, Breast Augmentation, Breast Lift, Breast Reduction, Ear Reshaping, Facelift, Rhinoplasty")
        print("  * Obesity Treatment: Sleeve Gastrectomy, Gastric Balloon, Gastric Band, Gastric Bypass")
        
        # Create sample services
        services_data = [
            {
                "slug": "dhi-hair-transplant",
                "title_tr": "DHI Saç Ekimi",
                "title_en": "DHI Hair Transplant",
                "description_tr": "DHI tekniği ile doğal görünümlü saç ekimi",
                "description_en": "Natural-looking hair transplant with DHI technique",
                "content_tr": "DHI (Direct Hair Implantation) saç ekimi tekniği, saç foliküllerinin özel kalemler ile direkt olarak ekildiği gelişmiş bir yöntemdir.",
                "content_en": "DHI (Direct Hair Implantation) hair transplant technique is an advanced method where hair follicles are directly implanted using special pens.",
                "price": 2500.00,
                "duration": "6-8 saat",
                "is_active": True
            },
            {
                "slug": "fue-hair-transplant",
                "title_tr": "FUE Saç Ekimi",
                "title_en": "FUE Hair Transplant",
                "description_tr": "FUE tekniği ile minimal invaziv saç ekimi",
                "description_en": "Minimally invasive hair transplant with FUE technique",
                "content_tr": "FUE (Follicular Unit Extraction) saç ekimi, saç foliküllerinin tek tek çıkarılarak hedef bölgeye nakledildiği popüler bir yöntemdir.",
                "content_en": "FUE (Follicular Unit Extraction) hair transplant is a popular method where hair follicles are individually extracted and transplanted to the target area.",
                "price": 2000.00,
                "duration": "5-7 saat",
                "is_active": True
            },
            {
                "slug": "sapphire-fue-hair-transplant",
                "title_tr": "Sapphire FUE Saç Ekimi",
                "title_en": "Sapphire FUE Hair Transplant",
                "description_tr": "Safir bıçaklar ile premium saç ekimi",
                "description_en": "Premium hair transplant with sapphire blades",
                "content_tr": "Sapphire FUE saç ekimi, safir bıçakların kullanıldığı gelişmiş FUE tekniğidir. Daha hassas kanallar ve hızlı iyileşme sağlar.",
                "content_en": "Sapphire FUE hair transplant is an advanced FUE technique using sapphire blades. It provides more precise channels and faster healing.",
                "price": 3000.00,
                "duration": "6-8 saat",
                "is_active": True
            },
            {
                "slug": "beard-transplant",
                "title_tr": "Sakal Ekimi",
                "title_en": "Beard Transplant",
                "description_tr": "Doğal görünümlü sakal ekimi",
                "description_en": "Natural-looking beard transplant",
                "content_tr": "Sakal ekimi, saç foliküllerinin sakal bölgesine nakledilmesi ile yapılan estetik işlemdir.",
                "content_en": "Beard transplant is an aesthetic procedure performed by transplanting hair follicles to the beard area.",
                "price": 1500.00,
                "duration": "4-6 saat",
                "is_active": True
            },
            {
                "slug": "eyebrow-transplant",
                "title_tr": "Kaş Ekimi",
                "title_en": "Eyebrow Transplant",
                "description_tr": "Doğal kaş çizgisi oluşturma",
                "description_en": "Creating natural eyebrow line",
                "content_tr": "Kaş ekimi, ince saç foliküllerinin kaş bölgesine nakledilmesi ile yapılan hassas bir işlemdir.",
                "content_en": "Eyebrow transplant is a delicate procedure performed by transplanting fine hair follicles to the eyebrow area.",
                "price": 1200.00,
                "duration": "3-4 saat",
                "is_active": True
            },
            {
                "slug": "woman-hair-transplant",
                "title_tr": "Kadın Saç Ekimi",
                "title_en": "Woman Hair Transplant",
                "description_tr": "Kadınlara özel saç ekimi çözümleri",
                "description_en": "Hair transplant solutions specifically for women",
                "content_tr": "Kadın saç ekimi, kadınların saç dökülme problemlerine özel olarak tasarlanmış saç ekimi yöntemleridir.",
                "content_en": "Woman hair transplant is hair transplant methods specifically designed for women's hair loss problems.",
                "price": 2800.00,
                "duration": "6-8 saat",
                "is_active": True
            },
            {
                "slug": "afro-hair-transplant",
                "title_tr": "Afro Saç Ekimi",
                "title_en": "Afro Hair Transplant",
                "description_tr": "Kıvırcık saç yapısına özel saç ekimi",
                "description_en": "Hair transplant specialized for curly hair structure",
                "content_tr": "Afro saç ekimi, kıvırcık ve kalın saç yapısına sahip kişiler için özel tekniklerle yapılan saç ekimi işlemidir.",
                "content_en": "Afro hair transplant is a hair transplant procedure performed with special techniques for people with curly and thick hair structure.",
                "price": 3200.00,
                "duration": "7-9 saat",
                "is_active": True
            },
            {
                "slug": "hair-transplant-turkey",
                "title_tr": "Türkiye'de Saç Ekimi",
                "title_en": "Hair Transplant in Turkey",
                "description_tr": "Türkiye'de kaliteli ve uygun fiyatlı saç ekimi",
                "description_en": "Quality and affordable hair transplant in Turkey",
                "content_tr": "Türkiye, dünya çapında tanınan saç ekimi merkezleri ve deneyimli doktorları ile saç ekimi turizminde lider konumdadır.",
                "content_en": "Turkey is a leader in hair transplant tourism with its world-renowned hair transplant centers and experienced doctors.",
                "price": 2200.00,
                "duration": "6-8 saat",
                "is_active": True
            },
            {
                "slug": "hair-transplant-albania",
                "title_tr": "Arnavutluk'ta Saç Ekimi",
                "title_en": "Hair Transplant in Albania",
                "description_tr": "Arnavutluk'ta profesyonel saç ekimi hizmetleri",
                "description_en": "Professional hair transplant services in Albania",
                "content_tr": "Arnavutluk'ta modern teknikler ve deneyimli ekiplerle kaliteli saç ekimi hizmetleri sunulmaktadır.",
                "content_en": "Quality hair transplant services are offered in Albania with modern techniques and experienced teams.",
                "price": 1800.00,
                "duration": "5-7 saat",
                "is_active": True
            }
        ]
        
        for service_data in services_data:
            existing = db.query(Service).filter(Service.slug == service_data["slug"]).first()
            if not existing:
                service = Service(**service_data)
                db.add(service)
                db.commit()
                print(f"Service created: {service_data['title_en']}")
        
        print("- 9 Hair Transplant Services (DHI, FUE, Sapphire FUE, Beard, Eyebrow, Woman, Afro, Turkey, Albania)")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
