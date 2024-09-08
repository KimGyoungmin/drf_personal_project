## **개발환경**
- OS : Window
- IDE : VsCode
- Python version : 3.11
- DataBase : Sqlite3
- Framework : Django REST Framework
- PIP : [pillow, simple-jwt, Django-extensions, ipython]


## **기능 구현**
- 회원관련기능
    - **회원가입**
        - **조건**: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
        - **검증**: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
        - **구현**: 데이터 검증 후 저장.
    - **로그인**
        - **조건**: 사용자명과 비밀번호 입력 필요.
        - **검증**: 사용자명과 비밀번호가 데이터베이스의 기록과 일치해야 함.
        - **구현**: 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.
    - **프로필 조회**
        - **조건**: 로그인 상태 필요.
        - **검증**: 로그인 한 사용자만 프로필 조회 가능
        - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.
    - **로그아웃**
        - **조건**: 로그인 상태 필요.
        - **구현**: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
    - **본인 정보 수정**
        - **조건**: 이메일, 이름, 닉네임, 생일 입력 필요하며, 성별, 자기소개 생략 가능
        - **검증**: 로그인 한 사용자만 본인 프로필 수정 가능. 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안 됨.
        - **구현**: 입력된 정보를 검증 후 데이터베이스를 업데이트.
    - **패스워드 변경**
        - 조건: 기존 패스워드와 변경할 패스워드는 상이해야 함
        - 검증: 패스워드 규칙 검증
        - 구현: 패스워드 검증 후 데이터베이스에 업데이트.
    - **회원 탈퇴**
        - **조건**: 로그인 상태, 비밀번호 재입력 필요.
        - **검증**: 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
        - **구현**: 비밀번호 확인 후 계정 삭제.

- 상품관련기능
    - **상품 등록**
        - **조건**: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
        - **구현**: 새 게시글 생성 및 데이터베이스 저장.
    - **상품 목록 조회**
        - **조건**: 로그인 상태 불필요.
        - **구현**: 모든 상품 목록 페이지네이션으로 반환.
    - **상품 수정**
        - **조건**: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
        - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
        - **구현**: 입력된 정보로 기존 상품 정보를 업데이트.
    - **상품 삭제**
        - **조건**: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
        - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
        - **구현**: 해당 상품을 데이터베이스에서 삭제.
    - **페이지네이션 및 필터링(검색기능)**
        - **조건**: 상품 목록 조회 시 적용됩니다.
        - **구현**: 제목, 유저명, 내용으로 필터링이 가능하며, 결과는 페이지네이션으로 관리
    - **카테고리 기능(admin page 활용)**
        - 조건: admin 계정만 카테고리 생성 가능하며, 일반/로그인 유저는 상품등록 시 카테고리를 연결할 수 있음.
        - 구현: 생성 시 카테고리명은 유일해야 하며, 연결 시 상품과 카테고리 간의 관계가 데이터베이스에 저장

- 데이터베이스 관계 모델링 선택 기능
    - **팔로잉 시스템**
        - 사용자 간의 **ManyToMany** 관계를 통한 **팔로잉** 기능.
    
    - **태그 기능**
        - 모든 태그는 Unique해야 함
            - Apple, aPple, applE는 같은 단어로 취급하여 데이터베이스 업데이트
         
## **ERD 작성**
![image](https://github.com/user-attachments/assets/751c25f5-a0f9-48b5-9b15-c25bc462a65e)

## **트러블 슈팅**
1. product_img field default None 문제
   - Products.product_img 필드에 default값을 지정했음에도 불구하고 상품등록을 했을때 아예 빈값이 들어가는것을 확인
   - 변수에 default img이름을 넣고 저장된 변수를 img_field의 default 속성에 넣음
   - 문제가 해결이 안되는것을 인지하고 Model을 다시 구성하기로 하고 데이터베이스 삭제 및 migration진행
   - 그럼에도 불구하고 계속해서 imagefield에 값이 안들어가는 상황이 발생
   - serializer하면서 validate를 하는과정에서 img_field값이 None or Null 일때 default값을 넣는 코드를 작성
   - 결과적으로는 imagefield에 값을 안넣을때 자동적으로 default값이 들어가는것을 확인 후 해결

2. API accounts/logout의 Method 방식 매칭 에러
   - 로그아웃 기능구현에 대한 코드를 마친 후 POSTMAN에서의 응답을 확인하던 중 Method POST not Allow 에러를 인지
   - 에러 내용이 단순히 Method POST not Allow 이 한줄이였기 때문에 더욱 원인을 찾기 어려웠음
   - 작성한 코드 중에 문법적으로 실수한 부분이 있는지 확인
   - method 관련 오류라 def post로 받았는지 그리고 POSTMAN에서의 메소드 방식을 정확하게 POST로 했는지 확인
   - POSTMAN의 헤더부분을 확인해본 결과 POSTMAN은 GET으로 인식하고있었음
   - 코드를 계속해서 확인했지만 method관련 문제는 없어보였음
   - accounts/urls.py에서 url들을 보던중 문제 인식
   - 이전의 만들었던 'accounts/<str:username>/'path를 가진 프로필 리소스 확인
   - 'accounts/logout/' path로 이름지었던 로그아웃을 프로필 리소스로 인식하여 method POST not allow로 빠지는거였음
   - 프로필 리소스의 path를 'accounts/profile/<str:username>/'으로 변경
   - 그 이후로 리소스 경로를 인지하여 제대로 작동하기 시작하여 해결하게 됨
