from datetime import datetime

import bcrypt
import grpc
import user_pb2
import user_pb2_grpc
from db_connection import get_db_connection
from psycopg.rows import dict_row


class UserService(user_pb2_grpc.UserServiceServicer):

    def Register(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                try:
                    cursor.execute("SELECT user_id FROM users WHERE email = %s", (request.email,))
                    if cursor.fetchone():
                        context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                        context.set_details('Email already registered')
                        return user_pb2.UserResponse()

                    password_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    now = datetime.now()

                    cursor.execute("""
                        INSERT INTO users (email, password_hash, first_name, last_name, phone, status, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING user_id
                    """, (request.email, password_hash, request.first_name, request.last_name, request.phone, True, now, now))

                    user_id = cursor.fetchone()['user_id']
                    conn.commit()

                    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                    row = cursor.fetchone()
                    return self._build_user_response(row)
                except Exception as e:
                    conn.rollback()
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(e))
                    return user_pb2.UserResponse()

    def Login(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
                row = cursor.fetchone()

                if not row:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('User not found')
                    return user_pb2.LoginResponse()

                if not bcrypt.checkpw(request.password.encode('utf-8'), row['password_hash'].encode('utf-8')):
                    context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                    context.set_details('Invalid password')
                    return user_pb2.LoginResponse()

                if not row['status']:
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details('User account is deactivated')
                    return user_pb2.LoginResponse()

                user = self._build_user_response(row)
                token = f"token_{row['user_id']}"
                return user_pb2.LoginResponse(user=user, token=token)

    def GetUserById(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (request.user_id,))
                row = cursor.fetchone()

                if not row:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('User not found')
                    return user_pb2.UserResponse()

                return self._build_user_response(row)

    def GetUserByEmail(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
                row = cursor.fetchone()

                if not row:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('User not found')
                    return user_pb2.UserResponse()

                return self._build_user_response(row)

    def ModifyUser(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                try:
                    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (request.user_id,))
                    if not cursor.fetchone():
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details('User not found')
                        return user_pb2.UserResponse()

                    now = datetime.now()
                    updates = []
                    params = []

                    if request.data.email:
                        updates.append("email = %s")
                        params.append(request.data.email)
                    if request.data.first_name:
                        updates.append("first_name = %s")
                        params.append(request.data.first_name)
                    if request.data.last_name:
                        updates.append("last_name = %s")
                        params.append(request.data.last_name)
                    if request.data.phone:
                        updates.append("phone = %s")
                        params.append(request.data.phone)
                    if request.data.password:
                        password_hash = bcrypt.hashpw(request.data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        updates.append("password_hash = %s")
                        params.append(password_hash)

                    updates.append("updated_at = %s")
                    params.append(now)
                    params.append(request.user_id)

                    cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s", params)
                    conn.commit()

                    cursor.execute("SELECT * FROM users WHERE user_id = %s", (request.user_id,))
                    row = cursor.fetchone()
                    return self._build_user_response(row)
                except Exception as e:
                    conn.rollback()
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(e))
                    return user_pb2.UserResponse()

    def DeactivateUser(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET status = false, updated_at = %s WHERE user_id = %s",
                             (datetime.now(), request.user_id))
                conn.commit()

                success = cursor.rowcount > 0
                return user_pb2.SuccessResponse(success=success)

    def DeleteUser(self, request, context):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_id = %s", (request.user_id,))
                conn.commit()

                success = cursor.rowcount > 0
                return user_pb2.SuccessResponse(success=success)

    def _build_user_response(self, row):
        return user_pb2.UserResponse(
            user_id=row['user_id'],
            email=row['email'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            phone=row.get('phone') or '',
            status=bool(row['status']),
            created_at=row['created_at'].isoformat() if row.get('created_at') else '',
            updated_at=row['updated_at'].isoformat() if row.get('updated_at') else ''
        )
