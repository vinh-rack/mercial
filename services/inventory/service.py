import re
from datetime import datetime

import grpc
import inventory_pb2
import inventory_pb2_grpc
from db_connection import get_db_connection
from psycopg.rows import dict_row


class InventoryService(inventory_pb2_grpc.InventoryServiceServicer):

    def GetProductById(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT p.*,
                        json_agg(
                            json_build_object(
                                'img_id', pi.img_id,
                                'img_url', pi.img_url,
                                'alt_text', pi.alt_text,
                                'sort_order', pi.sort_order
                            ) ORDER BY pi.sort_order
                        ) FILTER (WHERE pi.img_id IS NOT NULL) as images
                    FROM products p
                    LEFT JOIN product_images pi ON p.prod_id = pi.prod_id
                    WHERE p.prod_id = %s
                    GROUP BY p.prod_id
                """, (request.prod_id,))

                row = cursor.fetchone()
                if not row:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Product not found')
                    return inventory_pb2.ProductResponse()

                return self._build_product_response(row)

    def GetProductBySku(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT p.*,
                        json_agg(
                            json_build_object(
                                'img_id', pi.img_id,
                                'img_url', pi.img_url,
                                'alt_text', pi.alt_text,
                                'sort_order', pi.sort_order
                            ) ORDER BY pi.sort_order
                        ) FILTER (WHERE pi.img_id IS NOT NULL) as images
                    FROM products p
                    LEFT JOIN product_images pi ON p.prod_id = pi.prod_id
                    WHERE p.sku = %s
                    GROUP BY p.prod_id
                """, (request.sku,))

                row = cursor.fetchone()
                if not row:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Product not found')
                    return inventory_pb2.ProductResponse()

                return self._build_product_response(row)

    def ListProducts(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                limit = request.limit if request.limit > 0 else 50
                offset = request.offset if request.offset >= 0 else 0

                cursor.execute("""
                    SELECT p.*,
                        json_agg(
                            json_build_object(
                                'img_id', pi.img_id,
                                'img_url', pi.img_url,
                                'alt_text', pi.alt_text,
                                'sort_order', pi.sort_order
                            ) ORDER BY pi.sort_order
                        ) FILTER (WHERE pi.img_id IS NOT NULL) as images
                    FROM products p
                    LEFT JOIN product_images pi ON p.prod_id = pi.prod_id
                    GROUP BY p.prod_id
                    ORDER BY p.prod_id DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                products = [self._build_product_response(row) for row in cursor.fetchall()]
                return inventory_pb2.ListProductsResponse(products=products)

    def CreateProduct(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                try:
                    slug = self._generate_slug(request.name)
                    now = datetime.now()

                    cursor.execute("""
                        INSERT INTO products (cat_id, name, slug, sku, short_desc, long_desc,
                                            price, discount_price, warranty_months, stock_qty, status, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING prod_id
                    """, (
                        request.cat_id, request.name, slug, request.sku,
                        request.short_desc, request.long_desc, request.price,
                        request.discount_price, request.warranty_months,
                        request.stock_qty, request.status, now, now
                    ))

                    prod_id = cursor.fetchone()['prod_id']
                    conn.commit()

                    cursor.execute("""
                        SELECT p.*,
                            json_agg(
                                json_build_object(
                                    'img_id', pi.img_id,
                                    'img_url', pi.img_url,
                                    'alt_text', pi.alt_text,
                                    'sort_order', pi.sort_order
                                ) ORDER BY pi.sort_order
                            ) FILTER (WHERE pi.img_id IS NOT NULL) as images
                        FROM products p
                        LEFT JOIN product_images pi ON p.prod_id = pi.prod_id
                        WHERE p.prod_id = %s
                        GROUP BY p.prod_id
                    """, (prod_id,))

                    row = cursor.fetchone()
                    return self._build_product_response(row)
                except Exception as e:
                    conn.rollback()
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(e))
                    return inventory_pb2.ProductResponse()

    def UpdateProduct(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                try:
                    cursor.execute("SELECT prod_id FROM products WHERE prod_id = %s", (request.prod_id,))
                    if not cursor.fetchone():
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details('Product not found')
                        return inventory_pb2.ProductResponse()

                    slug = self._generate_slug(request.data.name)
                    now = datetime.now()

                    cursor.execute("""
                        UPDATE products
                        SET cat_id = %s, name = %s, slug = %s, sku = %s, short_desc = %s,
                            long_desc = %s, price = %s, discount_price = %s,
                            warranty_months = %s, stock_qty = %s, status = %s, updated_at = %s
                        WHERE prod_id = %s
                    """, (
                        request.data.cat_id, request.data.name, slug, request.data.sku,
                        request.data.short_desc, request.data.long_desc, request.data.price,
                        request.data.discount_price, request.data.warranty_months,
                        request.data.stock_qty, request.data.status, now, request.prod_id
                    ))

                    conn.commit()

                    cursor.execute("""
                        SELECT p.*,
                            json_agg(
                                json_build_object(
                                    'img_id', pi.img_id,
                                    'img_url', pi.img_url,
                                    'alt_text', pi.alt_text,
                                    'sort_order', pi.sort_order
                                ) ORDER BY pi.sort_order
                            ) FILTER (WHERE pi.img_id IS NOT NULL) as images
                        FROM products p
                        LEFT JOIN product_images pi ON p.prod_id = pi.prod_id
                        WHERE p.prod_id = %s
                        GROUP BY p.prod_id
                    """, (request.prod_id,))

                    row = cursor.fetchone()
                    return self._build_product_response(row)
                except Exception as e:
                    conn.rollback()
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(e))
                    return inventory_pb2.ProductResponse()

    def DeactivateProduct(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE products SET status = false, updated_at = %s WHERE prod_id = %s",
                             (datetime.now(), request.prod_id))
                conn.commit()

                success = cursor.rowcount > 0
                return inventory_pb2.DeleteProductResponse(success=success)

    def DeleteProduct(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM product_images WHERE prod_id = %s", (request.prod_id,))
                cursor.execute("DELETE FROM products WHERE prod_id = %s", (request.prod_id,))
                conn.commit()

                success = cursor.rowcount > 0
                return inventory_pb2.DeleteProductResponse(success=success)

    def AdjustStock(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                try:
                    cursor.execute("SELECT stock_qty FROM products WHERE prod_id = %s FOR UPDATE",
                                 (request.prod_id,))
                    row = cursor.fetchone()

                    if not row:
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details('Product not found')
                        return inventory_pb2.StockResponse()

                    new_stock = row['stock_qty'] + request.adjustment

                    if new_stock < 0:
                        context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                        context.set_details('Insufficient stock')
                        return inventory_pb2.StockResponse()

                    cursor.execute("UPDATE products SET stock_qty = %s, updated_at = %s WHERE prod_id = %s",
                                 (new_stock, datetime.now(), request.prod_id))
                    conn.commit()

                    return inventory_pb2.StockResponse(prod_id=request.prod_id, stock_qty=new_stock)
                except Exception as e:
                    conn.rollback()
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(e))
                    return inventory_pb2.StockResponse()

    def GetStockLevel(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT prod_id, stock_qty FROM products WHERE prod_id = %s",
                             (request.prod_id,))
                row = cursor.fetchone()

                if not row:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Product not found')
                    return inventory_pb2.StockResponse()

                return inventory_pb2.StockResponse(
                    prod_id=row['prod_id'],
                    stock_qty=row['stock_qty']
                )

    def _build_product_response(self, row):
        images = []
        if row.get('images'):
            for img in row['images']:
                images.append(inventory_pb2.ProductImage(
                    img_id=img['img_id'],
                    img_url=img['img_url'],
                    alt_text=img.get('alt_text', ''),
                    sort_order=img['sort_order']
                ))

        return inventory_pb2.ProductResponse(
            prod_id=row['prod_id'],
            cat_id=row['cat_id'],
            name=row['name'],
            slug=row['slug'],
            sku=row.get('sku') or '',
            short_desc=row.get('short_desc') or '',
            long_desc=row.get('long_desc') or '',
            price=int(row['price']),
            discount_price=int(row.get('discount_price') or 0),
            warranty_months=row['warranty_months'],
            stock_qty=row['stock_qty'],
            status=bool(row['status']),
            images=images
        )

    def _generate_slug(self, name):
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '_', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug
