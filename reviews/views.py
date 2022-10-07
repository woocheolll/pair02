from django.shortcuts import redirect, render
from .models import Review
from .forms import ReviewForm
from django.core.paginator import Paginator


def create(req):
    if req.method == 'POST':
        data = ReviewForm(req.POST)

        if data.is_valid():
            # form 으로 부터 받은 데이터를 가져오기
            db_data = data.save(commit=False)

            # 0 ~ 5 까지의 별점
            for i in range(6):
                if db_data.grade == 0:
                    db_data.star = '☆' * 5
                    break
                # 정수일 때 i 만큼 ★ 으로 채우고 나머지는
                # 5 - i 만큼 ☆ 으로 채운다.
                elif db_data.grade == i:
                    db_data.star = '★' * i + '☆' * (5 - i)
                    break
                # 소수일 때 i + 1 만큼 ★ 으로 채우고 나머지는
                # 4 - i 만큼 ☆ 으로 채운다.
                elif db_data.grade <= i + 1:
                    db_data.star = '★' * (i + 1)  + '☆' * (4 - i)
                    break

            db_data.save()

            return redirect('reviews:index')

    else:
        data = ReviewForm()

    return render(req, 'reviews/create.html', {'data': data})


# ref(pagination) : https://velog.io/@jewon119/Django-%EA%B8%B0%EC%B4%88-ListView
def index(req):
    data = Review.objects.all().order_by('-id')

    # review_list 페이징 처리
    page = req.GET.get('page') #GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(data, '6') #Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.get_page(page) #페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

    return render(req, 'reviews/index.html', {'data': data, 'page': page_obj})


def detail(req, _id):
    db_data = Review.objects.get(id=_id)

    return render(req, 'reviews/detail.html', {'data': db_data})


def update(req, _id):
    db_data = Review.objects.get(id=_id)

    if req.method == 'POST':
        data = ReviewForm(req.POST, instance=db_data)

        if data.is_valid():
            data.save()

            return redirect('reviews:index')

    else:
        data = ReviewForm(instance=db_data)

    return render(req, 'reviews/create.html', {'data': data})


def delete(req, _id):
    Review.objects.get(id=_id).delete()

    return redirect('reviews:index')