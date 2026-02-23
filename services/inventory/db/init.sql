CREATE TABLE IF NOT EXISTS products (
  prod_id BIGSERIAL PRIMARY KEY,
  cat_id BIGINT NOT NULL,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL,
  sku VARCHAR(80),
  short_desc TEXT,
  long_desc TEXT,
  price DECIMAL(12,0) NOT NULL,
  discount_price DECIMAL(12,0),
  warranty_months INTEGER NOT NULL DEFAULT 12,
  stock_qty INTEGER NOT NULL DEFAULT 0,
  qr_path VARCHAR(255),
  status BOOLEAN NOT NULL DEFAULT true,
  keywords VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_images (
  img_id BIGSERIAL PRIMARY KEY,
  prod_id BIGINT NOT NULL REFERENCES products(prod_id) ON DELETE CASCADE,
  img_url VARCHAR(255) NOT NULL,
  alt_text VARCHAR(150),
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_product_images_prod_id ON product_images(prod_id);

INSERT INTO products (prod_id, cat_id, name, slug, sku, short_desc, long_desc, price, discount_price, warranty_months, stock_qty, qr_path, status, keywords, created_at, updated_at) VALUES
(1, 25, 'iPhone 14 Pro Max 512GB', 'iphone_14_pro_max_512gb', 'IPHONE-14-001', 'iPhone 14 Pro Max – flagship with 6.7" display, A16 chip, 48MP camera', 'iPhone 14 Pro Max is Apple''s most powerful flagship with Super Retina XDR 6.7" display, 120Hz ProMotion, A16 Bionic chip, 48MP camera system, and Dynamic Island.', 29990000, 27990000, 12, 5, 'https://example.com/qr/1.png', true, 'iPhone 14 Pro Max', NOW(), NOW()),
(2, 25, 'iPhone 14 Pro Max 256GB', 'iphone_14_pro_max_256gb', 'IPHONE-14-002', 'iPhone 14 Pro Max 256GB – Premium flagship smartphone', 'iPhone 14 Pro Max with 256GB storage, A16 Bionic chip, ProMotion display, and advanced camera system.', 26990000, 24990000, 12, 8, 'https://example.com/qr/2.png', true, 'iPhone 14 Pro Max', NOW(), NOW()),
(3, 24, 'iPhone 14 Pro 512GB', 'iphone_14_pro_512gb', 'IPHONE-14-003', 'iPhone 14 Pro – 6.1" ProMotion display, A16 chip', 'iPhone 14 Pro features 6.1" Super Retina XDR display with ProMotion, A16 Bionic chip, and professional camera system.', 27990000, 25990000, 12, 12, 'https://example.com/qr/3.png', true, 'iPhone 14 Pro', NOW(), NOW()),
(4, 24, 'iPhone 14 Pro 256GB', 'iphone_14_pro_256gb', 'IPHONE-14-004', 'iPhone 14 Pro 256GB – Professional grade smartphone', 'iPhone 14 Pro with 256GB storage, Dynamic Island, and 48MP main camera.', 24990000, 22990000, 12, 15, 'https://example.com/qr/4.png', true, 'iPhone 14 Pro', NOW(), NOW()),
(5, 22, 'iPhone 14 256GB', 'iphone_14_256gb', 'IPHONE-14-005', 'iPhone 14 256GB – Modern design, A15 Bionic chip', 'iPhone 14 with 256GB storage, dual camera system, and all-day battery life.', 21990000, 19990000, 12, 20, 'https://example.com/qr/5.png', true, 'iPhone 14', NOW(), NOW()),
(6, 22, 'iPhone 14 128GB', 'iphone_14_128gb', 'IPHONE-14-006', 'iPhone 14 with modern design, improved camera, A15 Bionic chip', 'iPhone 14 features modern design, dual 12MP camera with larger sensor, powerful A15 Bionic chip, improved low-light photography, and 5G connectivity.', 19990000, 17990000, 12, 25, 'https://example.com/qr/6.png', true, 'iPhone 14', NOW(), NOW()),
(7, 23, 'iPhone 14 Plus 256GB', 'iphone_14_plus_256gb', 'IPHONE-14-007', 'iPhone 14 Plus – Large 6.7" display, extended battery', 'iPhone 14 Plus with 6.7" display, A15 Bionic chip, and exceptional battery life.', 23990000, 21990000, 12, 10, 'https://example.com/qr/7.png', true, 'iPhone 14 Plus', NOW(), NOW()),
(8, 23, 'iPhone 14 Plus 128GB', 'iphone_14_plus_128gb', 'IPHONE-14-008', 'iPhone 14 Plus 128GB – Big screen, big battery', 'iPhone 14 Plus features large display and longest battery life in iPhone 14 lineup.', 21990000, 19990000, 12, 18, 'https://example.com/qr/8.png', true, 'iPhone 14 Plus', NOW(), NOW()),
(9, 32, 'iPhone 13 512GB', 'iphone_13_512gb', 'IPHONE-13-009', 'iPhone 13 512GB – Maximum storage capacity', 'iPhone 13 with 512GB storage, A15 Bionic chip, and dual camera system.', 21990000, 19990000, 12, 8, 'https://example.com/qr/9.png', true, 'iPhone 13', NOW(), NOW()),
(10, 32, 'iPhone 13 256GB', 'iphone_13_256gb', 'IPHONE-13-010', 'iPhone 13 256GB – Balanced storage option', 'iPhone 13 with 256GB storage, perfect balance of capacity and price.', 18990000, 16990000, 12, 22, 'https://example.com/qr/10.png', true, 'iPhone 13', NOW(), NOW()),
(11, 32, 'iPhone 13 128GB', 'iphone_13_128gb', 'IPHONE-13-011', 'iPhone 13 – Powerful performance, dual camera, 6.1" Super Retina XDR', 'iPhone 13 features elegant design, exceptional performance with A15 Bionic chip, improved battery life, 6.1" Super Retina XDR display, dual 12MP camera with Night mode and Cinematic Mode.', 16990000, 14990000, 12, 30, 'https://example.com/qr/11.png', true, 'iPhone 13', NOW(), NOW()),
(12, 34, 'iPhone 13 Mini 256GB', 'iphone_13_mini_256gb', 'IPHONE-13-012', 'iPhone 13 Mini – Compact powerhouse', 'iPhone 13 Mini with 5.4" display, A15 Bionic chip, perfect for one-handed use.', 17990000, 15990000, 12, 12, 'https://example.com/qr/12.png', true, 'iPhone 13 Mini', NOW(), NOW()),
(13, 34, 'iPhone 13 Mini 128GB', 'iphone_13_mini_128gb', 'IPHONE-13-013', 'iPhone 13 Mini 128GB – Small size, big performance', 'Compact iPhone 13 Mini with full flagship features in a pocket-friendly size.', 15990000, 13990000, 12, 15, 'https://example.com/qr/13.png', true, 'iPhone 13 Mini', NOW(), NOW()),
(14, 35, 'iPhone 13 Pro Max 512GB', 'iphone_13_pro_max_512gb', 'IPHONE-13-014', 'iPhone 13 Pro Max – Previous gen flagship', 'iPhone 13 Pro Max with 6.7" ProMotion display, A15 Bionic, triple camera system.', 25990000, 23990000, 12, 6, 'https://example.com/qr/14.png', true, 'iPhone 13 Pro Max', NOW(), NOW()),
(15, 35, 'iPhone 13 Pro Max 256GB', 'iphone_13_pro_max_256gb', 'IPHONE-13-015', 'iPhone 13 Pro Max 256GB – Pro features, large display', 'iPhone 13 Pro Max with ProMotion, ProRes video, and exceptional battery life.', 23990000, 21990000, 12, 10, 'https://example.com/qr/15.png', true, 'iPhone 13 Pro Max', NOW(), NOW()),
(16, 36, 'iPhone 13 Pro 512GB', 'iphone_13_pro_512gb', 'IPHONE-13-016', 'iPhone 13 Pro – Professional grade features', 'iPhone 13 Pro with 6.1" ProMotion display and advanced camera capabilities.', 23990000, 21990000, 12, 8, 'https://example.com/qr/16.png', true, 'iPhone 13 Pro', NOW(), NOW()),
(17, 36, 'iPhone 13 Pro 256GB', 'iphone_13_pro_256gb', 'IPHONE-13-017', 'iPhone 13 Pro 256GB – Pro performance', 'iPhone 13 Pro with triple camera system and ProRAW photography.', 21990000, 19990000, 12, 14, 'https://example.com/qr/17.png', true, 'iPhone 13 Pro', NOW(), NOW()),
(18, 40, 'iPhone 12 256GB', 'iphone_12_256gb', 'IPHONE-12-018', 'iPhone 12 – 5G capable, dual camera', 'iPhone 12 with A14 Bionic chip, 5G support, and dual camera system.', 15990000, 13990000, 12, 18, 'https://example.com/qr/18.png', true, 'iPhone 12', NOW(), NOW()),
(19, 40, 'iPhone 12 128GB', 'iphone_12_128gb', 'IPHONE-12-019', 'iPhone 12 128GB – Great value flagship', 'iPhone 12 with Super Retina XDR display and Night mode on all cameras.', 13990000, 11990000, 12, 25, 'https://example.com/qr/19.png', true, 'iPhone 12', NOW(), NOW()),
(20, 41, 'iPhone 12 Pro 256GB', 'iphone_12_pro_256gb', 'IPHONE-12-020', 'iPhone 12 Pro – Professional photography', 'iPhone 12 Pro with LiDAR scanner and ProRAW photography capabilities.', 19990000, 17990000, 12, 10, 'https://example.com/qr/20.png', true, 'iPhone 12 Pro', NOW(), NOW()),
(21, 50, 'Samsung Galaxy S23 Ultra 512GB', 'samsung_s23_ultra_512gb', 'SAMSUNG-S23-021', 'Galaxy S23 Ultra – 200MP camera, S Pen included', 'Samsung Galaxy S23 Ultra with 200MP camera, built-in S Pen, and Snapdragon 8 Gen 2.', 28990000, 26990000, 12, 12, 'https://example.com/qr/21.png', true, 'Samsung Galaxy S23', NOW(), NOW()),
(22, 50, 'Samsung Galaxy S23 Ultra 256GB', 'samsung_s23_ultra_256gb', 'SAMSUNG-S23-022', 'Galaxy S23 Ultra 256GB – Flagship Android', 'Premium Samsung flagship with advanced camera system and productivity features.', 25990000, 23990000, 12, 15, 'https://example.com/qr/22.png', true, 'Samsung Galaxy S23', NOW(), NOW()),
(23, 51, 'Samsung Galaxy S23+ 256GB', 'samsung_s23_plus_256gb', 'SAMSUNG-S23-023', 'Galaxy S23+ – Large display, powerful performance', 'Samsung Galaxy S23+ with 6.6" display and all-day battery life.', 22990000, 20990000, 12, 18, 'https://example.com/qr/23.png', true, 'Samsung Galaxy S23', NOW(), NOW()),
(24, 52, 'Samsung Galaxy S23 256GB', 'samsung_s23_256gb', 'SAMSUNG-S23-024', 'Galaxy S23 – Compact flagship', 'Samsung Galaxy S23 with flagship features in a compact form factor.', 19990000, 17990000, 12, 22, 'https://example.com/qr/24.png', true, 'Samsung Galaxy S23', NOW(), NOW()),
(25, 52, 'Samsung Galaxy S23 128GB', 'samsung_s23_128gb', 'SAMSUNG-S23-025', 'Galaxy S23 128GB – Entry flagship', 'Affordable entry to Samsung flagship lineup with premium features.', 17990000, 15990000, 12, 28, 'https://example.com/qr/25.png', true, 'Samsung Galaxy S23', NOW(), NOW()),
(26, 60, 'iPhone 16 Pro Max 1TB', 'iphone_16_pro_max_1tb', 'IPHONE-16-026', 'iPhone 16 Pro Max – Latest flagship with 1TB storage', 'iPhone 16 Pro Max with A18 Pro chip, titanium design, 48MP Fusion camera, and revolutionary Action button.', 39990000, 37990000, 12, 8, 'https://example.com/qr/26.png', true, 'iPhone 16 Pro Max', NOW(), NOW()),
(27, 60, 'iPhone 16 Pro Max 512GB', 'iphone_16_pro_max_512gb', 'IPHONE-16-027', 'iPhone 16 Pro Max 512GB – Premium titanium design', 'Latest iPhone with A18 Pro, advanced camera system, and longest battery life ever.', 36990000, 34990000, 12, 12, 'https://example.com/qr/27.png', true, 'iPhone 16 Pro Max', NOW(), NOW()),
(28, 60, 'iPhone 16 Pro Max 256GB', 'iphone_16_pro_max_256gb', 'IPHONE-16-028', 'iPhone 16 Pro Max 256GB – Flagship performance', 'iPhone 16 Pro Max with 6.9" display, A18 Pro chip, and pro camera features.', 33990000, 31990000, 12, 15, 'https://example.com/qr/28.png', true, 'iPhone 16 Pro Max', NOW(), NOW()),
(29, 61, 'iPhone 16 Pro 1TB', 'iphone_16_pro_1tb', 'IPHONE-16-029', 'iPhone 16 Pro – Maximum storage capacity', 'iPhone 16 Pro with 1TB storage, titanium frame, and advanced computational photography.', 36990000, 34990000, 12, 6, 'https://example.com/qr/29.png', true, 'iPhone 16 Pro', NOW(), NOW()),
(30, 61, 'iPhone 16 Pro 512GB', 'iphone_16_pro_512gb', 'IPHONE-16-030', 'iPhone 16 Pro 512GB – Pro features, compact size', 'iPhone 16 Pro with 6.3" display, A18 Pro chip, and professional camera system.', 33990000, 31990000, 12, 10, 'https://example.com/qr/30.png', true, 'iPhone 16 Pro', NOW(), NOW()),
(31, 61, 'iPhone 16 Pro 256GB', 'iphone_16_pro_256gb', 'IPHONE-16-031', 'iPhone 16 Pro 256GB – Balanced pro option', 'iPhone 16 Pro with titanium design and advanced camera capabilities.', 30990000, 28990000, 12, 18, 'https://example.com/qr/31.png', true, 'iPhone 16 Pro', NOW(), NOW()),
(32, 62, 'iPhone 16 Plus 512GB', 'iphone_16_plus_512gb', 'IPHONE-16-032', 'iPhone 16 Plus – Large display, extended battery', 'iPhone 16 Plus with 6.7" display, A18 chip, and exceptional battery life.', 28990000, 26990000, 12, 14, 'https://example.com/qr/32.png', true, 'iPhone 16 Plus', NOW(), NOW()),
(33, 62, 'iPhone 16 Plus 256GB', 'iphone_16_plus_256gb', 'IPHONE-16-033', 'iPhone 16 Plus 256GB – Big screen experience', 'iPhone 16 Plus with large display and all-day battery performance.', 25990000, 23990000, 12, 20, 'https://example.com/qr/33.png', true, 'iPhone 16 Plus', NOW(), NOW()),
(34, 62, 'iPhone 16 Plus 128GB', 'iphone_16_plus_128gb', 'IPHONE-16-034', 'iPhone 16 Plus 128GB – Affordable large screen', 'Entry-level iPhone 16 Plus with flagship features and large display.', 23990000, 21990000, 12, 25, 'https://example.com/qr/34.png', true, 'iPhone 16 Plus', NOW(), NOW()),
(35, 63, 'iPhone 16 512GB', 'iphone_16_512gb', 'IPHONE-16-035', 'iPhone 16 – Latest standard flagship', 'iPhone 16 with A18 chip, improved camera, and new Action button.', 26990000, 24990000, 12, 16, 'https://example.com/qr/35.png', true, 'iPhone 16', NOW(), NOW()),
(36, 63, 'iPhone 16 256GB', 'iphone_16_256gb', 'IPHONE-16-036', 'iPhone 16 256GB – Modern design, powerful chip', 'iPhone 16 with enhanced camera system and improved performance.', 23990000, 21990000, 12, 22, 'https://example.com/qr/36.png', true, 'iPhone 16', NOW(), NOW()),
(37, 63, 'iPhone 16 128GB', 'iphone_16_128gb', 'IPHONE-16-037', 'iPhone 16 128GB – Entry to latest generation', 'Affordable iPhone 16 with all the latest features and improvements.', 21990000, 19990000, 12, 30, 'https://example.com/qr/37.png', true, 'iPhone 16', NOW(), NOW()),
(38, 70, 'iPhone 17 Pro Max 1TB', 'iphone_17_pro_max_1tb', 'IPHONE-17-038', 'iPhone 17 Pro Max – Next-gen flagship (Pre-order)', 'Upcoming iPhone 17 Pro Max with A19 Pro chip, revolutionary camera, and AI features.', 44990000, 42990000, 12, 5, 'https://example.com/qr/38.png', true, 'iPhone 17 Pro Max', NOW(), NOW()),
(39, 70, 'iPhone 17 Pro Max 512GB', 'iphone_17_pro_max_512gb', 'IPHONE-17-039', 'iPhone 17 Pro Max 512GB – Future flagship (Pre-order)', 'Next generation iPhone with advanced AI capabilities and improved camera system.', 41990000, 39990000, 12, 8, 'https://example.com/qr/39.png', true, 'iPhone 17 Pro Max', NOW(), NOW()),
(40, 70, 'iPhone 17 Pro Max 256GB', 'iphone_17_pro_max_256gb', 'IPHONE-17-040', 'iPhone 17 Pro Max 256GB – Pre-order now', 'Upcoming flagship with breakthrough features and performance.', 38990000, 36990000, 12, 10, 'https://example.com/qr/40.png', true, 'iPhone 17 Pro Max', NOW(), NOW()),
(41, 71, 'iPhone 17 Pro 1TB', 'iphone_17_pro_1tb', 'IPHONE-17-041', 'iPhone 17 Pro – Next-gen pro features (Pre-order)', 'iPhone 17 Pro with A19 Pro chip and advanced computational photography.', 41990000, 39990000, 12, 6, 'https://example.com/qr/41.png', true, 'iPhone 17 Pro', NOW(), NOW()),
(42, 71, 'iPhone 17 Pro 512GB', 'iphone_17_pro_512gb', 'IPHONE-17-042', 'iPhone 17 Pro 512GB – Professional grade (Pre-order)', 'Next generation pro iPhone with enhanced AI and camera capabilities.', 38990000, 36990000, 12, 12, 'https://example.com/qr/42.png', true, 'iPhone 17 Pro', NOW(), NOW()),
(43, 71, 'iPhone 17 Pro 256GB', 'iphone_17_pro_256gb', 'IPHONE-17-043', 'iPhone 17 Pro 256GB – Pre-order available', 'Upcoming iPhone 17 Pro with revolutionary features and design.', 35990000, 33990000, 12, 15, 'https://example.com/qr/43.png', true, 'iPhone 17 Pro', NOW(), NOW()),
(44, 72, 'iPhone 17 512GB', 'iphone_17_512gb', 'IPHONE-17-044', 'iPhone 17 – Next generation (Pre-order)', 'iPhone 17 with A19 chip, improved battery, and enhanced features.', 31990000, 29990000, 12, 18, 'https://example.com/qr/44.png', true, 'iPhone 17', NOW(), NOW()),
(45, 72, 'iPhone 17 256GB', 'iphone_17_256gb', 'IPHONE-17-045', 'iPhone 17 256GB – Future standard (Pre-order)', 'Next generation iPhone with latest technology and improvements.', 28990000, 26990000, 12, 22, 'https://example.com/qr/45.png', true, 'iPhone 17', NOW(), NOW()),
(46, 72, 'iPhone 17 128GB', 'iphone_17_128gb', 'IPHONE-17-046', 'iPhone 17 128GB – Pre-order now', 'Affordable entry to next generation iPhone lineup.', 26990000, 24990000, 12, 28, 'https://example.com/qr/46.png', true, 'iPhone 17', NOW(), NOW());

SELECT setval('products_prod_id_seq', (SELECT MAX(prod_id) FROM products));
