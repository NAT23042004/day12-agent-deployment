# Deployment Information

## Public URL
https://day12-production-f11f.up.railway.app

## Platform
Railway

## Test Commands (Self-Test)

Thực hiện các lệnh sau để kiểm tra tính sẵn sàng của hệ thống:

### 1. Health check
Kiểm tra xem Agent có đang hoạt động hay không.
```bash
curl https://day12-production-f11f.up.railway.app/health
# Expected: {"status": "ok", ...}
```

### 2. Authentication required
Kiểm tra xem hệ thống có từ chối truy cập khi thiếu API Key hay không.
```bash
curl -i https://day12-production-f11f.up.railway.app/ask -X POST
# Expected: HTTP/1.1 401 Unauthorized
```

### 3. With API key works
Kiểm tra phản hồi của Agent khi có đủ API Key và dữ liệu hợp lệ.
```bash
curl -X POST https://day12-production-f11f.up.railway.app/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
# Expected: HTTP/1.1 200 OK với câu trả lời từ Agent
```

### 4. Advanced: Tìm chuyến bay và khách sạn
Kiểm tra khả năng gọi tool của Agent.
```bash
curl -X POST https://day12-production-f11f.up.railway.app/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Tìm giúp tôi chuyến bay từ Hà Nội đi Nha Trang và khách sạn dưới 2 triệu ở đó."}'
```

### 5. Advanced: Kiểm tra ghi nhớ ngữ cảnh (Stateless with Redis)
Gửi câu hỏi tiếp theo để xem Agent có nhớ thành phố bạn vừa hỏi không.
```bash
curl -X POST https://day12-production-f11f.up.railway.app/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Ở đó có khách sạn 5 sao nào không?"}'
# Agent nên trả lời về khách sạn 5 sao tại Nha Trang (dựa trên câu hỏi trước).
```

### 6. Rate limiting
Kiểm tra cơ chế chặn spam (giới hạn 10 request/phút).
```bash
for i in {1..15}; do 
  curl -H "X-API-Key: my-secret-key" \
       -H "Content-Type: application/json" \
       https://day12-production-f11f.up.railway.app/ask \
       -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Expected: Sẽ nhận được lỗi 429 Too Many Requests sau 10 lần gọi.
```

## Environment Variables Set
- **PORT:** `8000` (Assigned by Railway)
- **REDIS_URL:** `redis://default:VcqbvxeiMyZtPgeEDbZehJODueCSHyLh@redis.railway.internal:6379`
- **AGENT_API_KEY:** `my-secret-key`
- **OPENAI_API_KEY:** `sk-proj-xxxx` (Required for real agent)
- **ENVIRONMENT:** `production`
- **DEBUG:** `false`

## Screenshots
Vui lòng xem thư mục `screenshots/` để xác nhận:
1. Dashboard Railway hiển thị service Active.
2. Kết quả chạy thành công các lệnh test trên.
