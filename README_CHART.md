# Pionex Real-Time Price Chart

এটি একটি রিয়েল-টাইম চার্ট অ্যাপ্লিকেশন যা Pionex API থেকে BTC/USDT এবং ETH/USDT এর লাইভ প্রাইস দেখায়।

## Features (বৈশিষ্ট্য)

- ✅ **Real-time price updates** - লাইভ প্রাইস আপডেট
- ✅ **Multiple symbols** - একসাথে BTC/USDT এবং ETH/USDT
- ✅ **Interactive chart** - ইন্টারেক্টিভ চার্ট
- ✅ **Customizable update interval** - আপডেট ইন্টারভাল পরিবর্তন করা যায়
- ✅ **Start/Stop controls** - চালু/বন্ধ করার নিয়ন্ত্রণ
- ✅ **Price display** - বর্তমান প্রাইস প্রদর্শন

## Installation (ইনস্টলেশন)

### Method 1: Automatic Installation
```bash
python run_chart.py
```

### Method 2: Manual Installation
```bash
pip install matplotlib requests numpy
python real_time_chart.py
```

## Usage (ব্যবহার)

1. **Run the application** - অ্যাপ্লিকেশন চালু করুন:
   ```bash
   python real_time_chart.py
   ```

2. **Configure settings** - সেটিংস কনফিগার করুন:
   - **Symbols**: ট্রেডিং পেয়ার (default: BTC_USDT,ETH_USDT)
   - **Update Interval**: আপডেটের সময় (default: 5 seconds)

3. **Control updates** - আপডেট নিয়ন্ত্রণ করুন:
   - **Stop Updates**: আপডেট বন্ধ করুন
   - **Start Updates**: আপডেট চালু করুন

## Features Details (বৈশিষ্ট্যের বিবরণ)

### Real-time Data (রিয়েল-টাইম ডেটা)
- Pionex API থেকে সরাসরি প্রাইস ডেটা
- প্রতি 5 সেকেন্ডে আপডেট (পরিবর্তনযোগ্য)
- সর্বশেষ 100 ডেটা পয়েন্ট সংরক্ষণ

### Chart Display (চার্ট প্রদর্শন)
- **BTC/USDT**: লাল রঙে
- **ETH/USDT**: টিল রঙে
- সময় অনুযায়ী প্রাইস ট্রেন্ড
- গ্রিড লাইন সহ

### Price Display (প্রাইস প্রদর্শন)
- বর্তমান প্রাইস বড় ফন্টে
- USDT ফরম্যাটে
- রঙিন কোডিং

## API Information (API তথ্য)

এই অ্যাপ্লিকেশন Pionex এর পাবলিক API ব্যবহার করে:
- **Base URL**: `https://api.pionex.com/api/v1`
- **Endpoints**: 
  - `/market/tickers` - বর্তমান প্রাইস
  - `/market/klines` - হিস্টরিক্যাল ডেটা

## Troubleshooting (সমস্যা সমাধান)

### Common Issues (সাধারণ সমস্যা)

1. **Import Error**:
   ```bash
   pip install matplotlib requests numpy
   ```

2. **Network Error**:
   - ইন্টারনেট সংযোগ চেক করুন
   - Pionex API স্ট্যাটাস চেক করুন

3. **Chart Not Updating**:
   - "Start Updates" বোতাম ক্লিক করুন
   - আপডেট ইন্টারভাল চেক করুন

## Customization (কাস্টমাইজেশন)

### Adding More Symbols (আরও সিম্বল যোগ করা)
```python
self.symbols = ["BTC_USDT", "ETH_USDT", "SOL_USDT", "ADA_USDT"]
```

### Changing Update Interval (আপডেট ইন্টারভাল পরিবর্তন)
- UI থেকে ইন্টারভাল পরিবর্তন করুন
- অথবা কোডে `self.interval_var.set("10")` সেট করুন

### Changing Colors (রঙ পরিবর্তন)
```python
self.colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
```

## System Requirements (সিস্টেম প্রয়োজনীয়তা)

- Python 3.7+
- Windows/Linux/macOS
- Internet connection
- 4GB RAM (recommended)

## Support (সহায়তা)

যদি কোন সমস্যা হয়:
1. Error message চেক করুন
2. Internet connection চেক করুন
3. Dependencies আবার ইনস্টল করুন

---

**Note**: এই অ্যাপ্লিকেশন শুধুমাত্র প্রাইস দেখানোর জন্য। ট্রেডিং এর জন্য নয়। 