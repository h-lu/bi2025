import requests
import json
from datetime import datetime

class ExchangeRateAPI:
    def __init__(self):
        # 极速数据的API密钥
        self.api_key = "你的极速数据API密钥"
        self.base_url = "https://api.jisuapi.com/exchange/currency"
    
    def get_exchange_rate(self, from_currency="CNY", to_currency="USD"):
        """
        获取汇率信息
        :param from_currency: 源货币代码，默认人民币
        :param to_currency: 目标货币代码，默认美元
        :return: 汇率信息字典
        """
        params = {
            "appkey": self.api_key,
            "from": from_currency,
            "to": to_currency
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result["status"] == 0:
                return result["result"]
            else:
                print(f"获取汇率数据失败: {result['msg']}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
            return None

    def save_exchange_data(self, data, filename):
        """
        保存汇率数据到JSON文件
        """
        if data:
            data['timestamp'] = datetime.now().isoformat()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {filename}")

def main():
    # 创建ExchangeRateAPI实例
    exchange_api = ExchangeRateAPI()
    
    # 获取人民币兑换美元的汇率
    rate_data = exchange_api.get_exchange_rate("CNY", "USD")
    
    if rate_data:
        # 打印汇率信息
        print("\n当前汇率信息:")
        print(f"货币对: {rate_data['from']}/{rate_data['to']}")
        print(f"汇率: {rate_data['rate']}")
        print(f"更新时间: {rate_data['update']}")
        
        # 保存完整数据到文件
        exchange_api.save_exchange_data(rate_data, 'exchange_rate.json')

if __name__ == "__main__":
    main() 