from langchain_core.tools import tool

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Đà Nẵng", "Hà Nội"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_600_000,
            "class": "economy",
        },
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "08:50", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "13:20", "price": 1_300_000, "class": "economy"},
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "19:20",
            "price": 2_200_000,
            "class": "business",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_600_000,
            "class": "economy",
        },
        {"airline": "VietJet Air", "departure": "09:40", "arrival": "10:50", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "14:00", "arrival": "15:10", "price": 1_200_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "20:10", "arrival": "21:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Hà Nội"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_200_000,
            "class": "economy",
        },
        {"airline": "VietJet Air", "departure": "10:20", "arrival": "11:40", "price": 850_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "14:20", "arrival": "15:40", "price": 750_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
    ("Hà Nội", "Nha Trang"): [
        {"airline": "Vietnam Airlines", "departure": "08:30", "arrival": "10:20", "price": 1_850_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:15", "arrival": "15:05", "price": 1_200_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Huế"): [
        {"airline": "Bamboo Airways", "departure": "09:00", "arrival": "10:30", "price": 1_150_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "16:45", "arrival": "18:15", "price": 1_900_000, "class": "business"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Huang Thanh Luxury", "stars": 5, "price_per_night": 1_300_000},
        {"name": "Silk Danang Beach", "stars": 4, "price_per_night": 1_200_000},
        {"name": "Riviel Danang", "stars": 3, "price_per_night": 650_000},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000},
        {"name": "Christina & Romance", "stars": 2, "price_per_night": 350_000},
    ],
    "Nha Trang": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 4_500_000},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_800_000},
        {"name": "Sheraton Nha Trang", "stars": 5, "price_per_night": 3_200_000},
    ],
    "Huế": [
        {"name": "Azerai La Residence", "stars": 5, "price_per_night": 5_500_000},
        {"name": "Indochine Palace", "stars": 5, "price_per_night": 2_100_000},
        {"name": "Huế Riverside", "stars": 3, "price_per_night": 750_000},
    ],
    "Phú Quốc": [
        {"name": "VieganI Resort", "stars": 5, "price_per_night": 3_500_000},
        {"name": "Sunset Palms", "stars": 4, "price_per_night": 1_500_000},
        {"name": "Bai Truong", "stars": 4, "price_per_night": 1_500_000},
        {"name": "Island Resort", "stars": 3, "price_per_night": 800_000},
        {"name": "Station Hostel", "stars": 3, "price_per_night": 200_000},
        {"name": "Duong Kong", "stars": 4, "price_per_night": 200_000},
    ],
    "Hồ Chí Minh": [
        {"name": "Park Hotel", "stars": 5, "price_per_night": 2_800_000},
        {"name": "Quan 1", "stars": 4, "price_per_night": 900_000},
        {"name": "Central Saigon", "stars": 4, "price_per_night": 1_400_000},
        {"name": "Conchi Yen Hostel", "stars": 3, "price_per_night": 650_000},
        {"name": "The Cannon Room", "stars": 2, "price_per_night": 150_000},
        {"name": "Quan 1", "stars": 4, "price_per_night": 150_000},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay hay giải hạn phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đích (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về dạnh sách chuyến bay hay giải hạn.
    Nếu không có chuyến bay, trả về thông báo lỗi
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu FLIGHTS_DB[(origin, destination)]
    # - Nếu tìm thấy - format danh sách chuyến bay dễ đọc, bao gồm giá tiền
    # - Nếu không tìm thấy - thử tra ngược(destination, origin) - nếu có chuyến bay ngược thì trả về thông báo "Không tìm thấy chuyến bay từ X đến Y, nhưng có chuyến bay từ Y đến X"
    # - Nếu cũng không có - "Không tìm thấy chuyến bay từ X đến Y"
    # - Gợi ý: format giá tiền có dấu chấm phân cách (VD: 1.450.000 VND)

    if (origin, destination) not in FLIGHTS_DB:
        # Kiểm tra nếu có chuyến bay ngược
        if (destination, origin) not in FLIGHTS_DB:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        flights = FLIGHTS_DB[(destination, origin)]
    else:
        flights = FLIGHTS_DB[(origin, destination)]

    # Format kết quả
    result = f"Chuyến bay từ {origin} đến {destination}:\n"
    for flight in flights:
        result += f"- Hãng: {flight['airline']}, Khởi hành: {flight['departure']}, Đến nơi: {flight['arrival']}, Giá: {flight['price']:,} VND, Hạng: {flight['class']}\n"
    return result


@tool
def search_hotels(city: str, max_price_per_night: int = 9999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố với ngân sách tối đa
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với ngân sách, số sao, giá, khách sạn.
    """

    # TODO: Sinh viên tại triển khai
    # - Tra cứu HOTELS_DB[city]
    # - Lọc theo max_price_per_night
    # - Sắp xếp theo rating giảm dần
    # - Format đẹp.
    #  Nếu không có kết quả nào phù hợp - "Không tìm thấy khách sạn tại X voi giá dưới Y VND. Hãy thử tăng ngân sách."

    # Kiểm tra nếu city không có trong database
    if city not in HOTELS_DB:
        return f"Không tìm thấy khách sạn tại {city}."

    hotels = HOTELS_DB[city]
    # Lọc khách sạn theo max_price_per_night
    filtered_hotels = [hotel for hotel in hotels if int(hotel["price_per_night"]) <= max_price_per_night]

    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night} VND. Hãy thử tăng ngân sách."

    # Sắp xếp khách sạn theo số sao giảm dần
    sorted_hotels = sorted(filtered_hotels, key=lambda x: (-x["stars"], int(x["price_per_night"])))
    result = f"Danh sách các khách sạn sắp xếp theo rating giảm  dần và có giá một đêm dưới {max_price_per_night}d \n"
    for hotel in sorted_hotels:
        result += (
            f"- Khách sạn: {hotel['name']}, Rating: {hotel['stars']}, Giá một đêm: {hotel['price_per_night']:,}d, \n"
        )
    return result


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
    định dạng "tên_khoản:số_tiền" (VD:"ve_may_bay:890000,khach_san:650000")
    Trả ve: bảng chi tíết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # TODO: Sinh viên từ triển khai
    # - Parse chuỗi expenses thành dict (tên: số_tiền)
    # - Tính tổng chi phí
    # - Tinh ngản sách còn lại = total_budget - tổng chi phí
    # - Format bảng chi tiết:
    #   - Vé máy bay: 890.000d
    #   - Khách sạn: 650.000d
    #   - ...
    #   - Tổng chi: 1.540.000d
    #   - Ngân sách còn: 5.000.000d
    #   - Còn lại: 3.460.000d
    # - Nếu chi tiêu account làm vượt ngân sách - tra về có hàng thông báo - trả về thông báo lỗi ở có rằng

    expenses_dict = {x.split(":")[0].strip(): int(x.split(":")[1]) for x in expenses.split(",")}
    total_expense = sum(expenses_dict.values())
    remaning_budget = total_budget - total_expense
    # Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    if remaning_budget < 0:
        return f"!!!Cảnh báo ngân sách còn thiếu {abs(remaning_budget)} VND."

    results = "Bảng chi tiết các khoản chi:\n"
    for category, expense in expenses_dict.items():
        results += f"- {category.replace('_', ' ')}: {expense:,}d\n"

    results += f"- Ngân sách còn: {total_budget}d \n - Còn lại: {remaning_budget}d"
    return results
