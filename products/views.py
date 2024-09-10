from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ProductsSerializers
from rest_framework.response import Response
from rest_framework import status
from .models import Products, HashTag
from .pagination import CustomPageNumberPagination
from django.db.models import Q
from django.core import serializers


# 상품 등록과 조회 기능
class ProductsListView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

# - **조건**: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
# - **구현**: 새 게시글 생성 및 데이터베이스 저장.
    # 상품 등록
    def post(self, request):
        serializer = ProductsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save(seller=request.user)
            hashtags = request.data.get('hashtag')
            hashtags = [hashtag.strip() for hashtag in hashtags.split(',')]
            for hashtag in hashtags:
                hashtag, created = HashTag.objects.get_or_create(tags=hashtag)
                product.hashtag.add(hashtag.pk)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

# - **조건**: 로그인 상태 불필요.
# - **구현**: 모든 상품 목록 페이지네이션으로 반환.
    # 상품 목록 조회
    def get(self, request):
        query = request.query_params.get('query', '').strip()

        products = Products.objects.all()

        if query:
            products = products.filter(
                Q(seller__username__icontains=query) |
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
        products = products.order_by('-pk')

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        page_serializers = ProductsSerializers(paginated_products, many=True)
        print(page_serializers.data)
        return paginator.get_paginated_response(page_serializers.data)

# 상품 수정과 삭제 기능


class ProductsDetailView(APIView):
    permission_classes = [IsAuthenticated]
# - **조건**: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
# - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
# - **구현**: 입력된 정보로 기존 상품 정보를 업데이트.
    # 상품 수정

    def put(self, request, product_id):
        user = request.user
        product = get_object_or_404(Products, pk=product_id)

        if user == product.seller:
            # 일치하면 상품수정 가능
            serializer = ProductsSerializers(
                product, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                product = serializer.save()
                product.hashtag.clear()
                hashtags = request.data.get('hashtag')
                hashtags = [hashtag.strip() for hashtag in hashtags.split(',')]
                for hashtag in hashtags:
                    hashtag, created = HashTag.objects.get_or_create(tags=hashtag)
                    product.hashtag.add(hashtag.pk)
                return Response(serializer.data)
        else:
            return Response({"message": "유저와 상품판매자가 일치하지않음"}, status=status.HTTP_403_FORBIDDEN)

# - **조건**: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
# - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
# - **구현**: 해당 상품을 데이터베이스에서 삭제.
    # 상품 삭제
    def delete(self, request, product_id):
        user = request.user
        product = get_object_or_404(Products, pk=product_id)
        if user == product.seller:
            product.delete()
            return Response({"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "삭제할 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
