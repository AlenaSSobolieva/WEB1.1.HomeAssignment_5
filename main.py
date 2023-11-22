import aiohttp
import asyncio
import json
from datetime import datetime, timedelta

class ExchangeRateFetcher:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"

    async def fetch_exchange_rate(self, session, date):
        async with session.get(self.API_URL.format(date)) as response:
            return await response.json()

    async def fetch_exchange_rates(self, days):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_exchange_rate(session, self.get_date_n_days_ago(i)) for i in range(1, days + 1)]
            return await asyncio.gather(*tasks)

    def get_date_n_days_ago(self, n):
        return (datetime.now() - timedelta(days=n)).strftime('%d.%m.%Y')

    def parse_exchange_rate(self, data):
        result = []

        for day_data in data:
            date = day_data['date']
            rates = {}

            for currency in day_data['exchangeRate']:
                if currency['currency'] in ['EUR', 'USD']:
                    rates[currency['currency']] = {
                        'sale': currency['saleRateNB'],
                        'purchase': currency['purchaseRateNB']
                    }

            if rates:
                result.append({date: rates})

        return result

    def print_result(self, result):
        print(json.dumps(result, indent=2))

async def main():
    days = 10
    fetcher = ExchangeRateFetcher()
    exchange_rate_data = await fetcher.fetch_exchange_rates(days)
    result = fetcher.parse_exchange_rate(exchange_rate_data)
    fetcher.print_result(result)

if __name__ == "__main__":
    asyncio.run(main())

