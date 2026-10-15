## Dự án khóa học

Mục tiêu của dự án này là áp dụng mọi thứ chúng tôi đã học trong khóa học này và xây dựng đường dẫn dữ liệu từ đầu đến cuối.

Bạn sẽ có hai lần thử để gửi dự án của mình. Nếu bạn không có 
thời gian để gửi dự án của mình khi kết thúc lần thử số 1 (bạn bắt đầu khóa học 
muộn, bạn có kế hoạch đi nghỉ, life/work cản trở, v.v.)
hoặc bạn thất bại trong lần thử đầu tiên, 
thì bạn sẽ có cơ hội thứ hai để gửi dự án của mình dưới dạng lần thử
#2. 

Chỉ có hai lần thử.

Hãy nhớ rằng để vượt qua dự án, bạn phải đánh giá 3 đồng nghiệp. Nếu bạn không làm điều đó, dự án của bạn không thể được coi là hoàn thành.

Để tìm các dự án được giao cho bạn, hãy sử dụng liên kết bài tập đánh giá ngang hàng 
và tìm hàm băm của bạn trong cột đầu tiên. Bạn sẽ thấy ba hàng: bạn cần đánh giá 
từng dự án này. Đối với mỗi dự án, bạn cần gửi biểu mẫu một lần,
vì vậy tổng cộng bạn sẽ thực hiện ba lần gửi. 


### Gửi

#### Nỗ lực dự án số 1

Project:

* Form: https://forms.gle/zTJiVYSmCgsENj6y8
* Hạn chót: 10 tháng 4, 22:00 CET

Đánh giá ngang hàng:

* Bài tập đánh giá ngang hàng: [link](https://docs.google.com/spreadsheets/d/e/2PACX-1vRYQ0A9C7AkRK-YPSFhqaRMmuPR97QPfl2PjI8n11l5jntc6YMHIJXVVS0GQNqAYIGwzyevyManDB08/pubhtml?gid=0&single=true) (tờ ("dự án-01")
* Form: https://forms.gle/1bxmgR8yPwV359zb7
* Hạn chót: 17 tháng 4, 22:00 CET

Phản hồi về dự án: [link](https://docs.google.com/spreadsheets/d/e/2PACX-1vQuMt9m1XlPrCACqnsFTXTV_KGiSnsl9UjL7kdTMsLJ8DLu3jNJlPzoUKG6baxc8APeEQ8RaSP1U2VX/pubhtml?gid=27207346&single=true) (tờ ("dự án-01")

#### Nỗ lực dự án #2

Project:

* Form: https://forms.gle/gCXUSYBm1KgMKXVm8
* Hạn chót: 4 tháng 5, 22:00 CET

Đánh giá ngang hàng:

* Bài tập đánh giá ngang hàng: [link](https://docs.google.com/spreadsheets/d/e/2PACX-1vRYQ0A9C7AkRK-YPSFhqaRMmuPR97QPfl2PjI8n11l5jntc6YMHIJXVVS0GQNqAYIGwzyevyManDB08/pubhtml?gid=303437788&single=true) (tờ ("dự án-02")
* Form: https://forms.gle/2x5MT4xxczR8isy37
* Hạn chót: 11 tháng 5, 22:00 CET

Phản hồi dự án: [link](https://docs.google.com/spreadsheets/d/e/2PACX-1vQuMt9m1XlPrCACqnsFTXTV_KGiSnsl9UjL7kdTMsLJ8DLu3jNJlPzoUKG6baxc8APeEQ8RaSP1U2VX/pubhtml?gid=246029638&single=true)

### Tiêu chí đánh giá

See [here](../../week_7_project/README.md)


### Linh tinh

Để lấy hàm băm cho dự án của bạn, hãy sử dụng chức năng này để băm email của bạn:

```python
from hashlib import sha1

def compute_hash(email):
    return sha1(email.lower().encode('utf-8')).hexdigest()
```

Or use [this website](http://www.sha1-online.com/). 
