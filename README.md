## **프로젝트 주제**
- 기본적인 회원기능과 상품기능을 가지고 있는 마켓을 DjangoRestFramework를 사용하여 구현한 프로젝트

## **개발환경**
- OS : Window
- IDE : VsCode
- Python version : 3.11
- DataBase : Sqlite3
- Framework : Django
- PIP : [pillow, simple-jwt, Django-extensions, ipython,djagorestframework]


## **API ENDPOINT**
![image](https://github.com/user-attachments/assets/b122e8b9-3d7b-40cf-afdb-8ddd49945f46)




## **기능 구현**
- 회원관련기능
    - **회원가입**
        - **조건**: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
        - **검증**: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
        - **구현**: 데이터 검증 후 저장.

          **회원가입 REQUEST**
     ![image](https://github.com/user-attachments/assets/7dec0bc1-49cd-417c-b5a8-e9601bb7f289)
          **201 Created**
          ![image](https://github.com/user-attachments/assets/ff8037c1-9f8d-4502-bcb3-028b7ba7296a)
          **401 BadRequest**
          ![image](https://github.com/user-attachments/assets/234bd065-5b28-4aaa-a6c0-d59f8cd9009b)

    - **로그인**
        - **조건**: 사용자명과 비밀번호 입력 필요.
        - **검증**: 사용자명과 비밀번호가 데이터베이스의 기록과 일치해야 함.
        - **구현**: 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.
     
          **로그인 REQUEST**
          ![image](https://github.com/user-attachments/assets/f459d0b8-5492-4ffd-aa39-687582cf649e)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/6620655f-3f3c-4359-918e-302d742c6890)
          **400 BadRequest**
          ![image](https://github.com/user-attachments/assets/29d76995-f733-4fb5-bb97-a7bfdb675492)


    - **프로필 조회**
        - **조건**: 로그인 상태 필요.
        - **검증**: 로그인 한 사용자만 프로필 조회 가능
        - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.
     
          **프로필 조회 REQUEST**
          ![image](https://github.com/user-attachments/assets/4509a979-4241-4946-919e-165793859e2c)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/ba12ea10-e35f-4ad9-ad4e-bd515530a8fc)
          **403 Forbidden**
          ![image](https://github.com/user-attachments/assets/bc4755ed-f06d-4921-b9db-90e91c32fea7)
          **404 NotFound**
          ![image](https://github.com/user-attachments/assets/5ee875d7-10ad-4fef-8079-9547bb5a1fe4)


    - **로그아웃**
        - **조건**: 로그인 상태 필요.
        - **구현**: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
     
          **로그아웃 REQUEST**
          ![image](https://github.com/user-attachments/assets/7df37783-2aaf-4290-b3a7-06e6d52768fe)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/fda7c90a-530f-4495-99ef-41fe66386b8f)
          **401 Unauthorized**
          ![image](https://github.com/user-attachments/assets/a260e441-903c-4559-978f-7616ce72f7e9)


    - **본인 정보 수정**
        - **조건**: 이메일, 이름, 닉네임, 생일 입력 필요하며, 성별, 자기소개 생략 가능
        - **검증**: 로그인 한 사용자만 본인 프로필 수정 가능. 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안 됨.
        - **구현**: 입력된 정보를 검증 후 데이터베이스를 업데이트.
     
          **회원정보 수정 REQUEST**
          ![image](https://github.com/user-attachments/assets/a71d356b-0a62-4d3d-8447-4d1b5f5362b6)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/29745145-8a09-4e45-8504-0aa25ff167e7)
          **400 BadRequest**
          ![image](https://github.com/user-attachments/assets/1750a2d8-18a1-46d0-a8e5-186f075fa5bc)
          **403 Forbidden**
          ![image](https://github.com/user-attachments/assets/e4da468d-31b8-4635-a674-4fad81014474)

  
    - **패스워드 변경**
        - 조건: 기존 패스워드와 변경할 패스워드는 상이해야 함
        - 검증: 패스워드 규칙 검증
        - 구현: 패스워드 검증 후 데이터베이스에 업데이트.
     
          **패스워드 변경 REQUEST**
          ![image](https://github.com/user-attachments/assets/8210913d-5812-47ca-a41d-a34c994e77d0)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/61ee4b4a-2195-4c08-be83-d990ddd6bd18)
          **400 BadRequest**
          ![image](https://github.com/user-attachments/assets/d00e5556-0df1-4ac4-8a2b-c37f6148aa67)


    - **회원 탈퇴**
        - **조건**: 로그인 상태, 비밀번호 재입력 필요.
        - **검증**: 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
        - **구현**: 비밀번호 확인 후 계정 삭제.
     
          **회원삭제 REQUEST**
          ![image](https://github.com/user-attachments/assets/51ace9de-8704-4a1c-89ed-a846e25ab36b)
          **204 NoContent**
          ![image](https://github.com/user-attachments/assets/33793466-a1a4-44bc-848d-8904044803a6)
          **401 Unauthorized**
          ![image](https://github.com/user-attachments/assets/fbd9829c-cf3f-453e-8d7d-d6cd9d090af1)




- 상품관련기능
    - **상품 등록**
        - **조건**: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
        - **구현**: 새 게시글 생성 및 데이터베이스 저장.
     
          **상품 등록 REQUEST**
          ![image](https://github.com/user-attachments/assets/a4da4e65-3ca8-42a4-8c54-0c6a5fbe6a87)
          **201 Created**
          ![image](https://github.com/user-attachments/assets/ccce37cb-ae74-4592-9e3a-c38930e14e7b)
          **400 BadRequest**
          ![image](https://github.com/user-attachments/assets/6a06a1ce-6f7b-4bd4-92b6-288a6b615710)

          
    - **상품 목록 조회**
        - **조건**: 로그인 상태 불필요.
        - **구현**: 모든 상품 목록 페이지네이션으로 반환.
     
          **상품목록조회 REQUEST**
          ![image](https://github.com/user-attachments/assets/44a5de4d-79bb-467d-8dc6-7f10b4146f8c)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/aef98ff3-ab17-438f-a998-52a4e953464b)

            
    - **상품 수정**
        - **조건**: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
        - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
        - **구현**: 입력된 정보로 기존 상품 정보를 업데이트.
     
          **상품수정 REQUEST**
          ![image](https://github.com/user-attachments/assets/926a40dc-b64b-4e69-9aed-4d1cec09734e)
          **200 OK**
          ![image](https://github.com/user-attachments/assets/35b9dce8-2990-4f2e-9535-544038f616fb)
          **403 Forbidden**
          ![image](https://github.com/user-attachments/assets/7828b485-d22f-496d-a283-3c0306a9daf0)


    - **상품 삭제**
        - **조건**: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
        - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
        - **구현**: 해당 상품을 데이터베이스에서 삭제.
     
          **상품삭제 REQUEST**
          ![image](https://github.com/user-attachments/assets/f90daf6d-dd8c-4774-886e-cd1416fc235c)
          **204 NoContent**
          ![image](https://github.com/user-attachments/assets/f7291b73-bcdd-47f3-9623-a8e32953ed73)
          **403 Forbidden**
          ![image](https://github.com/user-attachments/assets/52f02aaf-386f-4fdd-808a-5f07db84fbe9)

         
## **ERD 작성**
![image](https://github.com/user-attachments/assets/4f83aa9a-fcc7-4d79-a1b9-04519ffafa2a)

## **트러블 슈팅**
1. product_img field default None 문제
   - Products.product_img 필드에 default값을 지정했음에도 불구하고 상품등록을 했을때 아예 빈값이 들어가는것을 확인
   - 변수에 default img이름을 넣고 저장된 변수를 img_field의 default 속성에 넣음
   - 문제가 해결이 안되는것을 인지하고 Model을 다시 구성하기로 하고 데이터베이스 삭제 및 migration진행
   - 그럼에도 불구하고 계속해서 imagefield에 값이 안들어가는 상황이 발생
   - serializer하면서 validate를 하는과정에서 img_field값이 None 일때 default값을 넣는 코드를 작성
   - 결과적으로는 imagefield에 값을 안넣을때 자동적으로 default값이 들어가는것을 확인 후 해결

2. API accounts/logout의 Method 방식 매칭 에러
   - 로그아웃 기능구현에 대한 코드를 마친 후 POSTMAN에서의 응답을 확인하던 중 Method POST not Allow 에러를 인지
   - 에러 내용이 단순히 Method POST not Allow 이 한줄이였기 때문에 더욱 원인을 찾기 어려웠음
   - 작성한 코드 중에 문법적으로 실수한 부분이 있는지 확인
   - method 관련 오류라 def post로 받았는지 그리고 POSTMAN에서의 메소드 방식을 정확하게 POST로 했는지 확인
   - POSTMAN의 헤더부분을 확인해본 결과 POSTMAN은 GET으로 인식하고있었음
   - 코드를 계속해서 확인했지만 method관련 문제는 없어보였음
   - accounts/urls.py에서 url들을 보던중 문제 원인 파악
   - 이전의 만들었던 'accounts/<str:username>/'path를 가진 프로필 리소스 확인
   - 'accounts/logout/' path로 이름지었던 로그아웃을 프로필 리소스로 인식하여 method POST not allow로 빠지는거였음
   - 프로필 리소스의 path를 'accounts/profile/<str:username>/'으로 변경
   - 그 이후로 리소스 경로를 인지하여 제대로 작동하기 시작하여 해결하게 됨
